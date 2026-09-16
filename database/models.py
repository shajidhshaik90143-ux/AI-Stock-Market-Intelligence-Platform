from dataclasses import dataclass
from datetime import datetime


@dataclass
class WatchlistItem:
    ticker: str
    id: int | None = None
    created_at: datetime | None = None


@dataclass
class SearchRecord:
    ticker: str
    id: int | None = None
    searched_at: datetime | None = None