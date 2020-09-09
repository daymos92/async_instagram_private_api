from ..feeds.direct_inbox import DirectInboxFeed
from ..feeds.direct_pending import DirectPendingInboxFeed
from ..feeds.timeline import TimelineFeed
from ..feeds.user_feed import UserFeed


class FeedFactory:
    def __init__(self, client):
        self.client = client

    def timeline(self, reason=None):
        feed = TimelineFeed(self.client)
        if reason:
            feed.reason = reason
        return feed

    def direct_inbox(self):
        return DirectInboxFeed(self.client)

    def direct_pending(self):
        return DirectPendingInboxFeed(self.client)

    def user(self, user_id):
        feed = UserFeed(self.client, user_id)
        return feed
