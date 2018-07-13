from enum import Enum


class ResetPeriod(Enum):
    NEVER = 'never'
    DAILY = 'daily'
    MONTHLY = 'monthly'
    YEARLY = 'yearly'
