from async_instagram_private_api.core.repository import Repository


class MediaRepository(Repository):

    async def blocked(self):
        options = {
            'url': '/api/v1/media/blocked/',
        }
        response = await self.client.request.send(**options)

        return response['media_ids']
