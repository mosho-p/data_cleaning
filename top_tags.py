import pandas as pd
from collections import Counter
from glob import iglob

def main():
    filenames = iglob(input("Enter filename (wildcard * accepted): "))
    tags = count_hashtags(merge_files(filenames))
    print(tags.most_common(10))


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
    return [word[1:] for word in text.split() if (word[0]=='#' and word!='#') and not word[1].isdigit()] or None



if __name__ == '__main__':
    main()
