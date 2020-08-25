from async_instagram_private_api.core.repository import Repository


class DirectRepository(Repository):

    async def ranked_recipients(self, mode, query=''):
        options = {
            'url': '/api/v1/direct_v2/ranked_recipients/',
            'method': 'GET',
            'params': {
                'mode': mode,
                'query': query,
                'show_threads': True,
            }
        }
        response = await self.client.request.send(**options)
        return response

    async def get_presence(self):
        options = {
            'url': '/api/v1/direct_v2/get_presence/',
            'method': 'GET'
        }
        response = await self.client.request.send(**options)
        return response
