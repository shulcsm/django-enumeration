import datetime

from django.test import TestCase

from enumeration.const import ResetPeriod
from enumeration.models import Sequence, Counter, Gap
from enumeration.manager import consume_gap


class ConsumeGapTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.s = Sequence.objects.create(format='#', reset_period=ResetPeriod.DAILY)

    def test_no_counter(self):
        d = datetime.date(2012, 1, 14)
        self.assertIsNone(consume_gap(self.s, d))

    def test_has_counter_no_gaps(self):
        d = datetime.date(2012, 1, 14)
        Counter.objects.create(sequence=self.s, period=d, position=5)
        self.assertIsNone(consume_gap(self.s, d))

    def test_gaps_consumed(self):
        d = datetime.date(2012, 1, 14)
        c = Counter.objects.create(sequence=self.s, period=d, position=5)
        Gap.objects.create(counter=c, position=2)
        Gap.objects.create(counter=c, position=3)

        self.assertEqual(consume_gap(self.s, d), 2)
        self.assertFalse(Gap.objects.filter(counter=c, position=2).exists())

        self.assertEqual(consume_gap(self.s, d), 3)
        self.assertFalse(Gap.objects.filter(counter=c, position=3).exists())

    def test_right_counter_consumed(self):
        d = datetime.date(2012, 1, 14)
        c = Counter.objects.create(sequence=self.s, period=d, position=5)
        Gap.objects.create(counter=c, position=2)
        Gap.objects.create(counter=c, position=3)

        d2 = datetime.date(2012, 1, 15)
        c2 = Counter.objects.create(sequence=self.s, period=d2, position=5)
        Gap.objects.create(counter=c2, position=2)
        Gap.objects.create(counter=c2, position=3)

        self.assertEqual(consume_gap(self.s, d2), 2)
        self.assertEqual(c.gaps.count(), 2)
        self.assertEqual(c2.gaps.count(), 1)
