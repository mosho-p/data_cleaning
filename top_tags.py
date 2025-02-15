import pandas as pd
from collections import Counter
import sys
from glob import iglob
import string
import re

def main(n=10):
    filenames = iglob(input("Enter filename (wildcard * accepted): "))
    tags = count_hashtags(merge_files(filenames))
    hashtag_col_len = max(len('hashtag'), *map(len, [x for x, y in tags.most_common(n)]))  # used for formatting
    print('\n')  # Jupyter Notebooks didn't want to leave whitespace between input and output unless I did this
    print('hashtag'.ljust(hashtag_col_len) + ' | count')
    print('-'*(hashtag_col_len+len(' | count')))
    print(*[hashtag.ljust(hashtag_col_len) + ' | ' + str(count).rjust(5)
            for hashtag, count in tags.most_common(n)], sep='\n')


def merge_files(filenames):
    """
    Combines .json files and returns a list of text strings. the files must have a 'text' key
    :param filenames: (list) of filenames
    :return: (list) of text strings
    """
    output = []
    for f in filenames:
        df = pd.read_json(f, lines=True)
        output.extend(df.text)
    return output


def count_hashtags(tweets):
    """
    Takes a list of text strings and extracts the hashtags from them. Puts it into a Counter object
    :param tweets: (list) of text strings
    :return: (Counter) object with hashtag counts
    """
    output = Counter()
    for tweet in tweets:
        output.update(get_hashtags(tweet))
    return output


def get_hashtags(text):
    """
    Given one tweet, extract a list of hashtags
    :param text: (str) tweet
    :return: (list) hashtags or None
    """
    if text.strip()=='':
        return None

    # re.split(r'[{}]'.format(string.punctuation), word[1:], 1)[0].lower()
    # this line removes everything after punctuation and removes case sensitivity, which is how Twitter handles hashtags

    # if (word[0]=='#' and word!='#') and word[1] not in (string.digits+string.punctuation)
    # this conditional checks to see if the word starts with #, makes sure there is a character after,
    # and ensures that the first character is not a digit or punctuation to avoid returning empty strings

    return [re.split(r'[{}]'.format(string.punctuation), word[1:], 1)[0].lower() for word in text.split()
            if (word[0]=='#' and word!='#') and word[1] not in (string.digits+string.punctuation)] or None



if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv)>1 else 10
    main(n)
