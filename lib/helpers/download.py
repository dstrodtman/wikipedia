import re
import requests
import pandas as pd
import numpy as np
from sys import argv
import pymongo
from lib.helpers.general import clean

def crawl_cats(cat_q, page_s, max_depth=3):
    next_cat_q = set()
    while cat_q:
        cat = cat_q.pop()
        r = requests.get('http://en.wikipedia.org/w/api.php?action=query&format=json&\
                          list=categorymembers&cmtitle=Category%3A{}&cmlimit=max'.format(cat))

        if r.status_code != 200:
            raise('Status error when getting {}'.format(cat))

        try:
            r_df = pd.DataFrame(r.json()['query']['categorymembers'])

            r_df['title'] = r_df.title.apply(lambda x: clean(x))

            category_mask = r_df.title.str.contains('Category:')
            
            for category in r_df[category_mask]['title']:
                next_cat_q.add(category[9:])
            
            for page in r_df[~category_mask]['title']:
                page_s.add(page)
        except:
            print('Error for {}'.format(cat))
    max_depth -= 1
    if max_depth < 0:
        return page_s
    page_s = crawl_cats(next_cat_q, page_s, max_depth)
    return page_s

def scrape_page(page):

    r = requests.get("http://en.wikipedia.org/w/api.php?action=query&\
                      format=json&prop=extracts&titles={}&rvprop=content".format(page))

    if r.status_code != 200:
            raise('Status error when getting {}'.format(page))

    q_key = list(r.json()['query']['pages'].keys())[0]

    title = r.json()['query']['pages'][q_key]['title']

    text = r.json()['query']['pages'][q_key]['extract']

    return title, text

def mongo_write(page, title, text, cat_arg):
    cli = pymongo.MongoClient('52.36.190.91', 27016)
    db_ref = cli.semantic_search
    co_ref = db_ref['{}'.format(cat_arg)]
    co_ref.insert_one({'page': page, 'category':re.sub('_', ' ', cat_arg), 'title':title, 'text':text})

