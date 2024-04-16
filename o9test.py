import abc
import enum

from bs4 import BeautifulSoup
from urllib.request import urlopen

from pydantic import BaseModel


URL = "https://www.jrepodcast.com/episodes/"


class HTMLTAG(enum.Enum):
    DIV = "div"

    def __str__(self):
        return self.value


class CSSTagClass(enum.Enum):
    PAGE_SECTION = "page-section page-section--body"
    CARD_THUMBNAIL = "card__thumbnail-wrapper"
    CARD_WRAPPER = "card__wrapper"

    def __str__(self):
        return self.value


class EpisodesDataSchema(BaseModel):
    title: str
    duration: str
    date: str

    class Config:
        extra = "forbid"

    def __str__(self):
        return f"Title: {self.title} \nDate: {self.date} \nDuration: ({self.duration}) \n\n"


class EpisodeDataManager:
    def __init__(self) -> None:
        self.episodes = []
    
    def add_episode_data(self, episode: EpisodesDataSchema) -> None:
        self.episodes.append(episode)
    
    def get_episodes_data(self) -> list:
        return self.episodes


class AbstractEpisodeFactory(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def create_episode_data(div, *attrs):
        pass


class JoeRoganEpisodeFactory(AbstractEpisodeFactory):

    @staticmethod
    def create_episode_data(div, attrs):
        data = {}
        print(attrs)
        for attr, (tag, klass) in attrs.items():
            content = div.find(tag, class_=klass)
            if content:
                data[attr] = content.text
        print(data)
        return EpisodesDataSchema(**data)


class WebScraper(abc.ABC):
    def __init__(self, url):
        self.url = url
        self.episode_manager = EpisodeDataManager()
    
    @abc.abstractmethod
    def define_attributes(self, *attrs):
        pass

    @abc.abstractmethod
    def scrape(self):
        pass

    @abc.abstractmethod
    def update_episode_data(self):
        pass


class JoeRoganPodcastScraper(WebScraper):
    def __init__(self, url) -> None:
        super().__init__(url)
        self.episode_data = []
    
    def define_attributes(self, *attrs):
        """
        attrs = ((title, html_tag, css_class))
        """
        self.attributes = {attr[0]: [a for a in attr[1:]] for attr in attrs}
    
    def scrape(self):
        page = urlopen(self.url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        page_section = soup.find(HTMLTAG.DIV, class_=CSSTagClass.PAGE_SECTION)

        card_details = page_section.find_all(HTMLTAG.DIV, class_=CSSTagClass.CARD_WRAPPER)
        for div in card_details:
            self.episode_data.append(JoeRoganEpisodeFactory.create_episode_data(div, self.attributes))
    
    def update_episode_data(self):
        for ep_data in self.episode_data:
            self.episode_manager.add_episode_data(ep_data)

