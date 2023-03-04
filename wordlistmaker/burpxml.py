import urllist
import xml.etree.ElementTree as ET


def get_directories(burpfile):
    """
    description: accept a Burp Suite XML file or a txt file with a list of URLs and get all the directories
    parameters:
        filename: a Burp Suite XML file or a txt file with a list of URLs
    return: a list of strings (filenames)
    """
    directories_list = []
    try:
        for event, elem in ET.iterparse(burpfile, events=("start", "end")):
            if event == "start":
                if elem.tag == "url":
                    if elem.text =="GET":
                        directories_list.append(elem.text)    
    except ET.ParseError as err:
        print(err)
    return directories_list

    # try:
    #     with open(filename, encoding="utf 8") as f:
    #         tree = ET.parse(f)
    #         files = []
    #         for tag in tree.iter():
    #             # get file from url
    #             if tag.tag == "url":
    #                 words = urlparse(tag.text)
    #                 if Path(words.path).suffix:
    #                     if (
    #                         unquote(Path(words.path).name) not in files
    #                         and unquote(Path(words.path).name) != ""
    #                     ):
    #                         files.append(unquote(Path(words.path).name))
    # except UnicodeDecodeError:
    #     sys.exit("Can't decode the content of the file.")
    # except ET.ParseError:
    #     raise

    # def get_directories(read_data):
    
    # directories_list = []

    # for url in read_data.split("\n"):
    #     words = urlparse(url).path.split("/")
    #     for word in words:
    #         # Non sono sicuro se voglio decodificare o no. Per decodificare, uncommentare la riga sotto.
    #         # word = unquote(word)

    #         if word not in directories_list and word != "" and "." not in word:
    #             directories_list.append(word)
    # directories_list.sort()
    # return directories_list