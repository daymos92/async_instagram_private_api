
class IgClientError(Exception):
    message = None

    def __init__(self, message='Instagram API error was made.'):
        self.message = message


class IgResponseError(IgClientError):
    response = None

    def __init__(self, response):
        message = '{} {} - {}'.format(response.method, response.url, response.status)
        super(IgResponseError, self).__init__(message=message)
        self.response = response


class IgNoCheckpointError(IgClientError):
    pass


class IgChallengeWrongCodeError(IgClientError):
    pass


class IgSignupBlockError(IgResponseError):
    pass


class IgNotFoundError(IgResponseError):
    pass


class IgRequestsLimitError(IgClientError):

    def __init__(self):
        message = "You just made too many request to instagram API"
        super(IgRequestsLimitError, self).__init__(message)


class IgCheckpointError(IgResponseError):

    def url(self):
        return self.response.json().get('challenge').get('url')

    def apt_url(self):
        return 'https://i.instagram.com/api/v1' + self.response.json().get('challenge').get('api_path')


class IgLoginTwoFactorRequiredError(IgResponseError):
    pass


class IgLoginBadPasswordError(IgResponseError):
    pass


class IgLoginInvalidUserError(IgResponseError):
    pass


class IgUserHasLoggedOutError(IgResponseError):
    pass


class IgLoginRequiredError(IgResponseError):
    pass


class IgPrivateUserError(IgResponseError):
    pass


class IgSentryBlockError(IgResponseError):
    pass


class IgInactiveUserError(IgResponseError):
    pass


class IgCookieNotFoundError(IgClientError):
    pass

