import base64
import json
import os
import pathlib
import re
import sys
from typing import Union
from urllib.parse import quote

import jinja2
import requests

from game import MasterMind, Color

base_url = os.environ.get('GITHUB_API_URL', 'https://api.github.com')
token = os.environ['GITHUB_TOKEN']
repo = os.environ.get('REPOSITORY', 'drdilyor/drdilyor')

try:
    issue_number = int(os.environ['ISSUE_NUMBER'])
except ValueError:
    sys.stderr.write('ISSUE_NUMBER must be a number\n')
    sys.exit(1)

session = requests.Session()
session.headers['Authorization'] = f'token {token}'
repo_url = f'{base_url}/repos/{repo}'

readme_request = session.get(f'{repo_url}/contents/README.md')
assert readme_request.ok
readme_json = readme_request.json()
readme = base64.b64decode(readme_json['content']).decode('utf-8')
readme_sha = readme_json['sha']

if match := re.search(
        r'^GAME_SAVED_STATE$(.*?)^END_GAME_SAVED_STATE$',
        readme, re.DOTALL | re.MULTILINE):
    game = MasterMind.from_saved_state(json.loads(match[1]))
else:
    game = MasterMind()

issue_request = session.get(f'{repo_url}/issues/{issue_number}')
assert issue_request.ok
issue = issue_request.json()


def answer(message):
    print('answer')
    url = f'{repo_url}/issues/{issue_number}/comments'
    res = session.post(url, json={'body': message})
    print(res.json())
    assert res.ok


issue_title: str = issue['title']
assert issue_title.startswith('mastermind:')
action, _, args = issue_title.partition(':')[2].partition(':')
if action == 'select':
    try:
        position, _, color = args.partition(':')
        position = int(position)
        color = int(color)
    except ValueError:
        answer('Malformed input N1')
        sys.exit(1)
    if color not in range(1, 7) or position not in range(4):
        answer('Malformed input N2')
        sys.exit(1)

    game.select_color(position, Color._value2member_map_[color])
elif action == 'commit':
    if args:
        answer('Malformed Input N3')
        sys.exit(1)
    game.commit()
elif action == 'new':
    if args:
        answer('Malformed Input N3')
        sys.exit(1)
    game = MasterMind()
else:
    answer('Malformed input N4')
    sys.exit(1)

# draw

ROOT_DIR = pathlib.Path(__file__).parent.parent

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(ROOT_DIR),
    autoescape=jinja2.select_autoescape(),
)


def get_color(col: 'Union[Color, int]'):
    if isinstance(col, Color):
        col = col.value
    return '🟡🟠🔴🟣🔵🟢'[col - 1]


def new_issue_url(title):
    title = quote(title)
    body = quote("Just push 'Submit new issue' and allow up to 30 seconds.")
    return f"https://github.com/{repo}/issues/new?title={title}&body={body}"


def select_url(position: int, color: int):  # noqa
    return new_issue_url(f'mastermind:select:{position}{color}')


readme_template = jinja_env.get_template('README.template.md')
readme_new = readme_template.render(
    game=game,
    repo=repo,
    color=get_color,
    new_issue_url=new_issue_url,
    select_url=select_url,
)
readme_new += f"""
<!--
GAME_SAVED_STATE
{json.dumps(game.save_state())}
END_GAME_SAVED_STATE
-->
"""

readme_new_res = session.put(f'{repo_url}/contents/README.md', json={
    'message': 'Mastermind: update README.md',
    'content': base64.b64encode(readme_new.encode('utf-8')).decode('utf-8'),
    'sha': readme_sha,
})
assert readme_new_res.ok, readme_new_res.json()

answer(f'Done. Return <a href="https://github.com/{repo}">back</a> to continue')
