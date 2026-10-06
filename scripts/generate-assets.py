#!/usr/bin/env python3
"""Generate the tiger arcade profile artwork with Python's standard library.

Run: python3 scripts/generate-assets.py
Commit README.md and the generated assets together. Four banners cover mobile,
desktop, light, and dark modes. Every animation respects reduced motion.
Keep badge dimensions in sync with README.md when changing them here.
"""
from pathlib import Path
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parents[1] / "assets"
PALETTES = {
    "light": {
        "bg": "#FFF9F3", "border": "#E5DCEC", "ink": "#302443",
        "muted": "#71647E", "grid": "#CBBADC", "panel": "#EDE2FF",
        "halo": "#FFE6A9", "orbit": "#C7B2EB", "ground": "#E2D9F3",
        "purple": "#7650C4", "pink": "#CF426F", "mint": "#197D73",
        "pill": "#EEE4FF", "bubble": "#FFFFFF",
    },
    "dark": {
        "bg": "#1D1830", "border": "#4C3A68", "ink": "#FFF3E1",
        "muted": "#C3B3D9", "grid": "#735A95", "panel": "#35264F",
        "halo": "#63426B", "orbit": "#8E67BD", "ground": "#392D50",
        "purple": "#BAA0FF", "pink": "#FF8CB4", "mint": "#6EEAD2",
        "pill": "#3A2A55", "bubble": "#392B50",
    },
}
OUTLINE = "#342543"


def svg_open(width, height, title, description):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" role="img" aria-labelledby="title desc">
  <title id="title">{escape(title)}</title>
  <desc id="desc">{escape(description)}</desc>'''


def write_svg(filename, content):
    content = "\n".join(line.rstrip() for line in content.splitlines()) + "\n"
    (ASSETS / filename).write_text(content, encoding="utf-8")


def motion_style(css):
    return f'''<style>
{css}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
  </style>'''


CHARACTER_MOTION = '''
    .body-bob { transform-origin: 231px 278px; animation: breathe 3s ease-in-out infinite; }
    .head-bop { transform-origin: 236px 198px; animation: bop 3s ease-in-out infinite; }
    .ear { transform-origin: 189px 112px; animation: ear 6s ease-in-out infinite; }
    .tail { transform-origin: 279px 244px; animation: tail 3.6s ease-in-out infinite; }
    .shades { transform-origin: 241px 145px; animation: shades 7s ease-in-out infinite; }
    .lens-shine { animation: lens-shine 5s ease-in-out infinite; }
    .typing-paw { animation: typing 1.2s ease-in-out infinite; }
    @keyframes breathe { 0%, 100% { transform: scaleY(1); } 50% { transform: scaleY(1.025); } }
    @keyframes bop { 0%, 100% { transform: rotate(-3deg); } 50% { transform: translateY(3px) rotate(3deg); } }
    @keyframes ear { 0%, 65%, 100% { transform: rotate(0); } 70%, 80% { transform: rotate(-9deg); } 75%, 85% { transform: rotate(5deg); } }
    @keyframes tail { 0%, 100% { transform: rotate(-8deg); } 50% { transform: rotate(10deg); } }
    @keyframes shades { 0%, 55%, 100% { transform: translateY(0) rotate(0); } 65%, 80% { transform: translateY(-5px) rotate(-4deg); } }
    @keyframes lens-shine { 0%, 55%, 100% { transform: translateX(-60px); opacity: 0; } 60% { opacity: .8; } 85% { transform: translateX(110px); opacity: .8; } 90% { opacity: 0; transform: translateX(110px); } }
    @keyframes typing { 0%, 40%, 70%, 100% { transform: translateY(0); } 20%, 55% { transform: translateY(-4px); } }
