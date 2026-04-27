import random
import string

from flask import session
from markupsafe import Markup


CAPTCHA_LENGTH = 5
CAPTCHA_CHARS = string.ascii_uppercase + string.digits
COLORS = ('#78bbff', '#f7a0fc', '#9a4afc', '#bf2a9a', '#f35afb')


def _new_code():
    return ''.join(random.choices(CAPTCHA_CHARS, k=CAPTCHA_LENGTH))


def generate():
    code = _new_code()
    session['captcha_answer'] = code
    return _render_svg(code)


def check(value):
    expected = session.pop('captcha_answer', None)
    if not expected or not value:
        return False
    return expected.upper() == str(value).strip().upper()


def _render_svg(code):
    width, height = 180, 60
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" class="blog-captcha-img">'
        f'<rect width="100%" height="100%" fill="#0f0f1a"/>'
    ]
    for _ in range(6):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{random.choice(COLORS)}33" stroke-width="1"/>'
        )
    step = width // (CAPTCHA_LENGTH + 1)
    for i, ch in enumerate(code, start=1):
        x = step * i + random.randint(-4, 4)
        y = height // 2 + 12 + random.randint(-4, 4)
        rotate = random.randint(-25, 25)
        parts.append(
            f'<text x="{x}" y="{y}" fill="{random.choice(COLORS)}" '
            f'font-family="monospace" font-size="28" font-weight="bold" '
            f'transform="rotate({rotate} {x} {y})">{ch}</text>'
        )
    parts.append('</svg>')
    return Markup(''.join(parts))
