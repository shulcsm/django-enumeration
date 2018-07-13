from typing import Match, Tuple, Pattern, Callable
import re
import datetime

POSITION = re.compile(r'#{1,10}')
YEAR = re.compile(r'Y{2,4}')
MONTH = re.compile(r'M{1,2}')
DAY = re.compile(r'D{1,2}')
CONTEXT = re.compile(r'{(\w+)}')


def _position(match: Match, position: int, **_context) -> str:
    return str(position).rjust(len(match.group()), '0')


def _year(match: Match, date: datetime.date, **_context) -> str:
    return str(date.year)[-len(match.group()):]


def _month(match: Match, date: datetime.date, **_context) -> str:
    return str(date.month).rjust(len(match.group()), '0')


def _day(match: Match, date: datetime.date, **_context) -> str:
    return str(date.day).rjust(len(match.group()), '0')


def _context(match: Match, **context) -> str:
    return context[match.group(1)]


FORMATTERS: Tuple[Tuple[Pattern, Callable], ...] = (
    (POSITION, _position),
    (YEAR, _year),
    (MONTH, _month),
    (DAY, _day),
    (CONTEXT, _context),
)


def format_number(format_string: str, **context) -> str:
    for pattern, resolve in FORMATTERS:
        for match in pattern.finditer(format_string):
            if match:
                format_string = format_string.replace(
                    match.group(), resolve(match, **context), 1)
    return format_string
