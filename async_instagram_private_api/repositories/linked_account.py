from async_instagram_private_api.core.repository import Repository


class LinkedAccountRepository(Repository):
    async def get_linkage_status(self):
        options = {
            'url': '/api/v1/linked_accounts/get_linkage_status/',
        }
        response = await self.client.request.send(**options)
        return response
