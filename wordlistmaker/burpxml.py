import base64
import re
import tracemalloc
import urllist
from urllib.parse import unquote, urlparse
import xml.etree.ElementTree as ET

tracemalloc.start()

regex_str = r"""
  (?:"|')                               # Start newline delimiter
  (
    ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
    [^"'/]{1,}\.                        # Match a domainname (any character + dot)
    [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path
    |
    ((?:/|\.\./|\./)                    # Start with /,../,./
    [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
    [^"'><,;|()]{1,})                   # Rest of the characters can't be
    |
    ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
    [a-zA-Z0-9_\-/]{1,}                 # Resource name
    \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters
    |
    ([a-zA-Z0-9_\-/]{1,}/               # REST API (no extension) with /
    [a-zA-Z0-9_\-/]{3,}                 # Proper REST endpoints usually have 3+ chars
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters
    |
    ([a-zA-Z0-9_\-]{1,}                 # filename
    \.(?:php|asp|aspx|jsp|json|
         action|html|js|txt|xml)        # . + extension
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters
  )
  (?:"|')                               # End newline delimiter
"""

regex = re.compile(regex_str, re.VERBOSE)


def get_directories(burpfile):
    """
    description: accept a Burp Suite XML file or a txt file with a list of URLs and get all the directories
    parameters:
        filename: a Burp Suite XML file or a txt file with a list of URLs
    return: a list of strings (filenames)
    """
    url_list = []
    directories_list = []
    n = 0
    try:
        for event, elem in ET.iterparse(burpfile):
            if elem.tag == "url":
                if elem.text not in url_list:
                    url_list.append(elem.text)
            if elem.tag == "method":
                if elem.text == "GET":
                    continue

            if elem.tag == "response":
                if elem.attrib["base64"] == "true":
                    print(base64.b64decode(elem.text))
                else:
                    elem.text = unquote(elem.text)

                    print(elem.text)
                    # urls = regex.search(elem.text)
                    
                    # for url in urls:
                    #     if url not in url_list:
                    #         url_list.append(url)
                    # for url in url_list:
                    #     print(url)

            if elem.tag == "item":
                n += 1
            elem.clear()
        print("Reached the end", n, "times.")
        directories_list = urllist.get_directories(url_list)

        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        tracemalloc.stop()

    except ET.ParseError as err:
        print(err)
    return directories_list