'''

SCENE_MOTION = '''
    .plant { transform-origin: 64px 221px; animation: sway 4s ease-in-out infinite; }
    .orbit { transform-origin: 237px 139px; animation: orbit 18s linear infinite; }
    .sparkle { transform-box: fill-box; transform-origin: center; animation: twinkle 4s ease-in-out infinite; }
    .sparkle-two { animation-delay: -2s; }
    .float { animation: float 5s ease-in-out infinite; }
    .float-two { animation-delay: -2.5s; }
    .steam { animation: steam 3s ease-out infinite; }
    .steam-two { animation-delay: -1.5s; }
    .screen-glint { animation: screen-shine 6s ease-in-out infinite; }
    .screen-code { animation: code-glow 3s ease-in-out infinite; }
    .status-ring { transform-box: fill-box; transform-origin: center; animation: ping 3s ease-out infinite; }
    .cheer { transform-origin: 358px 87px; animation: cheer 8s ease-in-out infinite; }
    .confetti { transform-box: fill-box; transform-origin: center; animation: confetti 8s ease-out infinite; }
    .status { animation: status 12s steps(1, end) infinite; }
    .status-two { animation-delay: -8s; }
    .status-three { animation-delay: -4s; }
    .accent-stroke { animation: underline 5s ease-in-out infinite; }
    .eq { transform-box: fill-box; transform-origin: bottom; animation: equalizer 1.4s ease-in-out infinite; }
    .eq-two { animation-delay: -.45s; }
    .eq-three { animation-delay: -.9s; }
    @keyframes sway { 0%, 100% { transform: rotate(-4deg); } 50% { transform: rotate(5deg); } }
    @keyframes orbit { to { transform: rotate(360deg); } }
    @keyframes twinkle { 0%, 100% { transform: scale(.65) rotate(-12deg); opacity: .35; } 50% { transform: scale(1.15) rotate(12deg); opacity: 1; } }
    @keyframes float { 0%, 100% { transform: translateY(4px); opacity: .5; } 50% { transform: translateY(-7px); opacity: 1; } }
    @keyframes steam { 0% { transform: translateY(4px); opacity: 0; } 25% { opacity: .65; } 100% { transform: translate(3px, -12px); opacity: 0; } }
    @keyframes screen-shine { 0%, 55% { transform: translateX(-55px); opacity: 0; } 60% { opacity: .2; } 90% { transform: translateX(165px); opacity: .2; } 91%, 100% { transform: translateX(165px); opacity: 0; } }
    @keyframes code-glow { 0%, 100% { opacity: .65; } 50% { opacity: 1; } }
    @keyframes ping { 0% { transform: scale(.75); opacity: .6; } 80%, 100% { transform: scale(2.4); opacity: 0; } }
    @keyframes cheer { 0%, 10%, 95%, 100% { transform: translateY(8px) scale(.85); opacity: 0; } 20%, 80% { transform: translateY(-3px) scale(1); opacity: 1; } 50% { transform: translateY(1px) scale(1.04); opacity: 1; } }
    @keyframes confetti { 0%, 55%, 100% { transform: translate(0, 0) scale(.3); opacity: 0; } 60% { opacity: 1; } 85%, 99% { transform: translate(var(--dx), var(--dy)) rotate(var(--turn)); opacity: 0; } }
    @keyframes status { 0%, 33% { opacity: 1; } 33.333%, 100% { opacity: 0; } }
    @keyframes underline { 0%, 100% { stroke-dashoffset: 0; } 50% { stroke-dashoffset: -90; } }
    @keyframes equalizer { 0%, 100% { transform: scaleY(.35); } 50% { transform: scaleY(1); } }
