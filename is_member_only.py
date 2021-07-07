#!/usr/bin/env python
import os

target_URL = input("Enter URL\n> ")
target_URL_HTML = os.popen("curl " + target_URL).read()

memberonly_element = "article class=\"meteredContent\""

if target_URL_HTML.find(memberonly_element) == -1:
    print("This article is FREE")
else: 
    print ("This article is member only :(")


