import re
import requests
import pandas as pd
import numpy as np
from sys import argv
import pymongo

def clean(string):
    string = re.sub('\s', '_', string)
    string = re.sub('\+', '%2B', string)
    string = re.sub('\&', '%26', string)
    return string