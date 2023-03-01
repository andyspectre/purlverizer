import argparse
import errno
import os
import re
import sys
import tracemalloc
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlparse


tracemalloc.start()

COMMON_EXTENSIONS = [
    ".asp",
    ".aspx",
    ".bak" ".bat",
    ".c",
    ".cfm",
    ".cgi",
    ".css",
    ".com",
    ".dll",
    ".do",
    ".exe",
    ".htm",
    ".html",
    ".inc",
    ".jhtml",
    ".js",
    ".jsa",
    ".json",
    ".jsp",
    ".log",
    ".mdb",
    ".nsf",
    ".old",
    ".pcap",
    ".php",
    ".php2",
    ".php3",
    ".php4",
    ".php5",
    ".php6",
    ".php7",
    ".phps",
    ".pht",
    ".phtml",
    ".pl",
    ".reg",
    ".sh",
    ".shtml",
    ".sql",
    ".swf",
    ".txt",
    ".xml",
]

# Tengo questa solo come esempio di utilizzo di xml.etree
#
# def get_files(filename):
#     try:
#         with open(filename, encoding="utf 8") as f:
#             tree = ET.parse(f)
#             files = []
#             for tag in tree.iter():
#                 # get file from url
#                 if tag.tag == "url":
#                     words = urlparse(tag.text)
#                     if Path(words.path).suffix:
#                         if (
#                             unquote(Path(words.path).name) not in files
#                             and unquote(Path(words.path).name) != ""
#                         ):
#                             files.append(unquote(Path(words.path).name))
#     except UnicodeDecodeError:
#         sys.exit("Can't decode the content of the file.")
#     except ET.ParseError:
#         raise


def print_result(wordlist):
    # print(wordlist)
    for k, v in wordlist.items():
        print("--------")
        print(k, ":", len(v))
        print("--------")
        for i in v:
            print(i)


def show_all_files(files_list):
    """description: accept a list of strings (filenames) and return a new list containing only strings that contains certain whitelisted pattern (file extension).
    parameters:
        files_list: a list of strings
    return: a list of strings (original wordlist - strings that don't contain the whitelisted pattern)
    """
    all_files_list = [f for f in files_list if Path(f).suffix in COMMON_EXTENSIONS]
    return all_files_list


def remove_nonprintable_chars(wordlist):
    """
    description: accept a list of strings (a wordlist) and return a new list containing only strings with printable characters.
    parameters:
        wordlist: a list of strings
    return: a list of strings (original wordlist - strings with nonprintable characters)
    """

    no_nonprintable_wordlist = [word for word in wordlist if word.isprintable()]
    return no_nonprintable_wordlist


def remove_numbers(wordlist):
    """
    description: accept a list of strings (a wordlist) and return a new list containing only number-less strings.
    parameters:
        wordlist: a list of strings
    return: a list of strings (original wordlist - strings with numbers)
    """
    no_numbers_wordlist = [
        word for word in wordlist if not bool(re.search(r"\d", word))
    ]
    return no_numbers_wordlist


def get_directories(read_data):
    """
    description: accept a Burp Suite XML file or a txt file with a list of URLs and get all the directories.
    parameters:
        filename: a Burp Suite XML file or a txt file with a list of URLs
    return: a list of strings (filenames)
    """
    directories_list = []

    for url in read_data.split("\n"):
        words = urlparse(url).path.split("/")
        for word in words:
            # word = unquote(word) -> non sono sicuro se voglio decodificare o no

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
        param_name_and_value = urlparse(url).query.replace("=", "&").split("&")
        if param_name_and_value[0] == "":
            pass
        elif len(param_name_and_value) == 2:
            if param_name_and_value[0] not in param_names_list:
                param_names_list.append(param_name_and_value[0])
        else:
            param_name_and_value = param_name_and_value[::2]
            for param in param_name_and_value:
                if param not in param_names_list:
                    param_names_list.append(param)
    param_names_list.sort()
    return param_names_list


def parse_txt_file(
    filename, directories=False, files=False, param_names=False, param_values=False
):
    directories_list = []
    files_list = []
    param_name_only_list = []

    # if param_values:
    #     for line in f:
    #         url = line.strip()
    #         param_name_and_value = urlparse(url).query.replace("&", "=").split("=")
    #         param_value_only_list = param_name_and_value[1::2]
    #     return param_value_only_list


def start_cli_parser():
    parser = argparse.ArgumentParser(
        description="Take a list of URLs or a Burp Suite XML file as input and get a list of: directories, files, parameters names, parameters values and links."
    )
    parser.add_argument(
        "-u", "--url", help="Path to the URLs list or to the Burp Suite XML file.")
    parser.add_argument(
        "-d",
        "--directories",
        help="Get a list of directories.",
        action="store_true",
    )
    parser.add_argument(
        "-f", "--files", help="Get a list of file names", action="store_true"
    )
    parser.add_argument(
        "-p",
        "--param-names",
        help="Get a list of parameter names.",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--param-values",
        help="Get a list of parameter values.",
        action="store_true",
    )
    parser.add_argument(
        "--no-numbers",
        help="Exclude results that contain numbers. Accepted values: dirs, files, param-names, param-values",
        nargs="*",
    )
    parser.add_argument(
        "--nonprintable",
        help="Include results that contain nonprintable characters.",
        action="store_false",
    )
    parser.add_argument(
        "--all-files",
        # di default off ma immagino che tutti vogliano vedere "all kind of files..."
        # forse meglio di default visualizzarli tutti e aggiungere un "filter most common"
        help="Include results that contain all kind of files.",
        action="store_false",
    )

    return parser


def wordstree():
    """Takes input from the cli, pass it to the parsing functions and then returns
    the wordlist.
    """
    wordlist = dict()
    directories_list = []
    files_list = []
    param_names_list = []
    param_values_list = []
    parser = start_cli_parser()
    args = vars(parser.parse_args())

    try:
        if os.stat(args["url"]).st_size == 0:
            sys.exit("The file is empty.")
        with open((args["url"]), encoding="utf 8") as f:
            print("Parsing ", args["url"], "...")
            read_data = f.read()
            if args["directories"]:
                directories_list = get_directories(read_data)
            if args["files"]:
                files_list = get_files(read_data)
            if args["param_names"]:
                param_names_list = get_param_names(read_data)

    except FileNotFoundError:
        sys.exit("No such file or directory.")
    else:
        if args["no_numbers"] == "dirs":
            directories_list = remove_numbers(directories_list)
        if args["no_numbers"] == "files":
            files_list = remove_numbers(files_list)
        if args["no_numbers"] == "param-names":
            param_names_list = remove_numbers(param_names_list)
        if args["nonprintable"]:
            directories_list = remove_nonprintable_chars(directories_list)
            files_list = remove_nonprintable_chars(files_list)
        if args["all_files"]:
            files_list = show_all_files(files_list)
        wordlist["directories"] = directories_list
        wordlist["file"] = files_list
        wordlist["param names"] = param_names_list
        print_result(wordlist)

        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        tracemalloc.stop()


if __name__ == "__main__":
    wordstree()
