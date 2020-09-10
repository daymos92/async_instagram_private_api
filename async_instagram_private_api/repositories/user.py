from async_instagram_private_api.core.repository import Repository


class UserRepository(Repository):

    async def arlink_download_info(self):
        options = {
            'url': '/api/v1/users/arlink_download_info/',
            'params': {'version_override': '2.0.2'}
        }
        response = await self.client.request.send(**options)
        return response

    async def account_details(self, user_id):
        options = {
            'url': f'/api/v1/users/{user_id}/account_details/'
        }
        response = await self.client.request.send(**options)
        return response

    async def info(self, user_id=None):
        user_id = user_id or self.client.state.cookie_user_id
        options = {
            'url': f'/api/v1/users/{user_id}/info/'
        }
        response = await self.client.request.send(**options)
        return response.get('user')

    async def search(self, username: str):
        options = {
            'url': f'/api/v1/users/search/',
            'params': {
                'timezone_offset': self.client.state.timezone_offset,
                'q': username,
                'count': 30,
            }
        }
        response = await self.client.request.send(**options)
        return response

    async def search_exact(self, username: str):
        username = username.lower()
        users = await self.search(username)
        if not users['users']:
            return None
        for user in users['users']:
            if user['username'] == username:
                return user
        return None