'''


def character_defs():
    return '''
    <linearGradient id="lens" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#19273E"/><stop offset="1" stop-color="#4A275D"/></linearGradient>
    <clipPath id="lenses"><path d="M187 128h45l-4 24a10 10 0 0 1-10 8h-18a10 10 0 0 1-10-8Zm61 0h45l-4 24a10 10 0 0 1-10 8h-18a10 10 0 0 1-10-8Z"/></clipPath>'''


def tiger():
    """Shared tiger rig: striped tail, hoodie, expressive ears and sunglasses."""
    return f'''
    <g stroke-linecap="round" stroke-linejoin="round">
      <g class="tail">
        <path d="M278 244c57 31 94-23 64-48" stroke="{OUTLINE}" stroke-width="29"/>
        <path d="M278 244c57 31 94-23 64-48" stroke="#FFAD45" stroke-width="23"/>
        <path d="m300 248-3 13m25-19 5 11m14-25 12 6m-13-26 10-5" stroke="#80433F" stroke-width="8"/>
      </g>
      <g class="body-bob">
        <ellipse cx="231" cy="226" rx="63" ry="52" fill="#FFAD45" stroke="{OUTLINE}" stroke-width="3"/>
        <path d="M177 206q8-25 31-28h45q32 3 36 34l-6 50q-51 17-105-1Z" fill="#A58AF3" stroke="{OUTLINE}" stroke-width="3"/>
        <path d="m207 184 24 25 24-25" fill="#8061C9" stroke="{OUTLINE}" stroke-width="3"/>
        <path d="m220 204-3 21m24-21 3 21" stroke="#91FFE2" stroke-width="3"/>
        <path d="M213 249h42l-5-13h-33Z" fill="#8061C9"/>
        <g class="head-bop">
          <g class="ear"><path d="m179 118-5-40q0-8 8-4l30 27" fill="#FFAD45" stroke="{OUTLINE}" stroke-width="3"/><path d="m183 104-1-19 15 16Z" fill="#F582A2"/></g>
          <path d="m265 101 23-26q7-6 8 3l2 42" fill="#FFAD45" stroke="{OUTLINE}" stroke-width="3"/>
          <path d="m281 103 8-17 1 22Z" fill="#F582A2"/>
          <rect x="174" y="96" width="128" height="111" rx="48" fill="#FFB64E" stroke="{OUTLINE}" stroke-width="3"/>
          <path d="m219 97 7 23 6-24m10 0 5 21 9-20M176 133l23 8-24 3m1 11 20 7-17 3m121-33-21 10 22 2m-1 11-18 8 16 2" fill="#80433F"/>
          <path d="M203 143q5-6 10 0m52 0q5-6 10 0" stroke="{OUTLINE}" stroke-width="3"/>
          <ellipse cx="226" cy="180" rx="19" ry="17" fill="#FFF0CD"/>
          <ellipse cx="250" cy="180" rx="19" ry="17" fill="#FFF0CD"/>
          <path d="m233 172 6 6 6-6Z" fill="#E05E85" stroke="{OUTLINE}" stroke-width="2"/>
          <path d="M239 178v7q-7 7-13 0m13 0q7 7 13 0" stroke="{OUTLINE}" stroke-width="2"/>
          <ellipse cx="195" cy="170" rx="8" ry="5" fill="#EF7E83"/>
          <ellipse cx="282" cy="170" rx="8" ry="5" fill="#EF7E83"/>
          <path d="m192 179-23-4m23 11-23 3m113-10 24-4m-24 11 24 3" stroke="{OUTLINE}" stroke-width="2"/>
          <g class="shades">
            <path d="M176 127h12m104 0h13m-73 8q8-5 16 0" stroke="{OUTLINE}" stroke-width="5"/>
            <path d="M187 128h45l-4 24a10 10 0 0 1-10 8h-18a10 10 0 0 1-10-8Zm61 0h45l-4 24a10 10 0 0 1-10 8h-18a10 10 0 0 1-10-8Z" fill="url(#lens)" stroke="{OUTLINE}" stroke-width="4"/>
            <g clip-path="url(#lenses)">
              <path d="m193 146 25-22m38 23 25-22" stroke="#6FF5DC" stroke-width="4"/>
              <path d="m205 149 25-22m39 23 25-22" stroke="#F18ECA" stroke-width="2.5"/>
              <path class="lens-shine" d="m185 124h10l22 40h-10Z" fill="#FFFFFF" opacity="0"/>
            </g>
          </g>
        </g>
      </g>
    </g>'''


def paws():
    return f'''
    <g stroke="{OUTLINE}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M282 219q17 10 17 31h-17q5-14-4-21" fill="#A58AF3"/>
      <rect x="288" y="249" width="27" height="14" rx="7" fill="#FFB64E"/>
      <path d="M297 256v5m7-5v5" stroke="#A5513C" stroke-width="2"/>
      <g class="typing-paw">
        <rect x="250" y="247" width="33" height="16" rx="8" fill="#FFB64E"/>
        <path d="M261 256v5m8-5v5" stroke="#A5513C" stroke-width="2"/>
      </g>
    </g>'''


def status_pill(p, x, y):
    return f'''<g transform="translate({x} {y})">
      <rect width="244" height="32" rx="16" fill="{p['pill']}"/>
      <circle class="status-ring" cx="17" cy="16" r="4" stroke="{p['mint']}" opacity="0"/>
      <circle cx="17" cy="16" r="4" fill="{p['mint']}"/>
      <g font-family="ui-monospace, 'SFMono-Regular', Consolas, monospace" font-size="12" fill="{p['purple']}">
        <text class="status" x="31" y="21">cooking up cool things</text>
        <text class="status status-two" x="31" y="21" opacity="0">stay curious. stay wild.</text>
        <text class="status status-three" x="31" y="21" opacity="0">100% cat-titude</text>
      </g>
    </g>'''


def confetti():
    pieces = [("#FFBE4F", -55, -40, -70), ("#7CE6C8", -30, -65, 60),
              ("#B78BFF", 2, -76, -110), ("#FF82AD", 33, -58, 110),
              ("#75CFFF", 60, -36, -80), ("#FFAD73", 70, -9, 70)]
    return "\n".join(
        f'<rect class="confetti" x="238" y="94" width="5" height="9" rx="2" fill="{color}" opacity="0" style="--dx:{dx}px;--dy:{dy}px;--turn:{turn}deg"/>'
        for color, dx, dy, turn in pieces)


def scene(p):
    return f'''
  <g stroke-linecap="round" stroke-linejoin="round">
    <rect x="38" y="18" width="356" height="252" rx="110" fill="{p['panel']}"/>
    <circle cx="237" cy="139" r="96" fill="{p['halo']}"/>
    <path d="M146 113h182m-187 20h191m-189 20h187m-181 20h174" stroke="{p['pink']}" stroke-width="2" opacity=".16"/>
    <ellipse cx="237" cy="139" rx="145" ry="89" transform="rotate(-24 237 139)" stroke="{p['orbit']}" stroke-width="2" stroke-dasharray="4 8"/>
    <g class="orbit"><circle cx="348" cy="139" r="6" fill="#FF83B5"/><path d="m126 133 2 5 5 1-5 2-2 5-2-5-5-2 5-1Z" fill="#54CFCA"/></g>
    <ellipse cx="225" cy="285" rx="180" ry="16" fill="{p['ground']}"/>
    <!-- Candy cactus and a striped pink pot. -->
    <g class="plant">
      <path d="M64 221v-66m0 43H48q-10 0-10-10v-12m26 3h16q10 0 10-10v-7" stroke="{OUTLINE}" stroke-width="20"/>
      <path d="M64 221v-66m0 43H48q-10 0-10-10v-12m26 3h16q10 0 10-10v-7" stroke="#60D7B2" stroke-width="15"/>
      <path d="M62 157v49m-23-27v8m50-23v6" stroke="#C1FFE5" stroke-width="2"/>
      <path class="sparkle" d="m63 135 3 8 9-2-5 8 5 6-10-1-5 7-1-10-8-3 9-3Z" fill="#F888BA"/>
    </g>
    <path d="m40 220 6 38q1 9 10 9h16q9 0 10-9l6-38Z" fill="#FF97B2" stroke="{OUTLINE}" stroke-width="2.5"/>
    <path d="m47 233 36 0m-33 12h30" stroke="#FFD4DE" stroke-width="4"/>
    <rect x="37" y="214" width="54" height="11" rx="5" fill="#F973A4" stroke="{OUTLINE}" stroke-width="2.5"/>
    {tiger()}
    <path d="M110 276v17m230-17v17" stroke="#A388D0" stroke-width="8"/>
    <rect x="84" y="263" width="288" height="13" rx="6.5" fill="#79DECF" stroke="{OUTLINE}" stroke-width="2.5"/>
    {paws()}
    <path d="M358 232h7c13 0 13 18 0 18h-7" stroke="#B9863D" stroke-width="5"/>
    <path d="M330 227h30v25q0 11-11 11h-8q-11 0-11-11Z" fill="#FFD069" stroke="{OUTLINE}" stroke-width="2.5"/>
    <path d="m346 234-7 11h6l-2 9 10-13h-7Z" fill="#ED6E98"/>
    <g stroke="{p['pink']}" stroke-width="2" opacity=".7">
      <path class="steam" d="M339 218c-8-8 6-11 0-20"/><path class="steam steam-two" d="M351 218c-8-8 6-11 0-20"/>
    </g>
    <path d="m119 195 113 0a7 7 0 0 1 7 6l12 57H127l-15-54a7 7 0 0 1 7-9Z" fill="#7258BE" stroke="{OUTLINE}" stroke-width="3"/>
    <g clip-path="url(#screen-clip)"><path class="screen-glint" d="m112 194h25l28 65h-25Z" fill="#FFFFFF" opacity="0"/></g>
    <path class="screen-code" d="m156 219-10 9 14 9m41-18 14 9-10 9m-21-23-6 27" stroke="#8BFFE0" stroke-width="3"/>
    <path d="M122 258h139v4q0 5-5 5H128q-6 0-6-6Z" fill="#BBA0F4" stroke="{OUTLINE}" stroke-width="2.5"/>
    <path d="m221 199-5 9h5l-1 7 8-11h-5l3-5Z" fill="#FFACC7"/>
    <!-- Floating stickers and a tiny equalizer keep the scene playful. -->
    <path class="sparkle" d="M357 103v16m-8-8h16" stroke="#F7A643" stroke-width="3"/>
    <path class="sparkle sparkle-two" d="M112 65v12m-6-6h12" stroke="#C17CEA" stroke-width="3"/>
    <text class="float" x="108" y="149" fill="{p['mint']}" font-family="ui-monospace, Consolas, monospace" font-size="17">&lt;/&gt;</text>
    <path class="float float-two" d="M355 168v-21l15-4v21m-15-13 15-4m-15 21c-9-7-14 6-6 6 4 0 6-3 6-6Zm15-4c-9-7-14 6-6 6 4 0 6-3 6-6Z" stroke="{p['purple']}" stroke-width="2.5"/>
    <g transform="translate(141 173)"><path class="float" d="M0 4C0-1 7-2 8 2 11-2 17-1 17 4c0 5-9 11-9 11S0 9 0 4Z" fill="#FF83AD"/></g>
    <g class="cheer">
      <path d="M329 43h68a13 13 0 0 1 13 13v12a13 13 0 0 1-13 13h-49l-19 10 4-10h-4a13 13 0 0 1-13-13V56a13 13 0 0 1 13-13Z" fill="{p['bubble']}" stroke="{p['purple']}" stroke-width="2"/>
      <text x="363" y="67" text-anchor="middle" fill="{p['pink']}" font-family="'Trebuchet MS', Arial, sans-serif" font-size="15" font-weight="700">meow.exe</text>
    </g>
    <g transform="translate(378 224)">
      <rect class="eq" width="5" height="19" rx="2.5" fill="#F7A643"/>
      <rect class="eq eq-two" x="9" y="-7" width="5" height="26" rx="2.5" fill="#F478B0"/>
      <rect class="eq eq-three" x="18" y="-2" width="5" height="21" rx="2.5" fill="#8B76DC"/>
    </g>
    {confetti()}
  </g>'''


def banner(theme, mobile=False):
    p = PALETTES[theme]
    width, height = (480, 580) if mobile else (960, 380)
    output = svg_open(width, height, "Small paws. Big ideas.",
                      "A striped tiger cat in neon sunglasses and a purple hoodie codes and bops beside a candy cactus. Colorful confetti, music notes, and sparkles float around the desk.")
    output += motion_style(CHARACTER_MOTION + SCENE_MOTION)
    output += f'''
  <defs>
    {character_defs()}
    <linearGradient id="rainbow"><stop stop-color="#A483EF"/><stop offset=".35" stop-color="#FB89B3"/><stop offset=".68" stop-color="#FFD074"/><stop offset="1" stop-color="#6BDDC6"/></linearGradient>
    <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="12" cy="12" r=".8" fill="{p['grid']}" opacity=".45"/></pattern>
    <clipPath id="card"><rect width="{width}" height="{height}" rx="24"/></clipPath>
    <clipPath id="screen-clip"><path d="m119 195 113 0a7 7 0 0 1 7 6l12 57H127l-15-54a7 7 0 0 1 7-9Z"/></clipPath>
  </defs>
  <g clip-path="url(#card)">
    <rect width="{width}" height="{height}" fill="{p['bg']}"/>
    <rect width="{width}" height="{height}" fill="url(#dots)"/>
    <rect width="{width}" height="5" fill="url(#rainbow)"/>
