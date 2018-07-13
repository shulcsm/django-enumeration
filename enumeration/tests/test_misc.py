import datetime

from django.db import IntegrityError
from django.test import TestCase

from enumeration.const import ResetPeriod
from enumeration.models import Sequence, Counter


class MiscTestCase(TestCase):
    def test_counter_constraint_same_date(self):
        s = Sequence.objects.create(format='#', reset_period=ResetPeriod.DAILY)
        Counter.objects.create(sequence=s, period=datetime.date(2012, 1, 14))

        with self.assertRaises(IntegrityError):
            Counter.objects.create(sequence=s, period=datetime.date(2012, 1, 14))

    def test_counter_constaint_nod_date(self):
        s = Sequence.objects.create(format='#', reset_period=ResetPeriod.NEVER)
        Counter.objects.create(sequence=s)

        with self.assertRaises(IntegrityError):
            Counter.objects.create(sequence=s)
