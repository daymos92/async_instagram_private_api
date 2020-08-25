from async_instagram_private_api.core.repository import Repository


class StatusRepository(Repository):

    async def get_viewable_statuses(self):
        options = {
            'url': '/api/v1/status/get_viewable_statuses/',
            'method': 'GET',
        }
        response = await self.client.request.send(**options)
        return response
