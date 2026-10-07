#!/usr/bin/env python3
"""Rebuild self-contained dark fantasy SVGs using the Python standard library."""
import base64
from pathlib import Path
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parents[1] / 'assets'


def data_uri(name, mime):
    return f'data:{mime};base64,' + base64.b64encode((ASSETS / name).read_bytes()).decode()


def svg(width, height, title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title>
{body}
</svg>\n'''


def text(x, y, value, size=20, color='#dce8f0', extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" {extra}>{escape(value)}</text>'


def hero(mobile=False):
    w, h = (640, 800) if mobile else (1280, 540)
    bg = data_uri('background.jpg', 'image/jpeg')
    photo = data_uri('profile.png', 'image/png')
    px, py, pw, ph = (24, 310, 592, 466) if mobile else (42, 42, 618, 456)
    ax, ay = (86, 378) if mobile else (108, 112)
    body = f'''<defs>
<clipPath id="outer"><rect width="{w}" height="{h}" rx="20"/></clipPath>
<clipPath id="avatar"><circle cx="{ax}" cy="{ay}" r="35"/></clipPath>
<linearGradient id="shade" x2="0" y2="1"><stop stop-color="#080e16" stop-opacity=".03"/><stop offset="1" stop-color="#080e16" stop-opacity=".64"/></linearGradient>
<linearGradient id="glass" x2="1" y2="1"><stop stop-color="#20303e" stop-opacity=".8"/><stop offset="1" stop-color="#0b141e" stop-opacity=".88"/></linearGradient>
<linearGradient id="edge" x2="1" y2="1"><stop stop-color="#b3cddd" stop-opacity=".5"/><stop offset=".5" stop-color="#91b1c5" stop-opacity=".12"/><stop offset="1" stop-color="#b3cddd" stop-opacity=".3"/></linearGradient>
</defs>
<g clip-path="url(#outer)">
<rect width="{w}" height="{h}" fill="#080e16"/>
<image xlink:href="{bg}" width="{w}" height="{510 if mobile else h}" preserveAspectRatio="{'xMaxYMid' if mobile else 'xMidYMid'} slice"/>
<rect width="{w}" height="{h}" fill="url(#shade)"/>
<rect x="{px}" y="{py + 8}" width="{pw}" height="{ph}" rx="18" fill="#000" opacity=".22"/>
<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="18" fill="url(#glass)" stroke="url(#edge)"/>
<path d="M {px+26} {py} H {px+112}" stroke="#c2d8e5" stroke-opacity=".8"/>
<circle cx="{ax}" cy="{ay}" r="43" fill="#b8d9ea" fill-opacity=".04" stroke="#b8d9ea" stroke-opacity=".26"/>
<circle cx="{ax}" cy="{ay}" r="37" fill="#12212e" stroke="#c5dce9" stroke-opacity=".45"/>
<image xlink:href="{photo}" x="{ax-35}" y="{ay-35}" width="70" height="70" clip-path="url(#avatar)"/>
<circle cx="{ax+29}" cy="{ay+29}" r="7" fill="#b7dce9" stroke="#15222e" stroke-width="3"/>
'''
    if mobile:
        body += text(150, 371, 'DEVELOPER PROFILE', 16, '#a5bdcc', 'letter-spacing="3"')
        body += text(150, 401, 'SELLEBEWW / INDONESIA', 17, '#dce8f0', 'letter-spacing="1.5"')
        body += text(58, 467, "HELLO, I'M", 17, '#a5bdcc', 'letter-spacing="4"')
        body += '<text x="54" y="537" fill="#edf3f7" font-family="Georgia, Times New Roman, serif" font-size="62">Vassel Goleyu</text>'
        body += text(58, 587, 'Software engineer. Curious builder.', 24)
        body += text(58, 628, 'Web · Applied AI · Thoughtful interfaces', 22, '#b1c5d3')
        body += '<path d="M58 662H582" stroke="#a6c3d5" stroke-opacity=".2"/>'
        body += '<circle cx="65" cy="704" r="4" fill="#c5e4f0"/>'
        body += text(83, 711, 'BUILDING SOMETHING', 17, '#c5e4f0', 'letter-spacing="2"')
        body += text(58, 745, 'Ideas into systems. Details into experiences.', 19, '#9db5c6')
    else:
        body += text(169, 106, 'DEVELOPER PROFILE', 13, '#a5bdcc', 'letter-spacing="3"')
        body += text(169, 134, 'SELLEBEWW / INDONESIA', 14, '#dce8f0', 'letter-spacing="2"')
        body += text(80, 208, "HELLO, I'M", 14, '#a5bdcc', 'letter-spacing="4"')
        body += '<text x="76" y="278" fill="#edf3f7" font-family="Georgia, Times New Roman, serif" font-size="60">Vassel Goleyu</text>'
        body += text(80, 324, 'Software engineer. Curious builder.', 23)
        body += text(80, 360, 'Web · Applied AI · Thoughtful interfaces', 19, '#b1c5d3')
        body += '<path d="M80 396H620" stroke="#a6c3d5" stroke-opacity=".2"/>'
        body += '<circle cx="86" cy="434" r="3" fill="#c5e4f0"/>'
        body += text(100, 439, 'BUILDING SOMETHING', 12, '#c5e4f0', 'letter-spacing="2"')
        body += text(80, 470, 'Ideas into systems. Details into experiences.', 15, '#9db5c6')
        body += text(1228, 502, 'STILL BUILDING / STILL EXPLORING', 11, '#bfd0dc', 'text-anchor="end" letter-spacing="2"')
    body += f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="20" fill="none" stroke="#8aabbe" stroke-opacity=".28"/></g>'
    return svg(w, h, 'Vassel Goleyu — software engineer, web and applied AI. An original frost-lit dragon watches behind a glass profile panel.', body)


def main():
    for mobile in (False, True):
        (ASSETS / ('hero-mobile.svg' if mobile else 'hero.svg')).write_text(hero(mobile))
    divider = '''<defs><linearGradient id="line"><stop stop-color="#90b7ce" stop-opacity="0"/><stop offset=".5" stop-color="#90b7ce" stop-opacity=".65"/><stop offset="1" stop-color="#90b7ce" stop-opacity="0"/></linearGradient></defs>
<style>.glow{animation:breathe 8s ease-in-out infinite}@keyframes breathe{0%,100%{opacity:.35}50%{opacity:.9}}@media(prefers-reduced-motion:reduce){.glow{animation:none;opacity:.6}}</style>
<path d="M0 20H610M670 20H1280" stroke="url(#line)"/>
<path d="M640 14L646 20L640 26L634 20Z" fill="#91b9cf" fill-opacity=".5"/>
<circle class="glow" cx="640" cy="20" r="13" fill="#91b9cf" fill-opacity=".1"/>'''
    (ASSETS / 'divider.svg').write_text(svg(1280, 40, '', divider))
    footer = f'''<defs><clipPath id="crop"><rect width="1280" height="150" rx="12"/></clipPath><linearGradient id="fade"><stop stop-color="#080e16"/><stop offset="1" stop-color="#080e16" stop-opacity=".25"/></linearGradient></defs>
<g clip-path="url(#crop)"><rect width="1280" height="150" fill="#080e16"/>
<image xlink:href="{data_uri('background.jpg', 'image/jpeg')}" width="1280" height="457" y="-105"/>
<rect width="1280" height="150" fill="url(#fade)"/>
<path d="M40 35V115M40 75H105" stroke="#a9cddd" stroke-opacity=".5"/>
{text(130, 71, 'THE NEXT CHAPTER IS STILL BEING WRITTEN.', 20, '#d7e6ef', 'letter-spacing="3"')}
{text(130, 104, 'One idea. One experiment. One commit at a time.', 16, '#acc2d1')}
</g>'''
    (ASSETS / 'footer.svg').write_text(svg(1280, 150, 'The next chapter is still being written. One idea. One experiment. One commit at a time.', footer))
    mobile_footer = f'''<defs><clipPath id="crop"><rect width="640" height="200" rx="12"/></clipPath></defs>
<g clip-path="url(#crop)"><rect width="640" height="200" fill="#080e16"/>
<image xlink:href="{data_uri('background.jpg', 'image/jpeg')}" width="640" height="229" y="-20"/>
<rect width="640" height="200" fill="#080e16" fill-opacity=".74"/>
<path d="M30 40V160" stroke="#a9cddd" stroke-opacity=".5"/>
{text(52, 76, 'THE NEXT CHAPTER', 24, '#d7e6ef', 'letter-spacing="2"')}
{text(52, 111, 'IS STILL BEING WRITTEN.', 24, '#d7e6ef', 'letter-spacing="2"')}
{text(52, 154, 'One idea. One experiment. One commit at a time.', 20, '#acc2d1')}
</g>'''
    (ASSETS / 'footer-mobile.svg').write_text(svg(640, 200, 'The next chapter is still being written.', mobile_footer))
    print('Generated desktop/mobile hero, divider, and desktop/mobile footer SVGs')


if __name__ == '__main__':
    main()
