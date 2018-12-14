#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 2018/9/28
import sys
from hashlib import md5
import requests
import uuid
import argparse
import re


class Language:
    ch = u'中文'


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def fm(s):
    """
    clear rich text
    :param s:
    :return:
    """
    return re.sub(r'<.*?>', '', s)


def search(text):
    print(u'{}using sougou translate search [{}] ...{}'.format(Bcolors.HEADER, text, Bcolors.ENDC))

    url = 'https://fanyi.sogou.com/reventondc/translate'
    _from = 'auto'
    to = 'zh-CHS'
    s = md5('{}{}{}{}'.format(_from, to, text, '41ee21a5ab5a13f72687a270816d1bfd').encode()).hexdigest()
    param = {'from'           : _from,
             'to'             : to,
             'client'         : 'pc',
             'fr'             : 'browser_pc',
             'text'           : text,
             'useDetect'      : 'on',
             'useDetectResult': 'on',
             'needQc'         : 1,
             'uuid'           : str(uuid.uuid4()),
             'oxford'         : 'on',
             'isReturnSugg'   : 'on',
             's'              : s}
    resp = requests.post(url=url, data=param).json()

    detect = resp.get('detect', {}).get('language')

    sys.stdout.write("\033[F")  # back to previous line
    sys.stdout.write("\033[K")  # clear line

    print(Bcolors.OKGREEN)
    print(u'{0: >10} : {1}'.format('text', resp.get('translate', {}).get('text')))
    print(u'{0: >10} : {1}'.format('dit', resp.get('translate', {}).get('dit')))

    # print(json.dumps(resp))
    d = resp.get('dictionary')
    if d:
        for item in d['content']:
            phonetic = item.get('phonetic', [])
            if isinstance(phonetic, list):
                for p in phonetic:
                    print(u'{0: >10} : {1}'.format(p['type'], p['text']))

            for u in item.get('usual', []):
                print(u'{0: >10} : {1}'.format(u['pos'], fm(' '.join(u['values']))))

    if detect == Language.ch and d:
        for item in d['content']:
            cat = item.get('category', [])
            for c in cat:
                for sense in c['sense']:
                    print('{:>10} : {}'.format('sense', sense['description']))

    print('')


def main():
    parser = argparse.ArgumentParser(description='search tool')

    parser.add_argument('text', nargs='?', help='search content')
    parser.add_argument('-e', nargs='+', help='search engineer')

    args = parser.parse_args()

    if args.text:
        search(args.text)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
