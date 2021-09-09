BOOK_SHIJING = 'shijing.json'
BOOK_YUEFU = 'yuefu.json'
BOOK_TANGSHI = 'tangshi.json'
BOOK_CIFU = 'cifu.json'
BOOK_CHUCI = 'chuci.json'
BOOK_SONGCI = 'songci.json'
BOOK_GUSHI = 'gushi.json'

import json
import random
import re
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

here = Path(__file__).absolute().parent


def clean_str(string: str):
    return ''.join(
        (
            s
            for s in string
            if s
            not in '胸鬼懒禽鸟鸡我邪罪凶丑仇鼠蟋蟀淫秽妹狐鸡鸭蝇悔鱼肉苦犬吠窥血丧饥女搔父母昏狗蟊疾病痛死潦哀痒害蛇牲妇狸鹅穴畜烂兽靡爪氓劫鬣螽毛婚姻匪婆羞辱'
        )
    )


def format_str(string: str):
    return re.sub(r'\(.+\)', '', re.sub(r'(\s|　|”|“){1,}|<br>|<p>|<\/p>', '', string))


def clean_punctuation(string):
    return re.sub(r'[<>《》！*\(\^\)\$%~!@#…&%￥—\+=、。，？；‘’“”：·`]', '', string)


def split_setence(content):
    string = format_str(content)
    string = re.sub(r'！|。|？|；', lambda m: f'{m.group()}|', string)
    string = string.rstrip('|')
    return [i for i in string.split('|') if len(i) >= 2]


def get_chars(items):
    length = len(items)
    first = random.randrange(0, length)
    second = random.randrange(0, length)

    times = 100
    while times > 0 and first == second:
        second = random.randrange(0, length)
        times -= 1
    if first <= second:
        return items[first] + items[second]
    return items[second] + items[first]


class Passage(BaseModel):
    content: str
    title: str
    author: Optional[str]
    book: str
    dynasty: str


class Name(Passage):
    name: str
    sentence: str


class Namer:
    def __init__(self, book: str = BOOK_SHIJING):
        with open(here / 'json' / book) as f:
            self.passages = json.load(f)

    def genarate(self) -> Optional[Name]:
        passage_dict = random.choice(self.passages)
        passage_dict['content'] = format_str(passage_dict['content'])
        passage = Passage(**passage_dict)
        if not passage.content:
            return

        sentence_list = split_setence(passage.content)
        if not sentence_list:
            return

        sentence = random.choice(sentence_list)

        clean_sentence = clean_str(clean_punctuation(sentence))
        if len(clean_sentence) <= 2:
            return

        name = get_chars(list(clean_sentence))
        return Name(name=name, sentence=sentence, **passage.dict())


if __name__ == '__main__':
    namer = Namer()
    name = namer.genarate()
    print(name)
