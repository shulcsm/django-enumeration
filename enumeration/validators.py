import re
from django.core.exceptions import ValidationError

from enumeration.const import ResetPeriod
from enumeration.formatter import TOKENS

POSITION = re.compile(TOKENS['POSITION'])
YEAR = re.compile(TOKENS['YEAR'])
MONTH = re.compile(TOKENS['MONTH'])
DAY = re.compile(TOKENS['DAY'])


def validate_format(format_string, period: ResetPeriod):
    if not POSITION.search(format_string):
        raise ValidationError("Number placeholder \"#{1,10}\" is required.")

    if period in [ResetPeriod.YEARLY, ResetPeriod.MONTHLY, ResetPeriod.DAILY]:
        if not YEAR.search(format_string):
            raise ValidationError(f"Year placeholder \"Y{{2,4}}\" is required for {period.value} period.")

    if period in [ResetPeriod.MONTHLY, ResetPeriod.DAILY]:
        if not MONTH.search(format_string):
            raise ValidationError(f"Month placeholder \"M{{1,2}}\" is required for {period.value} period.")

    if period == ResetPeriod.DAILY:
        if not DAY.search(format_string):
            raise ValidationError(f"Day placeholder \"D{{1,2}}\" is required for {period.value} period.")
