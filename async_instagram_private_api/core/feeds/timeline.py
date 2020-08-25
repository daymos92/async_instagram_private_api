from async_instagram_private_api.core.feed import Feed


class TimelineFeed(Feed):
    def __init__(self, client):
        super().__init__(client)
        self.next_max_id = None
        self.reason = None
        self.more_available = None

    def set_state(self, response):
        self.more_available = response['more_available']
        self.next_max_id = response['next_max_id']

    async def request(self, form_options):
        form = {
            'is_prefetch': '0',
            'feed_view_info': '',
            'seen_posts': '',
            'phone_id': self.client.state.phone_id,
            'is_pull_to_refresh': '0',
            'battery_level': self.client.state.battery_level,
            'timezone_offset': self.client.state.timezone_offset,
            '_csrftoken': self.client.state.cookie_csrf_token,
            'client_session_id': self.client.state.client_session_id,
            'device_id': self.client.state.uuid,
            '_uuid': self.client.state.uuid,
            'is_charging': int(self.client.state.is_charging),
            'is_async_ads_in_headload_enabled': 0,
            'rti_delivery_backend': 0,
            'is_async_ads_double_request': 0,
            'will_sound_on': 0,
            'is_async_ads_rti': 0,
            'recovered_from_crash': form_options.get('recovered_from_crash'),
            'push_disabled': form_options.get('push_disabled'),
            'latest_story_pk': form_options.get('latest_story_pk'),
        }

        if self.next_max_id:
            form.update({
                'max_id': self.next_max_id,
                'reason': form_options.get('reason') or 'pagination'
            })
        else:
            form.update({
                'reason': form_options.get('reason') or self.reason,
                'is_pull_to_refresh': '1' if self.reason == 'is_pull_to_refresh' else '0'
            })

        options = {
            'url': '/api/v1/feed/timeline/',
            'method': 'POST',
            'headers': {
                'X-Ads-Opt-Out': 0,
                'X-Google-AD-ID': self.client.state.adid,
                'X-DEVICE-ID': self.client.state.uuid,
                'X-FB': 1,
            },
            'form': form,
        }
        response = await self.client.request.send(**options)
        self.set_state(response)
        return response
