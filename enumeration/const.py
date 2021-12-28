from django.db import models


class ResetPeriod(models.TextChoices):
    NEVER = "never"
    DAILY = "daily"
    MONTHLY = "monthly"
    YEARLY = "yearly"
