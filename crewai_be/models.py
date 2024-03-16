from typing import List, Optional
from pydantic import BaseModel


class NamedUrl(BaseModel):
    name: str
    url: str


class PositionInfo(BaseModel):
    position: str
    name: str
    blog_articles_urls: List[NamedUrl]
    youtube_interviews_urls: List[NamedUrl]
    picture_url: Optional[str]


class CompanyInfo(BaseModel):
    company: str
    positions: List[PositionInfo]