'''
    if mobile:
        output += f'''
    <text x="32" y="40" font-family="ui-monospace, Consolas, monospace" fill="{p['muted']}" font-size="14">sellebeww / tiger.exe</text>
    <g font-family="'Trebuchet MS', Arial, sans-serif" font-size="53" font-weight="700" letter-spacing="-2">
      <text x="32" y="107" fill="{p['ink']}">Small paws.</text>
      <text x="32" y="165"><tspan fill="{p['purple']}">Big </tspan><tspan fill="{p['pink']}">ideas.</tspan></text>
    </g>
    <path class="accent-stroke" d="M34 178q100-5 251 0" stroke="url(#rainbow)" stroke-width="4" stroke-linecap="round" stroke-dasharray="55 18 9 18"/>
    <g transform="translate(25 179)">{scene(p)}</g>
    {status_pill(p, 118, 495)}
    <text x="240" y="554" text-anchor="middle" font-family="ui-monospace, Consolas, monospace" font-size="13" letter-spacing="2" fill="{p['muted']}">WEB · AI · DESIGN · AUTOMATION</text>
'''
    else:
        output += f'''
    <text x="46" y="52" font-family="ui-monospace, Consolas, monospace" font-size="14" fill="{p['muted']}">sellebeww / tiger.exe</text>
    <g font-family="'Trebuchet MS', Arial, sans-serif" font-size="62" font-weight="700" letter-spacing="-2">
      <text x="46" y="144" fill="{p['ink']}">Small paws.</text>
      <text x="46" y="212"><tspan fill="{p['purple']}">Big </tspan><tspan fill="{p['pink']}">ideas.</tspan></text>
    </g>
    <path class="accent-stroke" d="M48 226q140-5 310 0" stroke="url(#rainbow)" stroke-width="4" stroke-linecap="round" stroke-dasharray="55 18 9 18"/>
    {status_pill(p, 46, 251)}
    <text x="46" y="337" font-family="ui-monospace, Consolas, monospace" font-size="12" letter-spacing="1.5" fill="{p['muted']}">WEB · AI · DESIGN · AUTOMATION</text>
    <g transform="translate(494 34)">{scene(p)}</g>
