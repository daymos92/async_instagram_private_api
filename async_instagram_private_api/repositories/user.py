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

    async def info(self, user_id):
        options = {
            'url': f'/api/v1/users/{user_id}/info/'
        }
        response = await self.client.request.send(**options)
        return response.get('user')

#   async info(id: string | number): Promise<UserRepositoryInfoResponseUser> {
#     const { body } = await this.client.request.send<UserRepositoryInfoResponseRootObject>({
#       url: `/api/v1/users/${id}/info/`,
#     });
#     return body.user;
#   }