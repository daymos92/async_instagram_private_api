from async_instagram_private_api.core.repository import Repository


class FbSearchRepository(Repository):

    async def suggested_searches(self, search_type):
        options = {
            'url': '/api/v1/fbsearch/suggested_searches/',
            'params': {
                'type': search_type,
            }
        }
        response = await self.client.request.send(**options)
        return response

    async def recent_searches(self):
        options = {
            'url': '/api/v1/fbsearch/recent_searches/',
        }
        response = await self.client.request.send(**options)
        return response
