from enumeration.models import Counter
from enumeration.models import Gap
from enumeration.models import Sequence
from enumeration.const import ResetPeriod
from enumeration.manager import get_number
from datetime import date


def test_get_number(db):
    sequence = Sequence.objects.create(
        format="YYMM###{DERP}", reset_period=ResetPeriod.MONTHLY
    )
    res = get_number(sequence, DERP="BAZZ", date=date(2024, 11, 5))
    c = Counter.objects.get(sequence=sequence, period=date(2024, 11, 1))

    assert res.number == "2411001BAZZ"
    assert res.position == 1
    assert res.counter_id == c.pk

    res = get_number(sequence, DERP="BAZZ", date=date(2024, 11, 10))

    assert res.number == "2411002BAZZ"
    assert res.position == 2
    assert res.counter_id == c.pk
