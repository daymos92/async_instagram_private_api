import codecs
import hashlib
import hmac
import json
import pickle
import random
import time

from async_instagram_private_api.exceptions import IgNotFoundError, IgCheckpointError, \
    IgUserHasLoggedOutError, IgLoginRequiredError, IgPrivateUserError, \
    IgSentryBlockError, IgInactiveUserError, IgResponseError
from async_instagram_private_api.tools import dict_merge


class Request:
    def __init__(self, client):
        self.client = client

    async def send(self, **kwargs):
        host = 'https://i.instagram.com'
        options = {
            'proxy': self.client.state.proxy_url,
            'method': 'GET',
            'headers': self.get_default_headers()
        }
        options = dict_merge(options, kwargs)
        options['url'] = host + options['url']
        response = await self.client.state.session.request(**options)
        self.update_state(response)

        if response.status == 200:
            return await response.json()

        await self.handle_response_error(response)

    def signature(self, data: str):
        return hmac.new(
            self.client.state.signature_key.encode('ascii'), data.encode('ascii'),
            digestmod=hashlib.sha256).hexdigest()

    def sign(self, data):
        params = json.dumps(data, separators=(',', ':'))
        signature = self.signature(params)
        return {
            'ig_sig_key_version': self.client.state.signature_version,
            'signed_body': '{}.{}'.format(signature, params)
        }

    async def handle_response_error(self, response):
        json_response = await response.json()

        #     if (json.spam) {
        #       return new IgActionSpamError(response);
        #     }

        if response.status == 404:
            raise IgNotFoundError(response)

        message = json_response.get('message')
        if message:
            if message == 'challenge_required':
                self.client.state.checkpoint = json_response
                raise IgCheckpointError(response)
            elif message == 'user_has_logged_out':
                raise IgUserHasLoggedOutError(response)
            elif message == 'login_required':
                raise IgLoginRequiredError(response)
            elif message.lower() == 'not authorized to view user':
                raise IgPrivateUserError(response)
        error_type = json_response.get('error_type')
        if error_type:
            if error_type == 'sentry_block':
                raise IgSentryBlockError(response)
            elif error_type == 'inactive user':
                raise IgInactiveUserError(response)
        raise IgResponseError(response)

    def update_state(self, response):
        www_claim = response.headers.get('x-ig-set-www-claim')
        if isinstance(www_claim, str):
            self.client.state.ig_www_claim = www_claim
        auth = response.headers.get('ig-set-authorization')
        if isinstance(auth, str) and auth[-1] == ':':
            self.client.state.authorization = auth
        pw_key_id = response.headers.get('ig-set-password-encryption-key-id')
        if isinstance(pw_key_id, str):
            self.client.state.password_encryption_key_id = pw_key_id
        pw_pub_key = response.headers.get('ig-set-password-encryption-pub-key')
        if isinstance(pw_pub_key, str):
            self.client.state.password_encryption_pub_key = pw_pub_key

    def get_default_headers(self):
        headers = {
            'User-Agent': self.client.state.app_user_agent,
            'X-Ads-Opt-Out': '1' if self.client.state.ads_opt_out else '0',
            'X-CM-Bandwidth-KBPS': '-1.000',
            'X-CM-Latency': '-1.000',
            'X-IG-App-Locale': self.client.state.language,
            'X-IG-Device-Locale': self.client.state.language,
            'X-Pigeon-Session-Id': self.client.state.pigeon_session_id,
            'X-Pigeon-Rawclienttime': str(round(time.time() / 1000, 3)),
            'X-IG-Connection-Speed': '{}kbps'.format(random.randint(1000, 3700)),
            'X-IG-Bandwidth-Speed-KBPS': '-1.000',
            'X-IG-Bandwidth-TotalBytes-B': '0',
            'X-IG-Bandwidth-TotalTime-MS': '0',
            'X-IG-EU-DC-ENABLED': '' if self.client.state.eu_dc_enabled is None else str(self.client.state.eu_dc_enabled),
            'X-IG-Extended-CDN-Thumbnail-Cache-Busting-Value': str(self.client.state.thumbnail_cache_busting_value),
            'X-Bloks-Version-Id': self.client.state.bloks_version_id,
            'X-MID': self.client.state.extract_cookie('mid') or '',
            'X-IG-WWW-Claim': self.client.state.ig_www_claim or '0',
            'X-Bloks-Is-Layout-RTL': 'true' if self.client.state.is_layout_rtl else 'false',
            'X-IG-Connection-Type': self.client.state.connection_type_header,
            'X-IG-Capabilities': self.client.state.capabilities_header,
            'X-IG-App-ID': self.client.state.fb_analytics_application_id,
            'X-IG-Device-ID': self.client.state.uuid,
            'X-IG-Android-ID': self.client.state.device_id,
            'Accept-Language': self.client.state.language.replace('_', '-'),
            'X-FB-HTTP-Engine': 'Liger',
            'Authorization': self.client.state.authorization or '',
            'Host': 'i.instagram.com',
            'Accept-Encoding': 'gzip',
            'Connection': 'close',
        }
        return headers