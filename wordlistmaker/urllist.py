from pathlib import Path
from urllib.parse import unquote, urlparse

def get_directories(read_data):
    """
    description: accept a Burp Suite XML file or a txt file with a list of URLs and get all the directories
    parameters:
        filename: a Burp Suite XML file or a txt file with a list of URLs
    return: a list of strings (filenames)
    """
    directories_list = []

    for url in read_data.split("\n"):
        words = urlparse(url).path.split("/")
        for word in words:
            # Non sono sicuro se voglio decodificare o no. Per decodificare, uncommentare la riga sotto.
            # word = unquote(word)

            if word not in directories_list and word != "" and "." not in word:
                directories_list.append(word)
    directories_list.sort()
    return directories_list


def get_files(read_data):
    """
    description: accept a Burp Suite XML file or a txt file with a list of URLs and get all the directories.
    parameters:
        filename: a Burp Suite XML file or a txt file with a list of URLs
    return: a list of strings (filenames)
    """
    files_list = []
    for url in read_data.split("\n"):
        # word = unquote(Path(urlparse(url).path).name) -> non sono sicuro se voglio decodificare o no
        word = Path(urlparse(url).path).name
        if word not in files_list and word != "" and "." in word:
            files_list.append(word)
    files_list.sort()
    return files_list


def get_param_names(read_data):
    param_names_list = []
    for url in read_data.split("\n"):
        query = urlparse(url).query.replace("=", "&").split("&")
        if query[0] == "":
            pass
        elif len(query) == 2:
            if query[0] not in param_names_list:
                param_names_list.append(query[0])
        else:
            query = query[::2]
            for param in query:
                if param not in param_names_list:
                    param_names_list.append(param)
    param_names_list.sort()
    return param_names_list


def get_param_values(read_data):  
    param_values_list = []
    for url in read_data.split("\n"):
        query = urlparse(url).query.replace("=", "&").split("&")
        if query[0] == "":
            pass
        elif len(query) == 2:
            if query[1] not in param_values_list:
                param_values_list.append(query[1])
        else:
            query = query[1::2]
            for param in query:
                if param not in param_values_list:
                    param_values_list.append(param)
    param_values_list.sort()
    return param_values_list