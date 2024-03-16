from typing import List, Optional
from pydantic import BaseModel


class NamedUrl(BaseModel):
    name: str
    url: str


class PositionInfo(BaseModel):
    position: str
    name: str
    blog_articles_urls: str
    youtube_interviews_urls: List[NamedUrl]


class CompanyInfo(BaseModel):
    company: str
    positions: List[PositionInfo]
