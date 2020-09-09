from async_instagram_private_api.core.repository import Repository


class DiscoverRepository(Repository):
    async def topical_explore(self):
        options = {
            'url': '/api/v1/discover/topical_explore/',
            'params': {
                'is_prefetch': 'true',
                'omit_cover_media': 'false',
                'use_sectional_payload': 'true',
                'timezone_offset': self.client.state.timezone_offset,
                'session_id': self.client.state.client_session_id,
                'include_fixed_destinations': 'false',
            }
        }
        response = await self.client.request.send(**options)
        return response

    async def mark_su_seen(self):
        options = {
            'url': '/api/v1/discover/mark_su_seen/',
            'method': 'POST',
            'data': self.client.request.sign({
                '_csrftoken': self.client.state.cookie_csrf_token,
                '_uuid': self.client.state.uuid,
            })
        }
        response = await self.client.request.send(**options)
        return response

    async def facebook_ota(self):
        options = {
            'url': '/api/v1/facebook_ota/',
            'params': {
                'fields': self.client.state.fb_ota_fields,
                'custom_user_id': self.client.state.cookie_user_id,
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
