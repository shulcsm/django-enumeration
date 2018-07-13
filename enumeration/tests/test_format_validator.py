from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from enumeration.const import ResetPeriod
from enumeration.validators import validate_format


class FormatValidatorTestCase(SimpleTestCase):
    def test_number_required(self):
        with self.assertRaises(ValidationError) as ctx:
            validate_format('', ResetPeriod.NEVER)

        self.assertTrue("Number placeholder \"#{1,10}\" is required." in ctx.exception.messages)

        validate_format('##', ResetPeriod.NEVER)
        validate_format('###', ResetPeriod.NEVER)

    def test_year(self):
        with self.assertRaises(ValidationError) as ctx:
            validate_format('#', ResetPeriod.YEARLY)

        self.assertTrue("Year placeholder \"Y{2,4}\" is required for yearly period." in ctx.exception.messages)

        with self.assertRaises(ValidationError) as ctx:
            validate_format('Y#', ResetPeriod.YEARLY)

        validate_format('YY###', ResetPeriod.YEARLY)

    def test_month(self):
        with self.assertRaises(ValidationError) as ctx:
            validate_format('#', ResetPeriod.MONTHLY)

        self.assertTrue("Year placeholder \"Y{2,4}\" is required for monthly period." in ctx.exception.messages)

        with self.assertRaises(ValidationError) as ctx:
            validate_format('YY#', ResetPeriod.MONTHLY)

        self.assertTrue("Month placeholder \"M{1,2}\" is required for monthly period." in ctx.exception.messages)

        validate_format('YYM#', ResetPeriod.YEARLY)
        validate_format('YYM###', ResetPeriod.YEARLY)

    def test_day(self):
        with self.assertRaises(ValidationError) as ctx:
            validate_format('#', ResetPeriod.DAILY)
        self.assertTrue("Year placeholder \"Y{2,4}\" is required for daily period." in ctx.exception.messages)

        with self.assertRaises(ValidationError) as ctx:
            validate_format('YY#', ResetPeriod.DAILY)
        self.assertTrue("Month placeholder \"M{1,2}\" is required for daily period." in ctx.exception.messages)

        with self.assertRaises(ValidationError) as ctx:
            validate_format('YYM#', ResetPeriod.DAILY)
        self.assertTrue("Day placeholder \"D{1,2}\" is required for daily period." in ctx.exception.messages)

        validate_format('YYMD#', ResetPeriod.YEARLY)
        validate_format('YYYYMD###', ResetPeriod.YEARLY)
