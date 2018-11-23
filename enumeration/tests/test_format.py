from datetime import date
from django.test import SimpleTestCase
from enumeration.formatter import format_number


class FormatTestCase(SimpleTestCase):
    def test(self):
        self.assertEqual(format_number("#", position=1), '1')
        self.assertEqual(format_number("#", position=11), '11')
        self.assertEqual(format_number("##", position=1), '01')

        d = date(2017, 3, 11)

        self.assertEqual(format_number("#YY", position=1, date=d), '117')
        self.assertEqual(format_number("YY#", position=11, date=d), '1711')
        self.assertEqual(format_number("##YY", position=1, date=d), '0117')
        self.assertEqual(format_number("##YYYY", position=1, date=d), '012017')
        self.assertEqual(format_number("#YYMD", position=1, date=d), '117311')
        self.assertEqual(
            format_number("# {one} YY {two} M D", position=1, date=d, one='foo', two='bar'),
            '1 foo 17 bar 3 11'
        )

    def test_ascii(self):
        d = date(2017, 3, 11)
        self.assertEqual(format_number("YYA#B", position=1, date=d), '17A1B')
        self.assertEqual(format_number("YY#Ā⅜£B", position=1, date=d), '171B')

    def test_literal(self):
        d = date(2017, 3, 11)
        self.assertEqual(
            format_number(r"{{#YYYYMD}} #YYYYMD", position=1, date=d), r"#YYYYMD 12017311"
        )
