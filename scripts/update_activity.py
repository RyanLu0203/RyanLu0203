"""Refresh a public-only GitHub snapshot; preserve old assets if the API fails."""
import json
import os
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
LOGIN = 'RyanLu0203'

def request(url):
    headers={'Accept':'application/vnd.github+json','User-Agent':'RyanLu0203-profile','X-GitHub-Api-Version':'2022-11-28'}
    if os.environ.get('GITHUB_TOKEN'):
        headers['Authorization']='Bearer '+os.environ['GITHUB_TOKEN']
    with urlopen(Request(url,headers=headers),timeout=30) as r:
        return json.load(r)

def render(metrics,date,dark=False):
    bg,ink,muted,border=('#101d2c','#e1f3f5','#8eaebb','#27434f') if dark else ('#f6fbfa','#173c49','#61818a','#cee5df')
    pieces=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="222" viewBox="0 0 1200 222" role="img"><title>Public GitHub snapshot for {LOGIN}, updated {date} UTC</title>',f'<rect x="1" y="1" width="1198" height="220" rx="22" fill="{bg}" stroke="{border}"/>',f'<g font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif"><text x="36" y="39" fill="{muted}" font-size="13" letter-spacing="2">GITHUB / PUBLIC SNAPSHOT</text><text x="1164" y="39" text-anchor="end" fill="{muted}" font-size="12">UPDATED {date} UTC</text>']
    for i,(value,label,accent) in enumerate(metrics):
        x=38+i*398
        if i: pieces.append(f'<path d="M{x-20} 73V184" stroke="{border}"/>')
        pieces.extend([f'<text x="{x}" y="136" font-size="58" font-weight="700" fill="{ink}">{value}</text>',f'<circle cx="{x+5}" cy="171" r="4" fill="{accent}"><animate attributeName="opacity" values="1;.35;1" dur="3s" repeatCount="indefinite"/></circle>',f'<text x="{x+20}" y="176" font-size="16" fill="{muted}">{escape(label)}</text>'])
    return ''.join(pieces)+'</g></svg>\n'

def main():
    user=request(f'https://api.github.com/users/{LOGIN}')
    repos=[];page=1
    while True:
        batch=request(f'https://api.github.com/users/{LOGIN}/repos?type=owner&per_page=100&page={page}')
        repos.extend(batch)
        if len(batch)<100:break
        page+=1
    assert all(not r.get('private',True) and r['owner']['login'].lower()==LOGIN.lower() for r in repos)
    metrics=[(len(repos),'Public repositories','#35b99a'),(sum(r['stargazers_count'] for r in repos),'Stars on public repos','#d8ad48'),(user['followers'],'Followers','#8c86d5')]
    date=datetime.now(timezone.utc).date().isoformat()
    for theme in ('light','dark'):
        path=ROOT/f'assets/activity-{theme}.svg'
        content=render(metrics,date,theme=='dark')
        temporary=path.with_suffix('.tmp')
        temporary.write_text(content)
        temporary.replace(path)
    print('Refreshed public GitHub snapshot:',[m[:2] for m in metrics])

if __name__=='__main__':main()
