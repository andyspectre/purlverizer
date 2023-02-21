import argparse
import xml.etree.ElementTree as ET


def read_file():
    with open("test", encoding="utf 8") as f:
        tree = ET.parse(f)
        for item in tree.findall("item"):
            print(item.findtext("url"))


def start_cli_parser():
    parser = argparse.ArgumentParser(
        description="Take saved burpsuite requests and responses xml file as input. Create a list of directories, files, parameters names, parameters values, JSON keys or all of them as output."
    )
    parser.add_argument("filename", type=str, help="A saved burpsuite xml file.")
    parser.add_argument(
        "-f", "--folders", help="Print observed folders names.", action="store_true"
    )
    return parser


def wordstree():
    parser = start_cli_parser()
    args = vars(parser.parse_args())
    # myfile = read_file(args["filename"])


if __name__ == "__main__":
    read_file()
