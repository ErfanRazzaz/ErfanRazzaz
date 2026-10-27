import os, json, urllib.request, html, datetime
from pathlib import Path
USER = "ErfanRazzaz"
def fetch(path):
    req = urllib.request.Request("https://api.github.com/" + path, headers={"Authorization": "Bearer " + os.environ["GITHUB_TOKEN"], "Accept": "application/vnd.github+json", "User-Agent": "ErfanRazzaz-profile"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)
user = fetch("users/" + USER)
repos = []
page = 1
while True:
    batch = fetch(f"users/{USER}/repos?per_page=100&page={page}&type=owner")
    repos.extend(batch)
    if len(batch) < 100: break
    page += 1
original = [r for r in repos if not r["fork"]]
languages = {}
for r in original:
    if r["language"]: languages[r["language"]] = languages.get(r["language"], 0) + 1
parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="390" viewBox="0 0 1100 390"><rect width="1100" height="390" rx="18" fill="#0d1117"/>']
def text(x,y,t,size=19,color="#c9d1d9"):
    parts.append(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="{color}">{html.escape(str(t))}</text>')
text(36,46,"PUBLIC GITHUB SNAPSHOT",18,"#2dd4bf")
text(36,92,f"{user['public_repos']} public repos     /     {user['followers']} followers     /     {sum(r['stargazers_count'] for r in original)} stars on original repos",24,"#f0f6fc")
text(36,136,"Primary languages by original public repository count",17)
colors=["#a78bfa","#2dd4bf","#60a5fa","#fbbf24","#fb7185"]
for i,(name,count) in enumerate(sorted(languages.items(), key=lambda x:(-x[1],x[0]))[:5]):
    y=174+i*31
    text(36,y+15,f"{name} ({count})",16)
    width=round(680*count/max(languages.values()))
    parts.append(f'<rect x="260" y="{y}" width="{width}" height="17" rx="5" fill="{colors[i]}"/>')
if not languages: text(36,190,"No language data available yet.")
text(36,365,"Updated " + datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d UTC") + " · Public work only · Forks excluded from stars and languages",14,"#8b949e")
parts.append('</svg>')
Path("assets/activity.svg").write_text("".join(parts),encoding="utf-8")
