from async_instagram_private_api.core.feed import Feed


class DirectInboxFeed(Feed):

    def __init__(self, client):
        super().__init__(client)
        self.cursor = None
        self.seq_id = None
        self.more_available = None

    def set_state(self, response):
        self.more_available = response['inbox']['has_older']
        self.seq_id = response['seq_id']
        self.cursor = response['inbox']['oldest_cursor']

    async def request(self):
        options = {
            'url': '/api/v1/direct_v2/inbox/',
            'params': {
                'visual_message_return_type': 'unseen',
                # 'cursor': self.cursor,
                'direction': 'older' if self.cursor else '',
                'seq_id': self.seq_id,
                'thread_message_limit': 10,
                'persistentBadging': 'true',
                'limit': 20,
            },
        }
        if self.cursor:
            options['params']['cursor'] = self.cursor
        if self.seq_id:
            options['params']['seq_id'] = self.seq_id
        response = await self.client.request.send(**options)

        self.set_state(response)
        return response

    async def items(self):
        response = await self.request()
        return response['inbox']['threads']
