#!/usr/bin/env python3
"""Fetch public GitHub data and render local, dependency-free profile cards.

GITHUB_TOKEN is required for the contribution calendar. To render an existing
snapshot without a network request: python3 scripts/update-stats.py --offline
"""
import argparse
import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
SNAPSHOT = ASSETS / 'github-data.json'
USERNAME = 'sellebeww'
COLORS = ['#17232e', '#314e61', '#507991', '#80aec5', '#cee8f2']


def request(path, payload=None):
    token = os.environ.get('GITHUB_TOKEN')
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'sellebeww-profile'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    data = json.dumps(payload).encode() if payload else None
    req = Request(f'https://api.github.com/{path}', data=data, headers=headers)
    with urlopen(req, timeout=30) as response:
        return json.load(response)


def fetch():
    if not os.environ.get('GITHUB_TOKEN'):
        raise SystemExit('Set GITHUB_TOKEN to refresh, or use --offline to render the saved snapshot.')
    user = request(f'users/{USERNAME}')
    repos = []
    page = 1
    while True:
        batch = request(f'users/{USERNAME}/repos?per_page=100&page={page}')
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    query = '''query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks { contributionDays { contributionCount date weekday } }
          }
        }
      }
    }'''
    result = request('graphql', {'query': query, 'variables': {'login': USERNAME}})
    if result.get('errors'):
        raise RuntimeError(result['errors'])
    calendar = result['data']['user']['contributionsCollection']['contributionCalendar']
    # Exclude forks from stars/languages; never call primary-language counts byte shares.
    originals = [repo for repo in repos if not repo['fork']]
    return {
        'username': USERNAME,
        'updated_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'public_repos': user['public_repos'],
        'followers': user['followers'],
        'stars': sum(repo['stargazers_count'] for repo in originals),
        'primary_languages': dict(Counter(repo['language'] for repo in originals if repo['language'])),
        'calendar': calendar,
    }


def text(x, y, value, size=14, fill='#dce8f0', attrs=''):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" {attrs}>{escape(str(value))}</text>'


