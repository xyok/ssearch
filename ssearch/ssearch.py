#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created on 2018/9/28
import json
import sys

import requests
import uuid
import argparse
import re


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def fm(s: str):
    """
    消除富文本内容
    :param s:
    :return:
    """
    return re.sub(r'<.*?>', '', s)


def search(text):
    print('{}正在使用搜狗翻译查询 [{}] ...{}'.format(Bcolors.HEADER, text, Bcolors.ENDC))

    url = 'https://fanyi.sogou.com/reventondc/translate'
    param = {'from'           : 'auto',
             'to'             : 'zh-CHS',
             'client'         : 'pc',
             'fr'             : 'browser_pc',
             'text'           : text,
             'useDetect'      : 'on',
             'useDetectResult': 'on',
             'needQc'         : 1,
             'uuid'           : uuid.uuid4(),
             'oxford'         : 'on',
             'isReturnSugg'   : 'off'}

    resp = requests.post(url=url, data=param).json()

    detect = resp.get('detect', {}).get('language')

    sys.stdout.write("\033[F")  # back to previous line
    sys.stdout.write("\033[K")  # clear line

    print(Bcolors.OKGREEN)
    print('{0: >10} : {1}'.format('text', resp.get('translate', {}).get('text')))
    print('{0: >10} : {1}'.format('dit', resp.get('translate', {}).get('dit')))

    # print(json.dumps(resp))
    d = resp.get('dictionary')
    if d:
        for item in d['content']:
            phonetic = item.get('phonetic', [])
            if isinstance(phonetic, list):
                for p in phonetic:
                    print('{0: >10} : {1}'.format(p['type'], p['text']))

            for u in item.get('usual', []):
                print('{0: >10} : {1}'.format(u['pos'], fm(' '.join(u['values']))))

    if detect == '中文' and d:
        for item in d['content']:
            cat = item.get('category', [])
            for c in cat:
                for sense in c['sense']:
                    print('{:>10} : {}'.format('sense', sense['description']))

    print('')


def main():
    parser = argparse.ArgumentParser(description='search tool')

    parser.add_argument('text', nargs='?', help='搜索内容')
    parser.add_argument('-e', nargs='+', help='search engineer')

    args = parser.parse_args()

    if args.text:
        search(args.text)
    else:
        parser.print_help()


def test():
    search('notorio')


if __name__ == '__main__':
    main()
