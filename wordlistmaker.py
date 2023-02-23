import argparse
import errno
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlparse


def print_result(wordlist):
    # print(wordlist)
    for k, v in wordlist.items():
        print("--------")
        print(k, ":", len(v))
        print("--------")
        for i in v:
            print(i)


def get_files(filename):
    try:
        with open(filename, encoding="utf 8") as f:
            tree = ET.parse(f)
            files = []
            for tag in tree.iter():

                # get file from url
                if tag.tag == "url":
                    words = urlparse(tag.text)
                    if Path(words.path).suffix:
                        if (
                            unquote(Path(words.path).name) not in files
                            and unquote(Path(words.path).name) != ""
                        ):
                            files.append(unquote(Path(words.path).name))
    except UnicodeDecodeError:
        sys.exit("Can't decode the content of the file.")
    except ET.ParseError:
        raise


def get_folders(filename):
    try:
        with open(filename, encoding="utf 8") as f:
            tree = ET.parse(f)
            folders = []
            for tag in tree.iter():

                # split urls based on '/' to get folders
                if tag.tag == "url":
                    words = urlparse(tag.text).path.split("/")
                    for word in words:
                        if word not in folders and word != "" and "." not in word:
                            folders.append(word)
                folders.sort()
            return folders
    except UnicodeDecodeError:
        sys.exit("Can't decode the content of the file.")
    except ET.ParseError:
        raise


# def split_path(urls):
#     folders = []
#     for url in urls:
#         words = urlparse(url).path.split("/")
#         for word in words:
#             if word not in folders and word != "" and "." not in word:
#                 folders.append(word)
#     folders.sort()
#     return folders


def parse_txt_file(filename, directories=False, files=False):
    directories_list = []
    files_list = []
    with open(filename, encoding="utf 8") as f:
        if directories:
            for line in f:
                url = line.strip()
                words = urlparse(url).path.split("/")
                for word in words:
                    if word not in directories_list and word != "" and "." not in word:
                        directories_list.append(word)
            return directories_list

        if files:
            for line in f:
                url = line.strip()
                word = Path(urlparse(url).path).name
                if word not in files_list and word != "" and "." in word:
                    files_list.append(word)
            return files_list


def start_cli_parser():
    parser = argparse.ArgumentParser(
        description="Take saved burpsuite requests and responses xml file as input. Create a list of directories, files, parameters names, parameters values, JSON keys or all of them as output."
    )
    parser.add_argument("filename", type=str, help="A saved burpsuite xml file.")
    parser.add_argument(
        "-d",
        "--directories",
        help="Print observed directories names.",
        action="store_true",
    )
    parser.add_argument(
        "-f", "--files", help="Print observed filenames.", action="store_true"
    )
    return parser


def wordstree():
    """Takes input from the cli, pass it to the parsing functions and then returns
    the wordlist.
    """
    wordlist = dict()
    directories = []
    files = []
    known_urls_list = []
    parser = start_cli_parser()
    args = vars(parser.parse_args())

    # If not empty, send the xml parsing functions
    try:
        if os.stat(args["filename"]).st_size == 0:
            sys.exit("The file is empty.")
        print("Parsing ", args["filename"], "...")
        if args["directories"]:
            directories = get_folders(args["filename"])
        if args["files"]:
            files = get_files(args["filename"])
    except FileNotFoundError:
        sys.exit("No such file or directory.")

    # If the xml parser raises a parsing error, send the file to the txt
    # parsing functions.
    except ET.ParseError:
        if args["directories"]:
            directories = parse_txt_file(args["filename"], True)
            wordlist["directories"] = directories

        elif args["files"]:
            files = parse_txt_file(args["filename"], False, True)
            wordlist["files"] = files

        print_result(wordlist)
    else:
        wordlist["directories"] = directories
        wordlist["files"] = files
        print_result(wordlist)


if __name__ == "__main__":
    wordstree()
