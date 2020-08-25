from async_instagram_private_api.core.repository import Repository


class LoomRepository(Repository):
    async def fetch_config(self):
        options = {
            'url': '/api/v1/loom/fetch_config/',
        }
        response = await self.client.request.send(**options)
        return response
