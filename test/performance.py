import pandas as pd
# import numpy as np
import json
import time
from bs4 import BeautifulSoup  # requires lxml
from email_reply_parser import EmailReplyParser


def profile():
    df = pd.read_csv('test.csv')
    ground = time.time()
    content = df.content.values[np.argmax([len(d) for d in df.content.values])]
    start = time.time()
    parser = EmailReplyParser(language='fr')
    print(str(time.time() - start) + 'init parser')
    start = time.time()
    res = parser.parse_reply(content)
    print(str(time.time() - start) + 'parse')
    start = time.time()
    soup = BeautifulSoup(res, 'lxml')
    text = soup.getText(' ')
    print(str(time.time() - start) + 'soup')
    print(f'Total time: {time.time() - ground}')


def verify():
    parser = EmailReplyParser(language='fi')
    texts = json.load(open('test/emails/emails.json'))
    texts = list(filter(lambda d: type(d) == str, texts))
    parsed = []
    for text in texts:
        print('-'*100)
        soup = BeautifulSoup(text, 'lxml')
        text = soup.getText('\n')
        text = parser.parse_reply(text)
        parsed.append(text)
        print(text)


def parse_df():
    parser = EmailReplyParser(language='en')
    path = 'test/emails/zipwrotetest.csv'
    df = pd.read_csv(path)
    parsed = []
    for text in df.sentence.values:
        soup = BeautifulSoup(text, 'lxml')
        text = soup.getText('\n')
        text = parser.parse_reply(text)
        parsed.append(text)
    df = df.assign(clean=parsed)
    df.to_csv(path)
    import code
    code.interact(local=locals())


def parse_json():
    parser = EmailReplyParser(language='en')
    with open('english.json', 'rb') as fl:
        messages = json.load(fl)
    parsed = []
    for text in messages:
        soup = BeautifulSoup(text, 'lxml')
        text = soup.getText('\n')
        text = parser.parse_reply(text)
        parsed.append(text)
    import code
    code.interact(local=locals())


def parse_text():
    parser = EmailReplyParser(language='en')
    with open('test/emails/caution.txt', 'r') as fl:
        message = fl.read()
    text = parser.parse_reply(message)
    print(text)


if __name__ == '__main__':
    parse_text()
    # parse_text()
