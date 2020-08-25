import base64
import json
from datetime import datetime

from Crypto.Cipher import PKCS1_v1_5, AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

from async_instagram_private_api.core.repository import Repository
from async_instagram_private_api.exceptions import IgResponseError, IgLoginTwoFactorRequiredError, \
    IgLoginBadPasswordError, IgLoginInvalidUserError, IgSignupBlockError


class AccountRepository(Repository):

    async def login(self, username: str, password: str):
        if not self.client.state.password_encryption_pub_key:
            self.client.qe.sync_login_experiments()

        encrypted, time = self.encrypt_password(password)

        options = {
            'method': 'POST',
            'url': '/api/v1/accounts/login/',
            'data': self.client.request.sign({
                'username': username,
                'password': password,
                # 'enc_password': f'#PWD_INSTAGRAM:4:{time}:{encrypted}',
                'uid': self.client.state.uuid,
                'phone_id': self.client.state.phone_id,
                '_csrftoken': self.client.state.cookie_csrf_token,
                'device_id': self.client.state.device_id,
                'adid': '',
                'google_tokens': '[]',
                'login_attempt_count': 0,
                'country_codes': json.dumps([{'country_code': '1', 'source': 'default'}]),
                'jazoest': self.create_jazoest(self.client.state.phone_id)
            })
        }
        try:
            response = await self.client.request.send(**options)
            return response['logged_in_user']
        except IgResponseError as e:
            response_json = await e.response.json()
            if response_json.get('two_factor_required'):
                raise IgLoginTwoFactorRequiredError(e.response)
            elif response_json.get('error_type') == 'bad_password':
                raise IgLoginBadPasswordError(e.response)
            elif response_json.get('error_type') == 'invalid_user':
                raise IgLoginInvalidUserError(e.response)
            raise e

    @staticmethod
    def create_jazoest(text: str):
        buf = bytes(text, 'ascii')
        byte_sum = 0
        for b in buf:
            byte_sum += int(b)
        return f'2{byte_sum}'

    async def read_msisdn_header(self, usage='default'):
        options = {
            'method': 'POST',
            'url': '/api/v1/accounts/read_msisdn_header/',
            'headers': {'X-DEVICE-ID': self.client.state.uuid},
            'data': self.client.request.sign({
                'mobile_subno_usage': usage,
                'device_id': self.client.state.uuid,
            }),
        }
        response = await self.client.request.send(**options)
        return response

    async def msisdn_header_bootstrap(self, usage='default'):
        options = {
            'method': 'POST',
            'url': '/api/v1/accounts/msisdn_header_bootstrap/',
            'data': self.client.request.sign({
                'mobile_subno_usage': usage,
                'device_id': self.client.state.uuid,
            }),
        }
        response = await self.client.request.send(**options)
        return response

    async def contact_point_prefill(self, usage='default'):
        options = {
            'method': 'POST',
            'url': '/api/v1/accounts/contact_point_prefill/',
            'data': self.client.request.sign({
                'mobile_subno_usage': usage,
                'device_id': self.client.state.uuid,
            }),
        }
        response = await self.client.request.send(**options)
        return response

    async def get_prefill_candidates(self):
        options = {
            'method': 'POST',
            'url': '/api/v1/accounts/get_prefill_candidates/',
            'data': self.client.request.sign({
                'android_device_id': self.client.state.device_id,
                'usages': '["account_recovery_omnibox"]',
                'device_id': self.client.state.uuid,
            }),
        }
        response = await self.client.request.send(**options)
        return response

    def encrypt_password(self, password: str):
        session_key = get_random_bytes(32)
        iv = bytearray(12)
        time = str(int(datetime.now().timestamp()))
        decoded_publickey = base64.b64decode(self.client.state.password_encryption_pub_key.encode())
        recipient_key = RSA.import_key(decoded_publickey)
        cipher_rsa = PKCS1_v1_5.new(recipient_key)
        enc_session_key = cipher_rsa.encrypt(session_key)
        cipher_aes = AES.new(session_key, AES.MODE_GCM, iv)
        cipher_aes.update(time.encode())
        ciphertext, tag = cipher_aes.encrypt_and_digest(password.encode("utf8"))
        payload = base64.b64encode(
            (b"\x01\x00" + int(self.client.state.password_encryption_key_id).to_bytes(2, byteorder='big') +
             iv + len(enc_session_key).to_bytes(2, byteorder='big') + enc_session_key + tag + ciphertext)
        )
        return payload.decode(), time

    async def create(self, username, password, email, first_name):
        options = {
            'method': 'POST',
            'url': '/api/v1/accounts/create/',
            'data': self.client.request.sign({
                'username': username,
                'password': password,
                'email': email,
                'first_name': first_name,
                'guid': self.client.state.uuid,
                'device_id': self.client.state.device_id,
                '_csrftoken': self.client.state.cookie_csrf_token,
                'force_sign_up_code': '',
                'qs_stamp': '',
                'waterfall_id': self.client.state.uuid,
                'sn_nonce': '',
                'sn_result': '',
            })
        }
        try:
            response = await self.client.request.send(**options)
            return response
        except IgResponseError as e:
            response_json = await e.response.json()
            if response_json.get('error_type') == 'signup_block':
                raise IgSignupBlockError(e.response)
            raise e


