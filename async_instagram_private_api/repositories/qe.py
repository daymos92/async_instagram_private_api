from async_instagram_private_api.core.repository import Repository
from async_instagram_private_api.exceptions import IgCookieNotFoundError


class QeRepository(Repository):

    async def sync(self, experiments):
        try:
            uid = self.client.state.cookie_user_id
            data = {
                '_csrftoken': self.client.state.cookie_csrf_token,
                'id': uid,
                '_uid': uid,
                '_uuid': self.client.state.uuid,
            }
        except IgCookieNotFoundError:
            data = {
                'id': self.client.state.uuid
            }
        data['experiments'] = experiments

        options = {
            'method': 'POST',
            'url': '/api/v1/qe/sync/',
            'headers': {
                'X-DEVICE-ID': self.client.state.uuid,
            },
            'data': self.client.request.sign(data),
        }
        response = await self.client.request.send(**options)
        return response

    async def sync_experiments(self):
        return await self.sync(self.client.state.experiments)

    async def sync_login_experiments(self):
        return await self.sync(self.client.state.login_experiments)
