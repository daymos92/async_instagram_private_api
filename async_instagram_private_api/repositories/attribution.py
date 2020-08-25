from async_instagram_private_api.core.repository import Repository


class AttributionRepository(Repository):

    async def log_attribution(self):
        options = {
            'method': 'POST',
            'url': '/api/v1/attribution/log_attribution/',
            'data': self.client.request.sign({'adid': self.client.state.adid}),
        }
        response = await self.client.request.send(**options)
        return response

    async def log_resurrect_attribution(self):
        try:
            options = {
                'method': 'POST',
                'url': '/api/v1/attribution/log_resurrect_attribution/',
                'data': self.client.request.sign({
                    '_csrftoken': self.client.state.cookie_csrf_token,
                    '_uid': self.client.state.cookie_user_id,
                    'adid': self.client.state.adid,
                    '_uuid': self.client.state.uuid,
                })
            }
            response = await self.client.request.send(**options)
            return response
        except:
            pass
