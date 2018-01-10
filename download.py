from lib.helpers.download import crawl_cats, scrape_page, mongo_write
import re
import requests
import pandas as pd
import numpy as np
from sys import argv
import pymongo

if len(argv) == 1:
    raise('Please pass a valid wikipedia category name')

cat_arg = '_'.join((argv)[1:])

cat_q = set()
cat_q.add(cat_arg)

page_s = set()

page_s = crawl_cats(cat_q, page_s)

while page_s:
    page = page_s.pop()
    try:
        title, text = scrape_page(page)
        mongo_write(page, title, text, cat_arg)
    except:
        print('Error on {}'.format(page))
