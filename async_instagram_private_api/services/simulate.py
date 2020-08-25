import random

from async_instagram_private_api.core.repository import Repository


class SimulateService(Repository):

    def __init__(self, client):
        super().__init__(client)
        self.client = client

    def pre_login_flow_requests(self) -> list:
        requests = [
            self.client.account.read_msisdn_header(),
            self.client.account.msisdn_header_bootstrap('ig_select_app'),
            self.client.zr.token_result(),
            self.client.account.contact_point_prefill('prefill'),
            self.client.launcher.pre_login_sync(),
            self.client.qe.sync_login_experiments(),
            self.client.attribution.log_attribution(),
            self.client.account.get_prefill_candidates(),
        ]
        return requests

    def post_login_flow_requests(self):
        requests = [
            self.client.zr.token_result(),
            self.client.launcher.post_login_sync(),
            self.client.qe.sync_experiments(),
            self.client.attribution.log_attribution(),
            self.client.attribution.log_resurrect_attribution(),
            self.client.loom.fetch_config(),
            self.client.linkedAccount.get_linkage_status(),
            # // () => this.client.creatives.writeSupportedCapabilities(),
            # // () => this.client.account.processContactPointSignals(),
            self.client.feed.timeline().request({'recovered_from_crash': '1', 'reason': 'cold_start_fetch'}),
            self.client.fbsearch.suggested_searches('users'),
            self.client.fbsearch.suggested_searches('blended'),
            self.client.fbsearch.recent_searches(),
            self.client.direct.ranked_recipients('reshare'),
            self.client.direct.ranked_recipients('raven'),
            self.client.direct.get_presence(),
            self.client.feed.direct_inbox().request(),
            self.client.media.blocked(),
            self.client.qp.batch_fetch(),
            self.client.qp.get_cooldowns(),
            self.client.user.arlink_download_info(),
            self.client.discover.topical_explore(),
            self.client.discover.mark_su_seen(),
            self.facebook_ota(),
            self.client.status.get_viewable_statuses(),
        ]
        return requests

    async def _execute_request_flow(self, requests: list, to_shuffle=True):
        if to_shuffle:
            random.shuffle(requests)

        for request in requests:
            response = await request
            pass

    async def pre_login_flow(self, to_shuffle=True):
        await self._execute_request_flow(self.pre_login_flow_requests(), to_shuffle)

    async def post_login_flow(self, to_shuffle=True):
        await self._execute_request_flow(self.post_login_flow_requests(), to_shuffle)

    async def facebook_ota(self):
        uid = self.client.state.cookie_user_id
        options = {
            'url': '/api/v1/facebook_ota/',
            'params': {
                'fields': self.client.state.fb_ota_fields,
                'custom_user_id': uid,
                'signed_body': self.client.request.signature('') + '.',
                'ig_sig_key_version': self.client.state.signature_version,
                'version_code': self.client.state.app_version_code,
                'version_name': self.client.state.app_version,
                'custom_app_id': self.client.state.fb_orca_application_id,
                'custom_device_id': self.client.state.uuid,
            },
        }
        response = await self.client.request.send(**options)
        return response
