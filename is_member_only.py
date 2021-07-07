#!/usr/bin/env python

import os
import sys
import re
import argparse
import urllib.parse

parser = argparse.ArgumentParser(description='Check if an article on Medium is member-only.')
parser.add_argument("url", help="Article's URL to check")
args = parser.parse_args()

# Fetch URL

target_URL = args.url
target_URL_HTML = None
memberonly_element = "article class=\"meteredContent\""

def is_googlesearch_url(url):
    if url.startswith("https://www.google.com/url?"):
        return True

def parse_googlesearch_url(url):
    raw_url = re.search("url\=(.*)\&usg", url)
    encoded_url = raw_url.group(1)
    decoded_url = urllib.parse.unquote(encoded_url)
    return decoded_url


def fetch_URL(url):
    global target_URL_HTML
    target_URL_HTML = os.popen("curl -L " + target_URL).read()
    saveLog = open("/home/farhan/scripts/ismember.log.html", "w")
    saveLog.write(target_URL_HTML)
    saveLog.close()

def checkURL(url):
    return re.search("^(https?://)?(www\.)?medium\.com", url)

def checkMetadata(html):
    return target_URL_HTML.find("<meta data-rh=\"true\" property=\"og:site_name\" content=\"Medium\"/>")

def check_member_only(html):
    if target_URL_HTML == None:
        fetch_URL(target_URL)
    
    return target_URL_HTML.find(memberonly_element)

## Check if it's a Google Search URL
if is_googlesearch_url(target_URL):
    target_URL = parse_googlesearch_url(target_URL)

# Check if it's a Medium

## Check URL
if checkURL(target_URL) == None:
    print("This is not Medium's domain name, continue analyzing...")
    ## Check Metadata
    print("\nFetching Metadata...")
    fetch_URL(target_URL)
    if checkMetadata(target_URL) == -1:
        print("\nMedium's metadata is missing!")
        print("This is not a Medium Site, exiting...")
        sys.exit()
    else:
        print("Analyzing Metadata...")
else:
    print("Medium's domain name found")

# Verification test Passed, this article is in medium.
print("Domain Verified: This domain is hosted on Medium Platform")
# Proceed to check for Member-Only content

if target_URL_HTML == None:
    print("\nFetching Metadata...")
    fetch_URL(target_URL)
    print("Analyzing Metadata...")

if check_member_only(target_URL_HTML) == -1:
    print("\nMember-Only Check Completed")
    print("This article is FREE")
else:
    print("\nMember-Only Check Completed")
    print ("Result: This article is Member-Only (⌣́_⌣̀) ")
