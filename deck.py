#!/usr/bin/env python
# coding=utf-8
from collections import namedtuple

Card = namedtuple("card", [
    'english',
    'traditional_character',
    'simplified_character',
    'pinyin',
    'pronunciation',
    'lesson',
    'df'
])


Lesson = namedtuple("lesson", [
    'chapter',
    'cards'
])
