import re


TOKENS = {
    'LITERAL':  r'{{.*?}}',
    'CONTEXT':  r'{\w+}',
    'POSITION': r'#{1,10}',
    'YEAR':     r'Y{2,4}',
    'MONTH':    r'M{1,2}',
    'DAY':      r'D{1,2}',
    'CHAR':     r'[\x00-\x7F]',
    'WS':       r'\s+',
}

TOKEN_RE = re.compile('|'.join('(?P<%s>%s)' % pair for pair in TOKENS.items()))


def format_number(format_string: str, position: int, **context) -> str:
    parts = []

    for match in TOKEN_RE.finditer(format_string):
        token = match.lastgroup
        assert token

        value = match.group(token)

        if token in ['CHAR', 'WS']:
            parts.append(value)

        elif token == 'POSITION':
            parts.append(str(position).rjust(len(value), '0'))

        elif token == 'YEAR':
            parts.append(str(context['date'].year)[-len(value):])

        elif token == 'MONTH':
            parts.append(str(context['date'].month).rjust(len(value), '0'))

        elif token == 'DAY':
            parts.append(str(context['date'].day).rjust(len(value), '0'))

        elif token == 'LITERAL':
            parts.append(value.strip('{}'))

        elif token == 'CONTEXT':
            parts.append(context[value.strip('{}')])

    return "".join(parts)
