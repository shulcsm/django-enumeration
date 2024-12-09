from django.db import models
from typing import Dict, TYPE_CHECKING
from enumeration.manager import get_number, format_number, ResetPeriod, truncate_date

if TYPE_CHECKING:
    from enumeration.models import Sequence


class EnumeratedModelMixin(models.Model):
    sequence = models.ForeignKey(
        "enumeration.Sequence", null=True, on_delete=models.PROTECT
    )

    number = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    position = models.PositiveIntegerField(null=True)
    counter = models.ForeignKey(
        "enumeration.Counter", null=True, on_delete=models.PROTECT
    )

    def get_sequence(self) -> "Sequence":
        raise NotImplementedError

    def get_enumeration_context(self) -> Dict:
        return {}

    def assign_number(self):
        if self.number:
            raise RuntimeError("Number present")

        if not self.sequence:
            self.sequence = self.get_sequence()

        self.number, self.position, self.counter_id = get_number(
            sequence=self.sequence, **self.get_enumeration_context()
        )

    def reassign_number(self):
        assert self.sequence and self.position and self.counter
        ctx = self.get_enumeration_context()

        # Sequecne never resets
        if self.sequence.reset_period == ResetPeriod.NEVER:
            # And correct counter
            if self.counter.period is None:
                self.number = format_number(
                    self.sequence.format,
                    position=self.position,
                    **ctx,
                )
                return
        # sequnce resets
        else:
            # and correct counter period
            if self.counter.period == truncate_date(
                self.sequence.reset_period, ctx["date"]
            ):
                self.number = format_number(
                    self.sequence.format,
                    position=self.position,
                    **ctx,
                )
                return

        # get new number
        self.number, self.position, self.counter_id = get_number(
            sequence=self.sequence, **ctx
        )

    class Meta:
        abstract = True