'''
    output += f'''
  </g>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="23" stroke="{p['border']}" stroke-width="2"/>
</svg>'''
    suffix = ("-mobile" if mobile else "") + ("-dark" if theme == "dark" else "")
    write_svg(f"tiger-arcade{suffix}.svg", output)


def badge(name, label, symbol, width, color, background, delay):
    output = svg_open(width, 34, label, f"{label} toolkit badge")
    output += motion_style(f'''
    .badge-shine {{ animation: shine 8s ease-in-out {delay}s infinite; }}
    @keyframes shine {{ 0%, 65% {{ transform: translateX(-40px); opacity: 0; }} 70% {{ opacity: .55; }} 94% {{ transform: translateX({width + 25}px); opacity: .55; }} 95%, 100% {{ transform: translateX({width + 25}px); opacity: 0; }} }}
''')
    output += f'''
  <defs><clipPath id="badge-clip"><rect x=".5" y=".5" width="{width - 1}" height="33" rx="9"/></clipPath></defs>
  <rect x=".5" y=".5" width="{width - 1}" height="33" rx="9" fill="{background}" stroke="{color}" stroke-opacity=".3"/>
  <rect x="6" y="6" width="22" height="22" rx="6" fill="{color}"/>
  <text x="17" y="21" text-anchor="middle" fill="#FFFFFF" font-family="Arial, sans-serif" font-size="10" font-weight="700">{escape(symbol)}</text>
  <text x="36" y="22" fill="{OUTLINE}" font-family="Arial, sans-serif" font-size="13" font-weight="600">{escape(label)}</text>
  <g clip-path="url(#badge-clip)"><path class="badge-shine" d="M-14 0H0l17 34H3Z" fill="#FFFFFF" opacity="0"/></g>
