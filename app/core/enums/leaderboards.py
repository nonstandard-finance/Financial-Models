from enum import Enum


class LeaderboardType(str, Enum):
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    ALL_TIME = "All Time"
