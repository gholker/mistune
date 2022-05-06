import re
try:
    from urllib.parse import quote
    import html
except ImportError:
    from urllib import quote
    html = None


PREVENT_BACKSLASH = r'(?<!\\)(?:\\\\)*'

PUNCTUATION = r'''\\!"#$%&'()*+,./:;<=>?@\[\]^`{}|_~-'''
ESCAPE_CHAR_RE = re.compile(r'\\([' + PUNCTUATION + r'])')

LINK_LABEL = r'\[(?:[^\\\[\]]|\\.){0,500}\]'

# regex copied from commonmark.js
LINK_TITLE_RE = re.compile(
    r'(?:'
    r'"(?:\\[' + PUNCTUATION + ']|[^"\x00])*"|'  # "title"
    r"'(?:\\[" + PUNCTUATION + "]|[^'\x00])*'|"  # 'title'
    r'\((?:\\[' + PUNCTUATION + ']|[^()\x00])*"'  # (title)
    r')'
)
LINK_BRACKET_RE = re.compile(r'<(?:[^<>\n\\\x00]|\\.)*>')

HTML_TAGNAME = r'[A-Za-z][A-Za-z0-9-]*'
HTML_ATTRIBUTES = (
    r'(?:\s+[A-Za-z_:][A-Za-z0-9_.:-]*'
    r'(?:\s*=\s*(?:[^ "\'=<>`]+|\'[^\']*?\'|"[^\"]*?"))?)*'
)


def escape(s, quote=True):
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
    return s


def escape_url(link):
    safe = (
        ':/?#@'           # gen-delims - '[]' (rfc3986)
        '!$&()*+,;='      # sub-delims - "'" (rfc3986)
        '%'               # leave already-encoded octets alone
    )

    if html is None:
        return quote(link.encode('utf-8'), safe=safe)
    return html.escape(quote(html.unescape(link), safe=safe))


def escape_html(s):
    if html is not None:
        return html.escape(html.unescape(s)).replace('&#x27;', "'")
    return escape(s)


def unikey(s):
    return ' '.join(s.split()).lower()
