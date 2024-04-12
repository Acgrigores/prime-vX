from collections import namedtuple
from typing import List, Tuple

from prime_vx.db import (
    ANNUAL_ISSUE_COUNT_DB_TABLE_NAME,
    DAILY_ISSUE_COUNT_DB_TABLE_NAME,
    MONTHLY_ISSUE_COUNT_DB_TABLE_NAME,
    SIX_MONTH_ISSUE_COUNT_DB_TABLE_NAME,
    THREE_MONTH_ISSUE_COUNT_DB_TABLE_NAME,
    TWO_MONTH_ISSUE_COUNT_DB_TABLE_NAME,
    TWO_WEEK_ISSUE_COUNT_DB_TABLE_NAME,
    WEEKLY_ISSUE_COUNT_DB_TABLE_NAME,
)

BUCKET_STOR = namedtuple(
    typename="BUCKET_STOR",
    field_names=[
        DAILY_ISSUE_COUNT_DB_TABLE_NAME,
        WEEKLY_ISSUE_COUNT_DB_TABLE_NAME,
        TWO_WEEK_ISSUE_COUNT_DB_TABLE_NAME,
        MONTHLY_ISSUE_COUNT_DB_TABLE_NAME,
        TWO_MONTH_ISSUE_COUNT_DB_TABLE_NAME,
        THREE_MONTH_ISSUE_COUNT_DB_TABLE_NAME,
        SIX_MONTH_ISSUE_COUNT_DB_TABLE_NAME,
        ANNUAL_ISSUE_COUNT_DB_TABLE_NAME,
    ],
    defaults=[None, None, None, None, None, None, None, None],
)

INTERVAL_PAIRS: List[Tuple[str, str]] = [
    (DAILY_ISSUE_COUNT_DB_TABLE_NAME, "D"),
    (WEEKLY_ISSUE_COUNT_DB_TABLE_NAME, "W"),
    (TWO_WEEK_ISSUE_COUNT_DB_TABLE_NAME, "2W"),
    (MONTHLY_ISSUE_COUNT_DB_TABLE_NAME, "ME"),
    (TWO_MONTH_ISSUE_COUNT_DB_TABLE_NAME, "2ME"),
    (THREE_MONTH_ISSUE_COUNT_DB_TABLE_NAME, "QE"),
    (SIX_MONTH_ISSUE_COUNT_DB_TABLE_NAME, "2QE"),
    (ANNUAL_ISSUE_COUNT_DB_TABLE_NAME, "YE"),
]
