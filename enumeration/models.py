from django.core.exceptions import ValidationError
from django.db import models
from enumfields import EnumField
from partial_index import PartialIndex

from enumeration.const import ResetPeriod
from enumeration.validators import validate_format


class Sequence(models.Model):
    format = models.CharField(max_length=255)
    reset_period = EnumField(ResetPeriod, max_length=30, default=ResetPeriod.NEVER)

    def clean(self):
        try:
            validate_format(self.format, self.reset_period)

        except ValidationError as e:
            raise ValidationError({
                "format": e.messages
            })


class Counter(models.Model):
    sequence = models.ForeignKey(Sequence, related_name='counters')
    position = models.PositiveIntegerField(default=0)
    period = models.DateField(null=True)

    class Meta:
        unique_together = (
            ('sequence', 'period',)
        )
        indexes = [
            # only one counter for period-naive sequences
            PartialIndex(fields=['sequence_id'], unique=True, where='period IS NULL'),
        ]


class Gap(models.Model):
    counter = models.ForeignKey(Counter, related_name='gaps')
    position = models.PositiveIntegerField()

    unique_together = (
        ('counter', 'position',)
    )


# class EnumeratedDocumentMixin(models.Model):
#     sequence = models.ForeignKey(Sequence)
#     position = models.PositiveIntegerField(null=True)
#     number = models.CharField(max_length=255, null=True, blank=True)
#
#     class Meta:
#         abstract = True