import base64
import tracemalloc
import urllist
import xml.etree.ElementTree as ET

tracemalloc.start()

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
        for event, elem in ET.iterparse(burpfile, events=("start","end")):
            if event == "start":
                continue
            if event == "end" and elem.tag == "url":
                if elem.text not in url_list:
                    url_list.append(elem.text)
                
            if event == "end" and elem.tag == "item":
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