</svg>'''
    write_svg(f"badge-{name}.svg", output)


def footer():
    output = svg_open(320, 190, "BRB, taking a catnap.", "A striped tiger cat sleeps curled up on a mint cushion under a purple starry blanket, head resting on its paws, with a crescent moon, twinkling stars, drifting Zzz letters, and neon sunglasses set aside.")
    output += motion_style('''
    .breathe { transform-origin: 150px 140px; animation: breathe 4.5s ease-in-out infinite; }
    .head-rest { animation: head-rest 4.5s ease-in-out infinite; }
    .ear-twitch { transform-origin: 240px 90px; animation: twitch 9s ease-in-out infinite; }
    .tail-flick { transform-origin: 84px 132px; animation: flick 6s ease-in-out infinite; }
    .zzz { transform-box: fill-box; transform-origin: center; animation: dreaming 6s ease-out infinite; opacity: 0; }
    .zzz-two { animation-delay: -2s; }
    .zzz-three { animation-delay: -4s; }
    .star { transform-box: fill-box; transform-origin: center; animation: twinkle 4s ease-in-out infinite; }
    .star-two { animation-delay: -1.3s; }
    .star-three { animation-delay: -2.6s; }
    .glow { animation: glow 6s ease-in-out infinite; }
    @keyframes breathe { 0%, 100% { transform: scale(1, 1); } 50% { transform: scale(1.012, 1.04); } }
    @keyframes head-rest { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(1.5px); } }
    @keyframes twitch { 0%, 82%, 92%, 100% { transform: rotate(0); } 86% { transform: rotate(-7deg); } 89% { transform: rotate(2deg); } }
    @keyframes flick { 0%, 60%, 100% { transform: rotate(0); } 70% { transform: rotate(-9deg); } 80% { transform: rotate(3deg); } 88% { transform: rotate(-4deg); } }
    @keyframes dreaming { 0% { transform: translate(-4px, 8px) scale(.55); opacity: 0; } 20%, 55% { opacity: .95; } 100% { transform: translate(8px, -16px) scale(1.15); opacity: 0; } }
    @keyframes twinkle { 0%, 100% { transform: scale(.55) rotate(-10deg); opacity: .35; } 50% { transform: scale(1.1) rotate(10deg); opacity: 1; } }
    @keyframes glow { 0%, 100% { opacity: .12; } 50% { opacity: .2; } }
