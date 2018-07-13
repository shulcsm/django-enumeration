import datetime

from django.test import TestCase

from enumeration.const import ResetPeriod
from enumeration.models import Sequence, Counter, Gap
from enumeration.manager import get_next_position, EnumerationError


class GetNextTestCase(TestCase):
    def test_no_reset(self):
        s = Sequence.objects.create(format='#', reset_period=ResetPeriod.NEVER)
        self.assertEqual(get_next_position(s), 1, "New sequence")

        c = Counter.objects.create(sequence=s, position=5)
        self.assertEqual(get_next_position(s), 6, "Counter position")

        Gap.objects.create(counter=c, position=3)
        self.assertEqual(get_next_position(s), 3, "Gap position")

    def test_daily_reset(self):
        s = Sequence.objects.create(format='#', reset_period=ResetPeriod.DAILY)

        # Date required
        with self.assertRaises(EnumerationError):
            get_next_position(s)

        d = datetime.date(2012, 1, 14)
        self.assertEqual(get_next_position(s, d), 1, "New sequence")

        c = Counter.objects.create(sequence=s, period=d, position=5)
        self.assertEqual(get_next_position(s, d), 6, "Counter position")

        Gap.objects.create(counter=c, position=3)
        self.assertEqual(get_next_position(s, d), 3, "Gap position")

        next_day = datetime.date(2012, 1, 15)
        self.assertEqual(get_next_position(s, next_day), 1, "New sequence")

        c = Counter.objects.create(sequence=s, period=next_day, position=5)
        self.assertEqual(get_next_position(s, next_day), 6, "Counter position")

        Gap.objects.create(counter=c, position=2)
        self.assertEqual(get_next_position(s, next_day), 2, "Gap position")

        # Yesterday doesn't change
        self.assertEqual(get_next_position(s, d), 3, "Gap position")

    def test_monthly_reset(self):
        s = Sequence.objects.create(format='#', reset_period=ResetPeriod.MONTHLY)

        # Date required
        with self.assertRaises(EnumerationError):
            get_next_position(s)

        d = datetime.date(2012, 1, 14)
        self.assertEqual(get_next_position(s, d), 1, "New sequence")

        c = Counter.objects.create(sequence=s, period=datetime.date(2012, 1, 1), position=5)
        self.assertEqual(get_next_position(s, d), 6, "Counter position")

        Gap.objects.create(counter=c, position=3)
        self.assertEqual(get_next_position(s, d), 3, "Gap position")

        next_day = datetime.date(2012, 1, 15)
        self.assertEqual(get_next_position(s, next_day), 3, "Same sequence")

        next_month = datetime.date(2012, 2, 1)
        self.assertEqual(get_next_position(s, next_month), 1, "New sequence")

        c = Counter.objects.create(sequence=s, period=datetime.date(2012, 2, 1), position=5)
        self.assertEqual(get_next_position(s, next_month), 6, "Counter position")

        Gap.objects.create(counter=c, position=3)
        self.assertEqual(get_next_position(s, next_month), 3, "Gap position")

    def test_yearly_reset(self):
        s = Sequence.objects.create(format='#', reset_period=ResetPeriod.YEARLY)

        # Date required
        with self.assertRaises(EnumerationError):
            get_next_position(s)

        d = datetime.date(2012, 1, 14)
        self.assertEqual(get_next_position(s, d), 1, "New sequence")

        c = Counter.objects.create(sequence=s, period=datetime.date(2012, 1, 1), position=5)
        self.assertEqual(get_next_position(s, d), 6, "Counter position")

        Gap.objects.create(counter=c, position=3)
        self.assertEqual(get_next_position(s, d), 3, "Gap position")

        next_day = datetime.date(2012, 1, 15)
        self.assertEqual(get_next_position(s, next_day), 3, "Same sequence")

        next_month = datetime.date(2012, 2, 1)
        self.assertEqual(get_next_position(s, next_month), 3, "Same sequence")

        next_year = datetime.date(2013, 2, 2)
        c = Counter.objects.create(sequence=s, period=datetime.date(2013, 1, 1), position=5)
        self.assertEqual(get_next_position(s, next_year), 6, "Counter position")

        Gap.objects.create(counter=c, position=3)
        self.assertEqual(get_next_position(s, next_year), 3, "Gap position")
