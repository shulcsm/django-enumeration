import datetime

from django.test import TestCase

from enumeration.const import ResetPeriod
from enumeration.manager import increment
from enumeration.models import Counter
from enumeration.models import Sequence


class IncrementTestCase(TestCase):
    def test_never(self):
        s = Sequence.objects.create(format="#", reset_period=ResetPeriod.NEVER)
        res = increment(s)
        assert res.position == 1
        # created
        c = Counter.objects.get(sequence=s, position=1, period=None)
        assert res.counter_id == c.pk

        # updated
        res = increment(s)
        assert res.position == 2
        c = Counter.objects.get(sequence=s, position=2, period=None, pk=c.pk)
        assert res.counter_id == c.pk

    def test_daily_counter_created(self):
        s = Sequence.objects.create(format="#", reset_period=ResetPeriod.DAILY)

        d = datetime.date(2012, 1, 14)
        res = increment(s, d)
        self.assertEqual(res.position, 1)
        # created
        c = Counter.objects.get(sequence=s, position=1, period=d)
        assert c.pk == res.counter_id

        # updated
        self.assertEqual(increment(s, d), (2, c.pk))
        self.assertTrue(Counter.objects.get(sequence=s, position=2, period=d, pk=c.pk))

        d = datetime.date(2012, 1, 15)

        res = increment(s, d)
        self.assertEqual(res.position, 1)
        # new created
        c = Counter.objects.get(sequence=s, position=1, period=d)
        assert c.pk == res.counter_id

    def test_monthly_counter_created(self):
        s = Sequence.objects.create(format="#", reset_period=ResetPeriod.MONTHLY)

        m = datetime.date(2012, 1, 1)
        res = increment(s, datetime.date(2012, 1, 14))
        assert res.position == 1
        # created
        c = Counter.objects.get(sequence=s, position=1, period=m)
        assert res.counter_id == c.pk

        # updated
        res = increment(s, datetime.date(2012, 1, 14))
        self.assertEqual(res.position, 2)
        c = Counter.objects.get(sequence=s, position=2, period=m, pk=c.pk)
        assert res.counter_id == c.pk

        # next day, same month incremented
        next_d = datetime.date(2012, 1, 15)
        res = increment(s, next_d)
        self.assertEqual(res.position, 3)
        c = Counter.objects.get(sequence=s, position=3, period=m, pk=c.pk)
        assert res.counter_id == c.pk

        res = increment(s, datetime.date(2012, 2, 1))
        self.assertEqual(res.position, 1)
        # new created
        c = Counter.objects.get(
            sequence=s, position=1, period=datetime.date(2012, 2, 1)
        )
        assert res.counter_id == c.pk

    def test_yearly_counter_created(self):
        s = Sequence.objects.create(format="#", reset_period=ResetPeriod.YEARLY)

        y = datetime.date(2012, 1, 1)
        res = increment(s, datetime.date(2012, 1, 14))
        assert res.position == 1
        # created
        c = Counter.objects.get(sequence=s, position=1, period=y)
        assert res.counter_id == c.pk

        # updated
        res = increment(s, datetime.date(2012, 1, 14))
        assert res.position == 2
        c = Counter.objects.get(sequence=s, position=2, period=y, pk=c.pk)
        assert res.counter_id == c.pk

        # next month, same year incremented
        next_m = datetime.date(2012, 2, 14)
        res = increment(s, next_m)
        assert res.position == 3
        c = Counter.objects.get(sequence=s, position=3, period=y, pk=c.pk)
        assert res.counter_id == c.pk

        res = increment(s, datetime.date(2013, 2, 1))
        assert res.position == 1
        # new created
        c = Counter.objects.get(
            sequence=s, position=1, period=datetime.date(2013, 1, 1)
        )
        assert res.counter_id == c.pk
