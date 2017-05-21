from collections import Counter
from difflib import SequenceMatcher
from itertools import product
import re
import xml.etree.cElementTree as ET

IDENTICAL = 1.0
TOP_NUMBER = 10
RSS_FEED = 'rss.xml'
SIMILAR = 0.87
TAG_HTML = re.compile(r'<category>([^<]+)</category>')

def get_tags():
    """Find all tags (TAG_HTML) in RSS_FEED."""
    tree = ET.parse(RSS_FEED)
    return [elem.text for elem in tree.iter('category')]

def get_top_tags(tags):
    """Get the TOP_NUMBER of most common tags"""
    return Counter(tags).most_common(10)

def get_similarities(tags):
    """Find set of tags pairs with similarity ratio of > SIMILAR"""
    for i in product(tags, tags):
        if i[0][0] != i[1][0]:
            continue
        if SIMILAR < SequenceMatcher(a=i[0],b=i[1]).ratio() < 1:
            yield i

if __name__ == "__main__":
    tags = get_tags()
    top_tags = get_top_tags(tags)
    print('* Top {} tags:'.format(TOP_NUMBER))
    for tag, count in top_tags:
        print('{:<20} {}'.format(tag, count))
    first = get_similarities(tags)
    similar_tags = dict(get_similarities(tags))
    print('* Similar tags:')
    for singular, plural in similar_tags.items():
        print('{:<20} {}'.format(singular, plural))
