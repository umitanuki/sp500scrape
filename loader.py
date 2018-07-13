from data import *

from IPython import embed
import pandas as pd

def fetch(date):
    today = pd.Timestamp('now').floor('1D').strftime('%Y-%m-%d')
    symbols = set(latest)
    for key in sorted(changes.keys(), reverse=True):
        if key < date:
            break
        symbols -= set(changes[key]['added'])
        symbols |= set(changes[key]['removed'])
    return symbols

embed()