import re
from django.core.exceptions import ValidationError

from enumeration.const import ResetPeriod
from enumeration.formatter import POSITION, YEAR, MONTH, DAY


def validate_format(format_string, period: ResetPeriod):
    if not re.search(POSITION, format_string):
        raise ValidationError("Number placeholder \"#{1,10}\" is required.")

    if period in [ResetPeriod.YEARLY, ResetPeriod.MONTHLY, ResetPeriod.DAILY]:
        if not re.search(YEAR, format_string):
            raise ValidationError(f"Year placeholder \"Y{{2,4}}\" is required for {period.value} period.")

    if period in [ResetPeriod.MONTHLY, ResetPeriod.DAILY]:
        if not re.search(MONTH, format_string):
            raise ValidationError(f"Month placeholder \"M{{1,2}}\" is required for {period.value} period.")

    if period == ResetPeriod.DAILY:
        if not re.search(DAY, format_string):
            raise ValidationError(f"Day placeholder \"D{{1,2}}\" is required for {period.value} period.")
