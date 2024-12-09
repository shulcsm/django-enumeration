import pytest
from datetime import date
from enumeration.models import Sequence, ResetPeriod, Counter
from .models import Document


@pytest.fixture()
def sequence(db):
    return Sequence.objects.create(format="YYMM###", reset_period=ResetPeriod.MONTHLY)


def test_assign_number(sequence):
    d = Document(sequence=sequence, date=date(2024, 11, 5))
    d.assign_number()
    assert d.number == "2411001"
    assert d.position == 1
    assert d.counter == Counter.objects.get(
        sequence=sequence, position=1, period=date(2024, 11, 1)
    )

    # can't assign
    with pytest.raises(RuntimeError):
        d.assign_number()


def test_reassing(sequence):

    i = Document(sequence=sequence, date=date(2024, 11, 5))
    i.assign_number()

    assert i.number == "2411001"
    assert i.position == 1
    assert i.counter == Counter.objects.get(
        sequence=sequence, position=1, period=date(2024, 11, 1)
    )

    # jump day in same month
    i.date = date(2024, 11, 2)
    i.reassign_number()

    assert i.number == "2411001"
    assert i.position == 1
    assert i.counter == Counter.objects.get(
        sequence=sequence, position=1, period=date(2024, 11, 1)
    )

    # move to next month
    i.date = date(2024, 12, 2)
    i.reassign_number()
    assert i.number == "2412001"
    assert i.position == 1
    assert i.counter == Counter.objects.get(
        sequence=sequence, position=1, period=date(2024, 12, 1)
    )

    i = Document(sequence=sequence, date=date(2024, 12, 1))
    i.assign_number()
    assert i.number == "2412002"
    assert i.position == 2
    assert i.counter == Counter.objects.get(
        sequence=sequence, position=2, period=date(2024, 12, 1)
    )