def card(width, height, title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title>
<defs><linearGradient id="panel" x2="1" y2="1"><stop stop-color="#15222e"/><stop offset="1" stop-color="#0b121b"/></linearGradient></defs>
<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="14" fill="url(#panel)" stroke="#314555"/>
{body}
</svg>\n'''


def streaks(calendar):
    days = [day for week in calendar['weeks'] for day in week['contributionDays']]
    longest = run = 0
    for day in days:
        run = run + 1 if day['contributionCount'] else 0
        longest = max(longest, run)
    # A still-in-progress last day with no contributions does not end the streak.
    eligible = days[:-1] if days and days[-1]['contributionCount'] == 0 else days
    current = 0
    for day in reversed(eligible):
        if not day['contributionCount']:
            break
        current += 1
    return current, longest


def render(data):
    calendar = data['calendar']
    updated = data['updated_at'][:10]
    current, longest = streaks(calendar)
    body = text(24, 34, 'SYSTEM STATUS', 12, '#a8c7d9', 'letter-spacing="2.5"')
    body += text(24, 58, f'Public GitHub snapshot / {updated}', 12, '#a0b6c6')
    metrics = [(data['public_repos'], 'Public repos'), (calendar['totalContributions'], 'Contributions · 1y'), (current, 'Current streak · days'), (longest, 'Best streak · 1y')]
    for index, (value, label) in enumerate(metrics):
        x, y = 24 + (index % 2) * 218, 108 + (index // 2) * 87
        body += text(x, y, value, 34, '#edf5fa')
        body += text(x, y + 23, label, 13, '#adc3d2')
    body += '<path d="M24 239H436" stroke="#304353"/>'
    body += text(24, 266, f"{data['stars']} repository stars  /  {data['followers']} followers", 12, '#a0b6c6')
    (ASSETS / 'stats.svg').write_text(card(460, 290, f"{USERNAME}: {data['public_repos']} public repositories, {calendar['totalContributions']} contributions in the past year. Updated {updated}.", body))

    body = text(24, 34, 'LANGUAGE SIGNAL', 12, '#a8c7d9', 'letter-spacing="2.5"')
    body += text(24, 58, 'Primary language per public, non-fork repository', 12, '#a0b6c6')
    languages = sorted(data['primary_languages'].items(), key=lambda item: (-item[1], item[0]))[:5]
    max_count = max((count for _, count in languages), default=1)
    for i, (language, count) in enumerate(languages):
        y = 88 + i * 32
        body += text(24, y, language, 14)
        body += f'<rect x="144" y="{y-9}" width="230" height="5" rx="2.5" fill="#233440"/>'
        body += f'<rect x="144" y="{y-9}" width="{230 * count / max_count:.1f}" height="5" rx="2.5" fill="#9cbfd2"/>'
        body += text(433, y, count, 13, '#bed2df', 'text-anchor="end"')
    body += '<path d="M24 239H436" stroke="#304353"/>'
    body += text(24, 266, 'Repository counts, not proficiency or code percentages.', 12, '#a0b6c6')
    (ASSETS / 'languages.svg').write_text(card(460, 290, 'Primary languages by public non-fork repository count: ' + ', '.join(f'{k} {v}' for k, v in languages), body))

    for mobile in (False, True):
        weeks = calendar['weeks'][-16:] if mobile else calendar['weeks']
        width, height = (460, 294) if mobile else (960, 256)
        step, cell = (25, 19) if mobile else (16, 11)
        left, top = (30, 78) if mobile else (54, 84)
        body = text(24, 34, 'TRACES LEFT BEHIND', 12, '#a8c7d9', 'letter-spacing="2.5"')
        body += text(24, 58, f"{'Last 16 weeks' if mobile else 'Past year'} / updated {updated}", 12, '#a0b6c6')
        peak = max((day['contributionCount'] for week in calendar['weeks'] for day in week['contributionDays']), default=0)
        for i, week in enumerate(weeks):
            for day in week['contributionDays']:
                count = day['contributionCount']
                level = 0 if not count else min(4, 1 + int((count / max(peak, 1)) * 3))
                body += f'<rect x="{left+i*step}" y="{top+day["weekday"]*step}" width="{cell}" height="{cell}" rx="2" fill="{COLORS[level]}"><title>{day["date"]}: {count} contributions</title></rect>'
        if not mobile:
            for weekday, label in [(1, 'M'), (3, 'W'), (5, 'F')]:
                body += text(24, top + weekday * step + 10, label, 10, '#a0b6c6')
            first = weeks[0]['contributionDays'][0]['date']
            last = weeks[-1]['contributionDays'][-1]['date']
            body += text(24, 231, f'{first} — {last}', 12, '#a0b6c6')
        body += text(width - 175, height - 23, 'LESS', 10, '#a0b6c6')
        for i, color in enumerate(COLORS):
            body += f'<rect x="{width-138+i*15}" y="{height-33}" width="10" height="10" rx="2" fill="{color}"/>'
        body += text(width - 56, height - 23, 'MORE', 10, '#a0b6c6')
        name = 'activity-mobile.svg' if mobile else 'activity.svg'
        (ASSETS / name).write_text(card(width, height, f"GitHub contribution activity for {USERNAME}, {'last 16 weeks' if mobile else 'past year'}, updated {updated}.", body))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--offline', action='store_true')
    args = parser.parse_args()
    data = json.loads(SNAPSHOT.read_text()) if args.offline else fetch()
    render(data)
    if not args.offline:
        SNAPSHOT.write_text(json.dumps(data, indent=2) + '\n')
    print('Rendered stats, languages, and desktop/mobile contribution cards.')


if __name__ == '__main__':
    main()
