from enum import Enum
from typing import List, Literal

from pydantic import BaseModel, Field


class ArticleType(str, Enum):
    TOPS = "tops"
    PANTS = "pants"
    SWEATERS = "sweaters"
    SHOES = "shoes"


class ArticleSize(BaseModel):
    article_type: ArticleType = Field(description="article type")
    size: str = Field(description="article size")


class UserProfile(BaseModel):
    """ Profile of a user """
    name: str = Field(description="The user's preferred name")
    gender: Literal["male", "female", "other"] = Field(
        description="The user's preferred gender")
    user_article_sizes: List[ArticleSize] = Field(
        description="A list of the user's interests")