''')
    output += f'''
  <defs>
    <mask id="crescent"><rect width="320" height="190" fill="#fff"/><circle cx="58" cy="35" r="15" fill="#000"/></mask>
    <clipPath id="body-clip"><ellipse cx="142" cy="102" rx="78" ry="38"/></clipPath>
    <clipPath id="head-clip"><ellipse cx="214" cy="112" rx="38" ry="31"/></clipPath>
  </defs>
  <g stroke-linecap="round" stroke-linejoin="round">
    <rect class="glow" x="10" y="8" width="300" height="172" rx="76" fill="#B399EE" opacity=".14"/>
    <!-- Night sky: crescent moon and twinkling stars. -->
    <circle cx="50" cy="42" r="18" fill="#FFD98A" mask="url(#crescent)"/>
    <path class="star" d="M104 30 106 36 112 38 106 40 104 46 102 40 96 38 102 36Z" fill="#F7A643"/>
    <path class="star star-two" d="M276 100 277.5 104 282 105.5 277.5 107 276 111 274.5 107 270 105.5 274.5 104Z" fill="#7CE6C8"/>
    <path class="star star-three" d="M30 100 31.5 104 36 105.5 31.5 107 30 111 28.5 107 24 105.5 28.5 104Z" fill="#FF8CB4"/>
    <ellipse cx="160" cy="170" rx="128" ry="9" fill="#B399EE" opacity=".25"/>
    <!-- Mint cushion with stitching. -->
    <rect x="44" y="138" width="232" height="30" rx="15" fill="#5CCDB5" stroke="{OUTLINE}" stroke-width="2.5"/>
    <ellipse cx="160" cy="140" rx="116" ry="20" fill="#91E8D3" stroke="{OUTLINE}" stroke-width="2.5"/>
    <ellipse cx="160" cy="140" rx="98" ry="14" stroke="#49BBA3" stroke-width="1.5" stroke-dasharray="3 5"/>
    <path d="M44 153h-9m242 0h9" stroke="{OUTLINE}" stroke-width="2.5"/>
    <circle cx="32" cy="153" r="4" fill="#F7A643" stroke="{OUTLINE}" stroke-width="2"/>
    <circle cx="288" cy="153" r="4" fill="#F7A643" stroke="{OUTLINE}" stroke-width="2"/>
    <!-- Tail peeks out and flicks. -->
    <g class="tail-flick">
      <path d="M86 132C62 144 46 134 50 118c2-8 10-10 15-6" stroke="{OUTLINE}" stroke-width="17"/>
      <path d="M86 132C62 144 46 134 50 118c2-8 10-10 15-6" stroke="#FFAD45" stroke-width="12"/>
      <path d="M86 132C62 144 46 134 50 118c2-8 10-10 15-6" stroke="#80433F" stroke-width="12" stroke-dasharray="3 9" stroke-linecap="butt"/>
    </g>
    <g class="breathe">
      <ellipse cx="142" cy="102" rx="78" ry="38" fill="#FFB64E" stroke="{OUTLINE}" stroke-width="2.5"/>
      <g clip-path="url(#body-clip)">
        <path d="M138 60 143 84 150 60ZM156 60 161 86 168 60ZM174 62 178 84 186 62Z" fill="#80433F"/>
        <ellipse cx="152" cy="128" rx="46" ry="12" fill="#FFD48B" opacity=".85"/>
      </g>
      <ellipse cx="142" cy="102" rx="78" ry="38" stroke="{OUTLINE}" stroke-width="2.5"/>
      <!-- Starry blanket in hoodie purple. -->
      <path d="M70 114Q70 74 102 68Q130 64 136 88Q144 116 138 143H80Q68 132 70 114Z" fill="#A58AF3" stroke="{OUTLINE}" stroke-width="2.5"/>
      <path d="M76 92Q104 80 134 92" stroke="#C6B2FA" stroke-width="2.5"/>
      <path d="M72 124Q106 134 140 124" stroke="#8061C9" stroke-width="3"/>
      <path d="M92 100 93.5 104 98 105.5 93.5 107 92 111 90.5 107 86 105.5 90.5 104Z" fill="#91FFE2"/>
      <path d="M118 92 119.2 95 122.5 96.2 119.2 97.4 118 100.5 116.8 97.4 113.5 96.2 116.8 95Z" fill="#FFD98A"/>
      <path d="M112 114 113 116.5 115.5 117.5 113 118.5 112 121 111 118.5 108.5 117.5 111 116.5Z" fill="#FF9FC0"/>
    </g>
    <g class="head-rest">
      <g transform="translate(0 -4)">
        <g class="ear-twitch">
          <path d="M230 82 249 60Q255 56 257 64L256 96" fill="#FFB64E" stroke="{OUTLINE}" stroke-width="2.5"/>
          <path d="M243 80 252 68 253 86Z" fill="#F58DA7"/>
        </g>
        <path d="M184 92 180 62Q180 55 187 60L209 80" fill="#FFB64E" stroke="{OUTLINE}" stroke-width="2.5"/>
        <path d="M187 80 187 68 199 78Z" fill="#F58DA7"/>
        <ellipse cx="214" cy="112" rx="38" ry="31" fill="#FFB64E"/>
        <g clip-path="url(#head-clip)">
          <path d="M199 80 205 97 211 80ZM213 78 218 97 224 78ZM227 80 232 95 238 83Z" fill="#80433F"/>
          <path d="M176 106 192 111 176 116ZM252 106 236 111 252 116Z" fill="#80433F"/>
        </g>
        <ellipse cx="214" cy="112" rx="38" ry="31" stroke="{OUTLINE}" stroke-width="2.5"/>
        <ellipse cx="216" cy="124" rx="17" ry="11" fill="#FFF0CD"/>
        <ellipse cx="192" cy="121" rx="6" ry="3.5" fill="#EF7E83" opacity=".85"/>
        <ellipse cx="238" cy="121" rx="6" ry="3.5" fill="#EF7E83" opacity=".85"/>
        <path d="M197 111q6 6 12 0m18 0q6 6 12 0" stroke="{OUTLINE}" stroke-width="2.5"/>
        <path d="m198 113-3 3m13-3 3 3m15-3-3 3m13-3 3 3" stroke="{OUTLINE}" stroke-width="1.5"/>
        <path d="M212 119h8l-4 5Z" fill="#E05E85" stroke="{OUTLINE}" stroke-width="1.5"/>
        <path d="M216 124v2q-4 4-8 1m8-1q4 4 8 1" stroke="{OUTLINE}" stroke-width="1.5"/>
        <path d="M200 124 184 120m16 7-15 3m47-6 16-4m-16 7 15 3" stroke="{OUTLINE}" stroke-width="1.5"/>
      </g>
      <!-- Front paws cradle the chin. -->
      <g stroke="{OUTLINE}" stroke-width="2.2">
        <ellipse cx="198" cy="140" rx="17" ry="8" fill="#FFB64E"/>
        <ellipse cx="230" cy="141" rx="17" ry="8" fill="#FFB64E"/>
        <path d="M192 142v4m7-4v4m26-3v4m7-4v4" stroke="#A5513C" stroke-width="1.6"/>
      </g>
    </g>
    <!-- Sunglasses off: even a cool cat needs a nap. -->
    <g transform="translate(236 171) rotate(-4)">
      <path d="M0 0h16l-2 10H3Zm22 0h16l-2 10H25Z" fill="{OUTLINE}"/>
      <path d="M16 3h6" stroke="{OUTLINE}" stroke-width="2"/>
      <path d="m4 6 5-4m18 4 5-4" stroke="#75EBD5" stroke-width="1.5"/>
    </g>
    <!-- Zzz drifting upward. -->
    <g transform="translate(266 70)"><path class="zzz" d="M0 0h8l-8 10h8" stroke="#B18ADF" stroke-width="2.5"/></g>
    <g transform="translate(280 46)"><path class="zzz zzz-two" d="M0 0h10l-10 12h10" stroke="#F18CAF" stroke-width="3"/></g>
    <g transform="translate(296 18)"><path class="zzz zzz-three" d="M0 0h12l-12 14h12" stroke="#6FD9C3" stroke-width="3.5"/></g>
  </g>
</svg>'''
    write_svg("tiger-sleep.svg", output)


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    for theme_name in PALETTES:
        for compact in (False, True):
            banner(theme_name, compact)
    for args in [
        ("nodejs", "Node.js", "JS", 111, "#29836B", "#DFF9EC", 0),
        ("typescript", "TypeScript", "TS", 133, "#4976C0", "#E5EDFF", .5),
        ("react", "React", "⚛", 98, "#277C9D", "#DFF6FF", 1),
        ("docker", "Docker", "▤", 111, "#8657BA", "#F0E4FF", 1.5),
        ("ai", "AI / LLMs", "✦", 123, "#BF4D7B", "#FFE4EE", 2),
    ]:
        badge(*args)
    footer()
    print("Generated 4 tiger banners, 5 colorful badges, and 1 sleeping tiger.")
