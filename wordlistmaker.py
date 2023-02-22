import argparse
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
        return files


def get_folders(filename):
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

def split_path(urls):
    folders = []
    for url in urls:
        words = urlparse(url).path.split("/")
        for word in words:
            if word not in folders and word != "" and "." not in word:
                folders.append(word)
    folders.sort()
    return folders

def read_file(filename):
    list_of_urls = []
    with open(filename, encoding="utf 8") as f:
        for line in f:
            url = line.strip()
            list_of_urls.append(url)
    return list_of_urls

def start_cli_parser():
    parser = argparse.ArgumentParser(
        description="Take saved burpsuite requests and responses xml file as input. Create a list of directories, files, parameters names, parameters values, JSON keys or all of them as output."
    )
    parser.add_argument("filename", type=str, help="A saved burpsuite xml file.")
    parser.add_argument(
        "-F", "--folders", help="Print observed folders names.", action="store_true"
    )
    parser.add_argument(
        "-f", "--files", help="Print observed filenames.", action="store_true"
    )
    return parser


def wordstree():
    wordlist = dict()
    folders = []
    files = []
    parser = start_cli_parser()
    args = vars(parser.parse_args())
    try:
        print("Parsing ", args["filename"],"...")
        if args["folders"]:
            folders = get_folders(args["filename"])
        if args["files"]:
            files = get_files(args["filename"])
    except ET.ParseError:
        pass
    try:
        list_of_urls = read_file(args["filename"])
        if args["folders"]:
            folders = split_path(list_of_urls)
    except:
        print("error")

    wordlist["folders"] = folders
    wordlist["files"] = files
    print_result(wordlist)


if __name__ == "__main__":
    wordstree()
