from data import latest, changes

from IPython import embed


def fetch(date):
    '''
    date = YYYY-MM-DD
    '''
    symbols = set(latest)
    for key in sorted(changes.keys(), reverse=True):
        if key < date:
            break
        symbols -= set(changes[key]['added'])
        symbols |= set(changes[key]['removed'])
    return symbols


embed()
