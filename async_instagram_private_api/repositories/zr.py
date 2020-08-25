from async_instagram_private_api.core.repository import Repository


class ZrRepository(Repository):

    async def token_result(self):
        options = {
            'url': '/api/v1/zr/token/result/',
            'params': {
                'device_id': self.client.state.device_id,
                'token_hash': '',
                'custom_device_id': self.client.state.uuid,
                'fetch_reason': 'token_expired',
            }
        }
        response = await self.client.request.send(**options)
        return response
