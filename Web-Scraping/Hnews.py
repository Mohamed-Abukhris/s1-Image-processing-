import requests
from bs4 import BeautifulSoup
import pprint
import csv , re

res = requests.get('https://news.ycombinator.com/news')
res2 = requests.get('https://news.ycombinator.com/news?p=2')
soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

links = soup.select('.titleline')
subtext = soup.select('.subtext')
links2 = soup2.select('.titleline')
subtext2 = soup2.select('.subtext')

mega_links = links + links2
mega_subtext = subtext + subtext2

def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key = lambda k:k['votes'] , reverse = True)

def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        a = item.find('a', href=True)
        title = a.get_text(strip=True) if a else item.get_text(strip=True)
        href = a['href'] if a else None

        if href and href.startswith('item?id='):
            href = 'https://news.ycombinator.com/' + href

        s = subtext[idx] if idx < len(subtext) else None
        vote = s.select('.score') if s else []
        if vote:
            points = int(vote[0].get_text().split()[0])

            comments = 0
            if s:
                for a2 in s.select('a'):
                    txt = a2.get_text(' ', strip=True).lower()
                    if 'comment' in txt or txt == 'discuss':
                        m = re.search(r'(\d+)\s*comment', txt)
                        comments = int(m.group(1)) if m else 0
                        break

            if points > 99:
                hn.append({
                    'title': title,
                    'link': href,
                    'votes': points,
                    'comments': comments
                })
    return sort_stories_by_votes(hn)

def save_to_csv(items, filename='hn_top.csv'):
        fieldnames = ['title', 'link', 'votes', 'comments']
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for it in items:
                writer.writerow(it)
        print(f"Saved {len(items)} items to {filename}")

stories = create_custom_hn(mega_links, mega_subtext)
pprint.pprint(stories)
save_to_csv(stories, 'hn_top_over_100_votes.csv')

