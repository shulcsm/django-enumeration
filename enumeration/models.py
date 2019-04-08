from django.core.exceptions import ValidationError
from django.db import models
from enumfields import EnumField

from enumeration.const import ResetPeriod
from enumeration.validators import validate_format


class Sequence(models.Model):
    format = models.CharField(max_length=255)
    reset_period = EnumField(ResetPeriod, max_length=30, default=ResetPeriod.NEVER)

    def clean(self):
        try:
            validate_format(self.format, self.reset_period)

        except ValidationError as e:
            raise ValidationError({"format": e.messages})


class Counter(models.Model):
    sequence = models.ForeignKey(
        Sequence, related_name="counters", on_delete=models.CASCADE
    )
    position = models.PositiveIntegerField(default=0)
    period = models.DateField(null=True)

    class Meta:
        unique_together = ("sequence", "period")
        constraints = [
            # only one counter for period-naive sequences
            models.UniqueConstraint(
                fields=["sequence"],
                condition=models.Q(period__isnull=True),
                name="unique_counter_for_no_period",
            )
        ]


class Gap(models.Model):
    counter = models.ForeignKey(Counter, related_name="gaps", on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    unique_together = ("counter", "position")


# class EnumeratedDocumentMixin(models.Model):
#     sequence = models.ForeignKey(Sequence)
#     position = models.PositiveIntegerField(null=True)
#     number = models.CharField(max_length=255, null=True, blank=True)
#
#     class Meta:
#         abstract = True
