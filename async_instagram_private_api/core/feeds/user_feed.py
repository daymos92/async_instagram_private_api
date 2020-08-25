from async_instagram_private_api.core.feed import Feed


class UserFeed(Feed):

    def __init__(self, client, user_id):
        super().__init__(client)
        self.id = user_id
        self.more_available = None
        self.next_max_id = None

    def set_state(self, request):
        self.more_available = request['more_available']
        self.next_max_id = request['next_max_id']

    async def request(self):
        options = {
            'url': f'/api/v1/feed/user/{self.id}/',
        }
        if self.next_max_id:
            options['params'] = {'max_id': self.next_max_id}

        response = await self.client.request.send(**options)
        self.set_state(response)
        return response

    async def items(self):
        response = await self.request()
        return response['items']
