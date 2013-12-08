#!/usr/bin/env python
# coding=utf-8
import demjson
import requests

from deck import Card, Lesson


def build_url(lesson_number):
    """Build a URL to download the words for the given lesson_number.

    lesson_number: The int lesson number
    """
    url = ('http://www.yellowbridge.com/chinese/fc-load.php?'
           'language=zh&deck=ic3-2&wordLists=ic3-2-{lesson_number}')
    return url.format(lesson_number=lesson_number)


def card_from_json(data):
    card = Card(
        english=data['en'],
        traditional_character=data['tc'],
        simplified_character=data['sc'],
        pinyin=data['py'],
        pronunciation=data['pn'],
        lesson=data['rf'],
        df=data['df'],)
    return card


def get_cards(url):
    response = requests.get(url)
    data = response.content
    data = data.strip("var cardDeck = ")
    data = data.rstrip(";var loggedIn=false;var incTooBig=false;finishInit();")
    json = demjson.decode(data)
    cards = []
    for datum in json:
        card = card_from_json(datum)
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
            tags=u"IC3_Level_2_Lesson_%s" % lesson.chapter).encode('utf8').
            replace('\\"', '"'))
    return lines


if __name__ == "__main__":
    with open('deck.txt', 'w') as f:
        for lesson_number in range(1, 21):
            print(lesson_number)
            lesson = get_lesson(lesson_number)
            lines = lesson_to_tsv(lesson)
            f.writelines(lines)
