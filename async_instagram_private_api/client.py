from async_instagram_private_api.core.feed_factory import FeedFactory
from async_instagram_private_api.core.request import Request
from async_instagram_private_api.core.state import State
from async_instagram_private_api.repositories.account import AccountRepository
from async_instagram_private_api.repositories.attribution import AttributionRepository
from async_instagram_private_api.repositories.challenge import ChallengeRepository
from async_instagram_private_api.repositories.direct import DirectRepository
from async_instagram_private_api.repositories.discover import DiscoverRepository
from async_instagram_private_api.repositories.fbsearch import FbSearchRepository
from async_instagram_private_api.repositories.launcher import LauncherRepository
from async_instagram_private_api.repositories.linked_account import LinkedAccountRepository
from async_instagram_private_api.repositories.location import LocationRepository
from async_instagram_private_api.repositories.loom import LoomRepository
from async_instagram_private_api.repositories.media import MediaRepository
from async_instagram_private_api.repositories.qe import QeRepository
from async_instagram_private_api.repositories.qp import QpRepository
from async_instagram_private_api.repositories.status import StatusRepository
from async_instagram_private_api.repositories.user import UserRepository
from async_instagram_private_api.repositories.zr import ZrRepository
from async_instagram_private_api.services.simulate import SimulateService


class IgApiClient:

    def __init__(self, settings=None):
        self.state = State(settings)
        self.request = Request(self)
        self.feed = FeedFactory(self)
        #   public entity = new EntityFactory(this);

        #   /* Repositories */
        self.account = AccountRepository(self)
        self.attribution = AttributionRepository(self)
        self.challenge = ChallengeRepository(self)
        #   public consent = new ConsentRepository(this);
        #   public creatives = new CreativesRepository(this);
        self.direct = DirectRepository(self)
        #   public directThread = new DirectThreadRepository(this);
        self.discover = DiscoverRepository(self)
        self.fbsearch = FbSearchRepository(self)
        #   public friendship = new FriendshipRepository(this);
        self.launcher = LauncherRepository(self)
        self.linkedAccount = LinkedAccountRepository(self)
        self.loom = LoomRepository(self)
        self.media = MediaRepository(self)
        self.qe = QeRepository(self)
        self.qp = QpRepository(self)
        #   public tag = new TagRepository(this);
        #   public upload = new UploadRepository(this);
        self.user = UserRepository(self)
        self.zr = ZrRepository(self)
        #   public live = new LiveRepository(this);
        self.location = LocationRepository(self)
        #   public locationSearch = new LocationSearch(this);
        #   public music = new MusicRepository(this);
        #   public news = new NewsRepository(this);
        #   public highlights = new HighlightsRepository(this);
        #   public ads = new AdsRepository(this);
        #   public restrictAction = new RestrictActionRepository(this);
        #   public addressBook = new AddressBookRepository(this);
        self.status = StatusRepository(self)
        #   public igtv = new IgtvRepository(this);
        #   /* Services */
        #   public publish = new PublishService(this);
        #   public search = new SearchService(this);
        self.simulate = SimulateService(self)
        #   public story = new StoryService(this);
        #   public insights = new InsightsService(this);
