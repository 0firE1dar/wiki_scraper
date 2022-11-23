import os
import logging
import re
from threading import Thread, Lock

import requests
from bs4 import BeautifulSoup
from typing import Optional

PREFIX = "https://en.wikipedia.org/"
RANDOM_WIKI_URL_PAGE = PREFIX + "wiki/Special:Random"

"""
1. root: url
2. child urls nodes

Print a visualized graph of all urls from root
"""
class HTMLNode:
    def __init__(self, url: str, child_links: None | dict) -> None:
        self.url = url
        self.child_links = child_links

def get_tree(url):
    try:
        res = requests.get(url=url)
    except Exception as err:
        logging.error(f"An error occured:\n {err}")
        os._exit(1)
    
    # In case using the random page url
    # assigning the new url from the request response
    url = res.url
    root = HTMLNode(url=url, child_links={})
    soup = BeautifulSoup(res.text, 'html.parser')
    links = parse_links(soup=soup)

    # TODO: Add caching with hashmap to store all already scanned links
    # scanned_pages = {}
    for link in links:
        # TODO: start a thread for each sub link of the root link
        root.child_links[link] = get_page(HTMLNode(url= link, child_links={}))
    print(f'\n\nAnd the final root is {root.url}\nChilds:{root.child_links}')


def get_page(node: HTMLNode):
    try:
        res = requests.get(url=node.url)
    except Exception as err:
        logging.error(f"An error occured:\n {err}")
        os._exit(1)

    soup = BeautifulSoup(res.text, 'html.parser')

    # print(f'Title: {soup.title.text}\n')
    logging.info(f"Succesfully fetched: {node.url}")
    links = parse_links(soup=soup)
    # print(f'The page "{soup.title.text}" contains the following links:\n{links}')
    return links


# Get all href links from the wikipedia paragraphs i.e all <p> html elements in page
def parse_links(soup) -> list:
    paragraphs = soup.find_all("p")
    parsed = []
    for p in paragraphs:
        links = p.find_all("a")
        for l in links:
            # l.get("href") returns suffix of URL such as: /Joe_Biden
            suffix = l.get("href")
            if suffix == None:
                logging.info("Skipping empty 'a' tag")
                continue
            url = PREFIX + suffix
            # Skip invalid suffixes such as reference links and others
            if is_valid_suffix(suffix):
                parsed.append(url)
                continue
            logging.info(f"Skipping invalid url format {url}")
    return parsed

def is_valid_suffix(url: str) -> bool:
    # See tests/test_main.py||test_urls to understand which urls cases are excluded
    r = re.compile("[\#|:|%|\?]")
    if r.search(url) == None:
        return True
    return False

if __name__ == "__main__":
    # TODO Add CLI argument parser to run the app through CLI
    # Use RANDOM_WIKI_URL_PAGE as default if no url is passed to CLI
    get_tree(RANDOM_WIKI_URL_PAGE)