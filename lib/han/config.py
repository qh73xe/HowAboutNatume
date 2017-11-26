# -*- coding: utf-8 -*
"""共通設定を記述."""
from os import path
PROJECT_ROOT = path.dirname(path.dirname(path.dirname(
    path.abspath(__file__)
)))
MODEL_DIR = path.join(PROJECT_ROOT, 'DATA')

MONGOSETTING = {
    'host': 'localhost',
    'port': 27017,
    'db': 'han-api',
    'user': 'han-api',
    'pwd': 'hd7NcCbDShry'
}


AUTHORS = [
    {'name': '夏目漱石', 'url': 'person148.html'}
]
