#!/usr/bin/env python
# coding=utf-8
import re

import requests

from deck import Card, Lesson


def build_url(lesson_number):
    """Build a URL to download the words for the given lesson_number.

    lesson_number: The int lesson number
    """
    url = ('http://www.yellowbridge.com/chinese/fc-load.php?'
           'language=zh&deck=ic3-2&wordLists=ic3-2-{lesson_number}')
    return url.format(lesson_number=lesson_number)


def card_from_raw_data(data):
    traditional_character_pattern = re.compile(r'tc:"([^"]+)"')
    simplified_character_pattern = re.compile(r'sc:"([^"]+)"')
    english_pattern = re.compile(r'en:"([^"]+)"')
    pinyin_pattern = re.compile(r'py:"([^"]+)"')
    pronunciation_pattern = re.compile(r'pn:"([^"]+)"')
    lesson_pattern = re.compile(r'rf:"([^"]+)"')
    df_pattern = re.compile(r'df:(\d+)')
    card = Card(
        english=english_pattern.findall(data)[0],
        traditional_character=traditional_character_pattern.findall(data)[0],
        simplified_character=simplified_character_pattern.findall(data)[0],
        pinyin=pinyin_pattern.findall(data)[0],
        pronunciation=pronunciation_pattern.findall(data)[0],
        lesson=lesson_pattern.findall(data)[0],
        df=df_pattern.findall(data)[0])
    return card


def get_cards(url):
    response = requests.get(url)
    data = response.content
    cards = []
    for line in data.split("},{"):
        card = card_from_raw_data(line.decode('utf8'))
        cards.append(card)
    return cards


def get_lesson(lesson_number):
    url = build_url(lesson_number)
    lesson = Lesson(lesson_number, get_cards(url))
    return lesson


def lesson_to_tsv(lesson):
    """Turn a Lesson into a tsv"""
    lines = []
    line = u"{characters}\t<i>{pinyin}</i>\t{english}\t{tags}\n"
    for card in lesson.cards:
        characters = card.traditional_character
        if card.simplified_character != card.traditional_character:
            characters += u"<br>" + card.simplified_character
        lines.append(line.format(
            characters=characters,
            pinyin=card.pinyin,
            english=card.english,
            tags=u"IC3_LEVEL_2_LESSON_%s" % lesson.chapter).encode('utf8'))
    return lines


if __name__ == "__main__":
    with open('deck.txt', 'w') as f:
        for lesson_number in range(1, 21):
            print(lesson_number)
            lesson = get_lesson(lesson_number)
            lines = lesson_to_tsv(lesson)
            f.writelines(lines)
