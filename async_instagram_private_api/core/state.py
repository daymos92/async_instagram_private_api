import codecs
import pickle
import time
from datetime import datetime
from random import Random
import uuid

import aiohttp
from aiohttp import CookieJar

from ..core import constants as Constants
from ..exceptions import IgCookieNotFoundError, IgNoCheckpointError
from ..samples.builds import BUILDS
from ..samples.devices import DEVICES


class ClientCookieJar(CookieJar):
    """Custom CookieJar that can be pickled to/from strings
    """
    def __init__(self, cookie=None, **kwargs):
        CookieJar.__init__(self, **kwargs)
        if cookie:
            self._cookies = pickle.loads(codecs.decode(cookie.encode(), "base64"))

    def dump(self):
        return codecs.encode(pickle.dumps(self._cookies), "base64").decode()


class State:

    def __init__(self, settings=None):
        if settings is None:
            settings = {}

        self.username = settings.get('username') or None
        self.proxy = settings.get('proxy') or None
        self.limit_connector = settings.get('limit_connector') or 5
        self.timeout = settings.get('timeout') or 5
        self.cookie = settings.get('cookie') or None
        self.checkpoint = settings.get('checkpoint') or None
        self.challenge = settings.get('challenge') or None

        self.device_string = settings.get('device_string') or None

        self.eu_dc_enabled = settings.get('eu_dc_enabled') or None
        self.device_id = settings.get('device_id') or None
        self.uuid = settings.get('uuid') or None
        self.phone_id = settings.get('phone_id') or None
        self.adid = settings.get('adid') or None
        self.build = settings.get('build') or None
        self.timezone_offset = settings.get('timezone_offset') or str(-time.timezone)
        self.client_session_id_lifetime = settings.get('client_session_id_lifetime') or 120000
        self.pigeon_session_id_lifetime = settings.get('pigeon_session_id_lifetime') or 120000
        self.password_encryption_pub_key = settings.get('password_encryption_pub_key') or None
        self.password_encryption_key_id = settings.get('password_encryption_key_id') or None
        self.language = settings.get('language') or 'en_US'
        self.ads_opt_out = settings.get('ads_opt_out') or False
        self.thumbnail_cache_busting_value = settings.get('thumbnail_cache_busting_value') or 1000
        self.is_layout_rtl = settings.get('is_layout_rtl') or False
        self.connection_type_header = settings.get('connection_type_header') or 'WIFI'
        self.capabilities_header = settings.get('capabilities_header') or '3brTvwE='

        self.ig_www_claim = settings.get('ig_www_claim') or None
        self.authorization = settings.get('authorization') or None

        if self.cookie:
            cookie_jar = ClientCookieJar(self.cookie)
        else:
            cookie_jar = ClientCookieJar()
        connector = aiohttp.TCPConnector(verify_ssl=False, limit=self.limit_connector)
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        self.session = aiohttp.ClientSession(connector=connector,
                                             timeout=timeout,
                                             cookie_jar=cookie_jar)

    @property
    def settings(self):
        settings = {
            'username': self.username,
            'proxy': self.proxy,
            'limit_connector': self.limit_connector,
            'timeout': self.timeout,
            'checkpoint': self.checkpoint,
            'challenge': self.challenge,
            'device_string': self.device_string,

            'eu_dc_enabled': self.eu_dc_enabled,
            'device_id': self.device_id,
            'uuid': self.uuid,
            'phone_id': self.phone_id,
            'adid': self.adid,
            'build': self.build,
            'timezone_offset': self.timezone_offset,
            'client_session_id_lifetime': self.client_session_id_lifetime,
            'pigeon_session_id_lifetime': self.pigeon_session_id_lifetime,
            'password_encryption_pub_key': self.password_encryption_pub_key,
            'password_encryption_key_id': self.password_encryption_key_id,
            'language': self.language,
            'ads_opt_out': self.ads_opt_out,
            'thumbnail_cache_busting_value': self.thumbnail_cache_busting_value,
            'is_layout_rtl': self.is_layout_rtl,
            'connection_type_header': self.connection_type_header,
            'capabilities_header': self.capabilities_header,
            'ig_www_claim': self.ig_www_claim,
            'authorization': self.authorization,

            'cookie': self.session.cookie_jar.dump(),
        }
        return settings

    @property
    def signature_key(self):
        return Constants.SIGNATURE_KEY

    @property
    def signature_version(self):
        return Constants.SIGNATURE_VERSION

    @property
    def app_version_code(self):
        return Constants.APP_VERSION_CODE

    @property
    def app_version(self):
        return Constants.APP_VERSION

    @property
    def fb_orca_application_id(self):
        return Constants.FACEBOOK_ORCA_APPLICATION_ID

    @property
    def experiments(self):
        return Constants.EXPERIMENTS

    @property
    def fb_analytics_application_id(self):
        return Constants.FACEBOOK_ANALYTICS_APPLICATION_ID

    @property
    def login_experiments(self):
        return Constants.LOGIN_EXPERIMENTS


    @property
    def bloks_version_id(self):
        return Constants.BLOKS_VERSION_ID

    @property
    def fb_ota_fields(self):
        return Constants.FACEBOOK_OTA_FIELDS

    @property
    def cookie_jar(self):
        if hasattr(self, 'session'):
            return self.session.cookie_jar
        return None

    @property
    def cookie_user_id(self):
        return self.extract_cookie_value('ds_user_id')

    @property
    def cookie_csrf_token(self):
        try:
            return self.extract_cookie_value('csrftoken')
        except IgCookieNotFoundError:
            return 'missing'

    def extract_cookie(self, key):
        if self.session.cookie_jar is None:
            return None
        for cookie in self.cookie_jar:
            if cookie.key.lower() == key.lower():
                return cookie.value

    def extract_cookie_value(self, key):
        cookie = self.extract_cookie(key)
        if cookie is None:
            raise IgCookieNotFoundError
        return cookie

    def generate_device(self, seed: str):
        random_generator = Random(seed)
        self.device_string = random_generator.choice(DEVICES)

        common_id = ''.join(random_generator.choices('abcdef0123456789', k=16))
        self.device_id = f'android-{common_id}'
        self.uuid = str(uuid.UUID(int=random_generator.getrandbits(128)))
        self.phone_id = str(uuid.UUID(int=random_generator.getrandbits(128)))
        self.adid = str(uuid.UUID(int=random_generator.getrandbits(128)))
        self.build = random_generator.choice(BUILDS)

    @property
    def battery_level(self):
        random_generator = Random(self.device_id)
        percent_time = random_generator.randint(200, 600)
        return 100 - (int(time.time() / 1000 / percent_time) / 100)

    @property
    def is_charging(self):
        seed = '{}{}'.format(self.device_id, int(time.time() / 10800000))
        random_generator = Random(seed)
        return random_generator.randint(0, 1) == 1

    @property
    def challenge_url(self):
        if self.checkpoint is None:
            raise IgNoCheckpointError
        return '/api/v1' + self.checkpoint['challenge']['api_path']

    @property
    def client_session_id(self):
        return self.generate_temporary_guid('clientSessionId', self.client_session_id_lifetime)

    @property
    def pigeon_session_id(self):
        return self.generate_temporary_guid('pigeonSessionId', self.pigeon_session_id_lifetime)

    @property
    def app_user_agent(self):
        user_agent = f'Instagram {self.app_version} Android ({self.device_string}; {self.language}; {self.app_version_code})'
        return user_agent

    def generate_temporary_guid(self, seed, lifetime):
        full_seed = '{seed}{device_id}{time}'.format(
            seed=seed, device_id=self.device_id, time=int(time.time() - lifetime)
        )
        random_generator = Random(full_seed)
        return str(uuid.UUID(int=random_generator.getrandbits(128)))
