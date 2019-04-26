import requests
from bs4 import BeautifulSoup
import pandas as pd


def parse(soup):
    tables = soup.select('table')

    current = []
    for row in tables[0].select('tbody')[0].select('tr')[1:]:
        current.append(row.select('td')[0].text.strip())

    changes = {}
    last_date = None
    rowspan = 0
    for row in tables[1].select('tbody')[0].select('tr')[2:]:
        cells = row.select('td')
        if rowspan == 0:
            date = pd.Timestamp(cells[0].text).strftime('%Y-%m-%d')
            rowspan = int(cells[0].get('rowspan') or 1)
            has_date = True
        else:
            has_date = False
            date = last_date
        added = cells[1 if has_date else 0].text.strip()
        removed = cells[3 if has_date else 2].text.strip()
        if date not in changes:
            changes[date] = {
                'added': [],
                'removed': [],
            }
        if added != '':
            changes[date]['added'].append(added)
        if removed != '':
            changes[date]['removed'].append(removed)
        last_date = date
        rowspan -= 1

    print(f'latest = {current}\n')
    print(f'changes = {changes}\n')
    return current, changes
    from IPython import embed
    embed()


def write_history(current, changes):
    date = pd.Timestamp('now').floor('1D')
    start = pd.Timestamp('2000-01-01')
    symbols = set(current)
    with open('data.csv', 'w') as fp:
        while date > start:
            today = date.strftime('%Y-%m-%d')
            if today in changes:
                symbols += set(changes['removed'])
                symbols -= set(changes['added'])
            slist = ','.join(sorted(list(symbols)))
            fp.write(f'{today},"{slist}"\n')
            date -= pd.Timedelta('1day')


def main():
    content = requests.get(
        'https://en.wikipedia.org/wiki/List_of_S&P_500_companies').content
    soup = BeautifulSoup(content, 'html.parser')

    current, changes = parse(soup)

    # write_history(current, changes)
    return


if __name__ == '__main__':
    main()
