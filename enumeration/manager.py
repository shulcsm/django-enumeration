import datetime
from typing import Optional, Tuple

from django.db import connection

from enumeration.const import ResetPeriod
from enumeration.models import Sequence
from .formatter import format_number


class EnumerationError(RuntimeError):
    pass


PERIOD_CRITERIA = "AND c.period = %s"

NEXT_QUERY = """
SELECT
  COALESCE("gap", "c"."position" + 1, 1) AS "position"
FROM enumeration_sequence s
LEFT JOIN enumeration_counter c
  ON c.sequence_id = s.id {}
LEFT JOIN LATERAL (
    SELECT
      "eg"."position" AS gap
    FROM enumeration_gap eg
    WHERE "eg"."counter_id" = c.id
    ORDER BY "eg"."position" ASC
    LIMIT 1) g ON true
WHERE s.id = %s;
"""


def truncate_date(period: ResetPeriod, date: datetime.date):
    if period == ResetPeriod.MONTHLY:
        return date.replace(day=1)

    if period == ResetPeriod.YEARLY:
        return date.replace(month=1, day=1)

    return date


def get_next_position(sequence: Sequence, date: Optional[datetime.date] = None) -> int:
    never = sequence.reset_period == ResetPeriod.NEVER

    args = [sequence.pk]

    if never:
        query = NEXT_QUERY.format("")

    elif date:
        query = NEXT_QUERY.format(PERIOD_CRITERIA)
        args = [truncate_date(sequence.reset_period, date)] + args
    else:
        raise EnumerationError("Missing date")

    with connection.cursor() as cursor:
        cursor.execute(query, args)
        row = cursor.fetchone()

    return row[0]


CONSUME_GAP_QUERY = """
DELETE FROM
    enumeration_gap
WHERE id = (
    SELECT
        g.id
    FROM enumeration_gap g
    INNER JOIN enumeration_counter c
        ON c.id = g.counter_id {}
    WHERE c.sequence_id = %s
    ORDER BY g."position" ASC LIMIT 1
) RETURNING "position";
"""


def consume_gap(sequence: Sequence, date: Optional[datetime.date] = None) -> Optional[int]:
    never = sequence.reset_period == ResetPeriod.NEVER

    args = [sequence.pk]

    if never:
        query = CONSUME_GAP_QUERY.format("")

    elif date:
        query = CONSUME_GAP_QUERY.format(PERIOD_CRITERIA)
        args = [truncate_date(sequence.reset_period, date)] + args

    else:
        raise EnumerationError("Missing date")

    with connection.cursor() as cursor:
        cursor.execute(query, args)
        row = cursor.fetchone()

    if row:
        return row[0]

    return None


def increment(sequence: Sequence, date: Optional[datetime.date] = None) -> int:
    never = sequence.reset_period == ResetPeriod.NEVER

    if never:
        query = """
         INSERT INTO enumeration_counter (sequence_id, "position") VALUES (%s, 1)
         ON CONFLICT (sequence_id) WHERE period IS NULL
         DO UPDATE SET "position" = enumeration_counter."position" + 1 RETURNING "position";
        """
        args = [sequence.pk]

    elif date:
        query = """
         INSERT INTO enumeration_counter (sequence_id, "position", period) VALUES (%s, 1, %s)
         ON CONFLICT (sequence_id, period)
         DO UPDATE SET "position" = enumeration_counter."position" + 1 RETURNING "position";
        """
        args = [sequence.pk, truncate_date(sequence.reset_period, date)]

    else:
        raise EnumerationError("Missing date")

    with connection.cursor() as cursor:
        cursor.execute(query, args)
        row = cursor.fetchone()

    return row[0]


# @TODO testcase
def get_number(sequence: Sequence, fill_gap=True, **context) -> Tuple[str, int]:
    date = context.get('date', None)
    if fill_gap:
        gap_pos = consume_gap(sequence, date)
        if gap_pos is not None:
            return format_number(sequence.format, position=gap_pos, **context), gap_pos

    pos = increment(sequence, date)
    return format_number(sequence.format, position=pos, **context), pos
