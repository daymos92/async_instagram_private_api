from async_instagram_private_api.core.repository import Repository
from async_instagram_private_api.exceptions import IgNoCheckpointError, IgResponseError, \
    IgChallengeWrongCodeError


class ChallengeRepository(Repository):

    async def state(self):
        options = {
            'url': self.client.state.challenge_url,
            'params': {
                'guid': self.client.state.uuid,
                'device_id': self.client.state.device_id,
            },
        }
        response = await self.client.request.send(**options)
        self.middleware(response)

    # Phone number choice = 0, email = 1
    async def select_verify_method(self, choice, is_reply=False):
        url = self.client.state.challenge_url
        if is_reply:
            url = url.replace('/challenge/', '/challenge/replay/')
        options = {
            'url': url,
            'method': 'POST',
            'data': self.client.request.sign({
                'choice': choice,
                '_csrftoken': self.client.state.cookie_csrf_token,
                'guid': self.client.state.uuid,
                'device_id': self.client.state.device_id,
            })
        }
        response = await self.client.request.send(**options)
        self.middleware(response)
        return response

    # Phone number choice = 0, email = 1
    async def replay(self, choice):
        return await self.select_verify_method(choice, True)

    # choice It was me = 0, It wasn't me = 1
    async def delta_login_review(self, choice):
        return await self.select_verify_method(choice)

    async def send_phone_number(self, phone_number):
        options = {
            'url': self.client.state.challenge_url,
            'method': 'POST',
            'data': self.client.request.sign({
                'phone_number': phone_number,
                '_csrftoken': self.client.state.cookie_csrf_token,
                'guid': self.client.state.uuid,
                'device_id': self.client.state.device_id,
            }),
        }
        response = await self.client.request.send(**options)
        self.middleware(response)
        return response

    async def reset(self):
        options = {
            'url': self.client.state.challenge_url.replace('/challenge/', '/challenge/reset/'),
            'method': 'POST',
            'data': self.client.request.sign({
                '_csrftoken': self.client.state.cookie_csrf_token,
                'guid': self.client.state.uuid,
                'device_id': self.client.state.device_id,
            }),
        }
        response = await self.client.request.send(**options)
        self.middleware(response)
        return response

    async def auto(self, reset=False):
        if self.client.state.checkpoint is None:
            raise IgNoCheckpointError
        if reset:
            await self.reset()
        if self.client.state.challenge is None:
            await self.state()
        challenge = self.client.state.challenge
        if challenge['step_name'] == 'select_verify_method':
            return await self.select_verify_method(challenge['step_data']['choice'])
        elif challenge['step_name'] == 'delta_login_review':
            return await self.delta_login_review('0')
        else:
            return challenge

    async def sent_security_code(self, code):
        options = {
            'url': self.client.state.challenge_url,
            'method': 'POST',
            'data': self.client.request.sign({
                'security_code': code,
                '_csrftoken': self.client.state.cookie_csrf_token,
                'guid': self.client.state.uuid,
                'device_id': self.client.state.device_id,
            }),
        }
        try:
            response = await self.client.request.send(**options)
        except IgResponseError as e:
            response_json = await e.response.json()
            if e.response.status == 400 and response_json['status'] == 'fail':
                raise IgChallengeWrongCodeError(response_json['message'])
            raise e
        self.middleware(response)
        return response

    def middleware(self, response):
        if response.get('action') == 'close':
            self.client.state.checkpoint = None
            self.client.state.challenge = None
        else:
            self.client.state.challenge = response
