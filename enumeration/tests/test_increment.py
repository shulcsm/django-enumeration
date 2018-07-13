import datetime

from django.test import TestCase

from enumeration.const import ResetPeriod
from enumeration.models import Sequence, Counter
from enumeration.manager import increment


class IncrementTestCase(TestCase):
    def test_never(self):
        s = Sequence.objects.create(format='#', reset_period=ResetPeriod.NEVER)
        self.assertEqual(increment(s), 1)
        # created
        c = Counter.objects.get(sequence=s, position=1, period=None)

        # updated
        self.assertEqual(increment(s), 2)
        self.assertTrue(Counter.objects.get(sequence=s, position=2, period=None, pk=c.pk))

    def test_daily_counter_created(self):
        s = Sequence.objects.create(format='#', reset_period=ResetPeriod.DAILY)

        d = datetime.date(2012, 1, 14)
        self.assertEqual(increment(s, d), 1)
        # created
        c = Counter.objects.get(sequence=s, position=1, period=d)

        # updated
        self.assertEqual(increment(s, d), 2)
        self.assertTrue(Counter.objects.get(sequence=s, position=2, period=d, pk=c.pk))

        d = datetime.date(2012, 1, 15)
        self.assertEqual(increment(s, d), 1)
        # new created
        Counter.objects.get(sequence=s, position=1, period=d)

    def test_monthly_counter_created(self):
        s = Sequence.objects.create(format='#', reset_period=ResetPeriod.MONTHLY)

        m = datetime.date(2012, 1, 1)
        self.assertEqual(increment(s, datetime.date(2012, 1, 14)), 1)
        # created
        c = Counter.objects.get(sequence=s, position=1, period=m)

        # updated
        self.assertEqual(increment(s, datetime.date(2012, 1, 14)), 2)
        self.assertTrue(Counter.objects.get(sequence=s, position=2, period=m, pk=c.pk))

        # next day, same month incremented
        next_d = datetime.date(2012, 1, 15)
        self.assertEqual(increment(s, next_d), 3)
        self.assertTrue(Counter.objects.get(sequence=s, position=3, period=m, pk=c.pk))

        self.assertEqual(increment(s, datetime.date(2012, 2, 1)), 1)
        # new created
        Counter.objects.get(sequence=s, position=1, period=datetime.date(2012, 2, 1))

    def test_yearly_counter_created(self):
        s = Sequence.objects.create(format='#', reset_period=ResetPeriod.YEARLY)

        y = datetime.date(2012, 1, 1)
        self.assertEqual(increment(s, datetime.date(2012, 1, 14)), 1)
        # created
        c = Counter.objects.get(sequence=s, position=1, period=y)

        # updated
        self.assertEqual(increment(s, datetime.date(2012, 1, 14)), 2)
        self.assertTrue(Counter.objects.get(sequence=s, position=2, period=y, pk=c.pk))

        # next month, same year incremented
        next_m = datetime.date(2012, 2, 14)
        self.assertEqual(increment(s, next_m), 3)
        self.assertTrue(Counter.objects.get(sequence=s, position=3, period=y, pk=c.pk))

        self.assertEqual(increment(s, datetime.date(2013, 2, 1)), 1)
        # new created
        Counter.objects.get(sequence=s, position=1, period=datetime.date(2013, 1, 1))
