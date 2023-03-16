import argparse
import os
import sys
import tracemalloc
import re
import base64
import json
import re
import requests
from requests.packages import urllib3
import tracemalloc
from urllib.parse import unquote, quote, urlparse
from pathlib import Path
import xml.etree.ElementTree as ET


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

CHARS = [".", " ", "<", ">", "+", "*", ";", ":", '"', "{", "}", "|", "^", "`", "#"]

FIND_URLS = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s"()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[\\]?[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

URLS = re.compile(FIND_URLS)
JSON_PARSE = re.compile(r"JSON\.parse(\(\".+\"\);)")
TEXT_PLAIN = re.compile(r"Content-Type: text/plain")
# HOST_ESCAPED_TLD = re.compile(r"[a-zA-Z0-9-]+\\.[a-zA-Z]{2,}\.?[a-zA-Z]{0,2}")

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def print_result(wordlist):
    # print(wordlist)
    for k, v in wordlist.items():
        if len(v) > 0:
            print("--------")
            print(k, ":", len(v))
            print("--------")
            for i in v:
                print(i)


def check_url(url_list):
    urls = dict()

    for url in url_list:
        for char in url:
            if char in CHARS:
                char = quote(char)
        r = requests.head(url, proxies=proxies, verify=False)
        if r.status_code == requests.codes.ok:
            print(url, "ok")
            urls["ok"] = url
        else:
            print(url, "not ok")
            urls["not ok"] = url
    return urls


# 	# if the request succeeds
# 	if get.status_code == 200:
# 		return(f"{url}: is reachable")
# 	else:
# 		return(f"{url}: is Not reachable, status_code: {get.status_code}")

# #Exception
# except requests.exceptions.RequestException as e:
#     # print URL with Errs
# 	raise SystemExit(f"{url}: is Not reachable \nErr: {e}")


def parse_burp_file(burpfile):
    """
    description: accept a Burp Suite XML file or a txt file with a list of URLs and get all the directories
    parameters:
        filename: a Burp Suite XML file or a txt file with a list of URLs
    return: a list of strings (filenames)
    """
    url_list = []
    js_files = []
    false_positives = []
    urls_found = dict()
    html = False
    json = False
    n = 0
    try:
        for event, elem in ET.iterparse(burpfile):
            if elem.tag == "url" and elem.text not in url_list:
                url_list.append(elem.text)
            if elem.tag == "request" and elem.attrib["base64"] == "true":
                elem.text = str(base64.b64decode(elem.text))
                elem.text = unquote(elem.text)
                urls = URLS.findall(elem.text)
                for url in urls:
                    # if (
                    #     Path(urlparse(url).path).suffix in TLD
                    #     or Path(urlparse(url).netloc).suffix in TLD
                    # ):
                        if urlparse(url).scheme == "" and not urlparse(
                            url
                        ).path.startswith("."):
                            url = "https://" + url
                        elif urlparse(url).scheme == "" and urlparse(
                            url
                        ).path.startswith("."):
                            url = "https://www" + url
                        elif (
                            Path(urlparse(url).path).suffix != ".js"
                            and url not in url_list
                        ):
                            url_list.append(url)
                        elif (
                            Path(urlparse(url).path).suffix == ".js"
                            and url not in js_files
                        ):
                            js_files.append(url)
            
            if elem.tag == "response" and elem.attrib["base64"] == "true":
                elem.text = str(base64.b64decode(elem.text))
                elem.text = elem.text.replace("\\", "").replace("u002F", "/")
                # elem.text = elem.text.encode().decode("unicode-escape")
                urls = URLS.findall(elem.text)
                
                # print(elem.text)
                # elem.text = unquote(elem.text)
                
                # urls = URLS.findall(elem.text)
                # print(urls)
                for url in urls:
                    if (len(Path(urlparse(url).path).stem) == 1) and url not in false_positives:
                        false_positives.append(url)
                    elif (Path(urlparse(url).path).suffix != ".js" and url not in url_list and url not in false_positives):
                        url_list.append(url)
                    elif (Path(urlparse(url).path).suffix == ".js" and url not in js_files and url not in false_positives):
                        js_files.append(url)
                    

                    # if (
                    #     Path(urlparse(url).path).suffix in TLD
                    #     or Path(urlparse(url).netloc).suffix in TLD
                    # ):
                    #     if urlparse(url).scheme == "" and not urlparse(
                    #         url
                    #     ).path.startswith("."):
                    #         url = "https://" + url
                    #     elif urlparse(url).scheme == "" and urlparse(
                    #         url
                    #     ).path.startswith("."):
                    #         url = "https://www" + url
                    #     elif (
                    #         Path(urlparse(url).path).suffix != ".js"
                    #         and url not in url_list
                    #     ):
                    #         url_list.append(url)
                    #     elif (
                    #         Path(urlparse(url).path).suffix == ".js"
                    #         and url not in js_files
                    #     ):
                    #         js_files.append(url)
                
                # jsonparse = JSON_PARSE.findall(elem.text)
                # decoded = ""
                # for data in jsonparse:
                #     decoded = data.encode().decode("unicode-escape")               
                # urls_in_jsonparse = URLS.findall(decoded)                      
                # for urlmatch in urls_in_jsonparse:
                #     if (
                #         Path(urlparse(urlmatch).path).suffix != ".js"
                #         and urlmatch not in url_list
                #     ):
                #         url_list.append(urlmatch)
                #     elif (
                #         Path(urlparse(urlmatch).path).suffix == ".js"
                #         and urlmatch not in js_files
                #     ):
                #         js_files.append(urlmatch)
                # print(elem.text)
                # host_only_in_js = HOST_ESCAPED_TLD.findall(elem.text)
                

                
                # hosts_in_js = []
                # for host_tld in host_only_in_js:
                #     if (
                #         Path(urlparse(host_tld).path).suffix != ".js"
                #         and host_tld not in url_list
                #     ):
                #         url_list.append(host_tld)
                #     elif (
                #         Path(urlparse(host_tld).path).suffix == ".js"
                #         and host_tld not in js_files
                #     ):
                #         js_files.append(host_tld)
                    
            elif elem.tag == "response" and elem.attrib["base64"] == "false":
                print(
                    'Looks like the requests and responses are not Base64 encoded. To get more results, make sure to select "Base64-encode requests and responses" when saving the items from Burp Suite Site map.'
                )
            if elem.tag == "item":
                n += 1
            elem.clear()
        print("Reached the end", n, "times.")

    except ET.ParseError as err:
        print(err)

    urls_found["urls"] = url_list
    urls_found["javascript files"] = js_files
    urls_found["probably false positives"] = false_positives
    return urls_found
    # with open('urls_test_list.txt', 'w') as filehandle:
    #     for url in urls_found["urls"]:
    #         filehandle.writelines(f"{url}\n")


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


def get_directories(url_list):
    """
    description: accept a Burp Suite XML file or a txt file with a list of URLs and get all the directories
    parameters:
        filename: a Burp Suite XML file or a txt file with a list of URLs
    return: a list of strings (filenames)
    """
    directories_list = []

    for url in url_list:
        words = urlparse(url).path.split("/")
        for word in words:
            # Non sono sicuro se voglio decodificare o no. Per decodificare, uncommentare la riga sotto.
            # word = unquote(word)

            if word not in directories_list and word != "" and "." not in word:
                directories_list.append(word)
    directories_list.sort()
    return directories_list


def get_files(url_list):
    """
    description: accept a Burp Suite XML file or a txt file with a list of URLs and get all the directories.
    parameters:
        filename: a Burp Suite XML file or a txt file with a list of URLs
    return: a list of strings (filenames)
    """
    files_list = []
    for url in url_list:
        # word = unquote(Path(urlparse(url).path).name) -> non sono sicuro se voglio decodificare o no
        word = Path(urlparse(url).path).name
        if word not in files_list and word != "" and "." in word:
            files_list.append(word)
    files_list.sort()
    return files_list


def get_param_names(url_list):
    param_names_list = []
    for url in url_list:
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


def get_param_values(url_list):
    param_values_list = []
    for url in url_list:
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


def command_line_parser():
    parser = argparse.ArgumentParser(
        description="Take a list of URLs or a Burp Suite XML file as input and get a list of: directories, files, parameters names, parameters values and links."
    )
    parser.add_argument("-u", "--url", help="Path to a list of URLs.")
    parser.add_argument("-x", "--xml", help="Path to a Burp XML file.")
    parser.add_argument(
        "-l",
        "--list-of-urls",
        help="find all URLs from the Burp file",
        action="store_true",
    )
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


def main():
    """Takes input from the cli, pass it to the parsing functions and then returns
    the wordlist.
    """
    wordlist = dict()
    directories_list = []
    files_list = []
    param_names_list = []
    param_values_list = []
    burp_request_response = []
    javascript_files = []
    # new_urls = []
    parser = command_line_parser()
    args = vars(parser.parse_args())

    try:
        if args["xml"]:
            if os.stat(args["xml"]).st_size == 0:
                sys.exit("The file is empty.")
            burp_request_response = parse_burp_file(args["xml"])

        elif args["url"]:
            if os.stat(args["url"]).st_size == 0:
                sys.exit("The file is empty.")
            with open((args["url"]), encoding="utf 8") as f:
                url_list = []
                print("Parsing ", args["url"], "...")
                for line in f:
                    url = line.strip()
                    url_list.append(url)
                if args["directories"]:
                    directories_list = get_directories(url_list)
                if args["files"]:
                    files_list = get_files(url_list)
                if args["param_names"]:
                    param_names_list = get_param_names(url_list)
                if args["param_values"]:
                    param_values_list = get_param_values(url_list)
                if args["no_numbers"]:
                    if "dirs" in args["no_numbers"]:
                        directories_list = remove_numbers(directories_list)
                    if "files" in args["no_numbers"]:
                        files_list = remove_numbers(files_list)
                    if "param-names" in args["no_numbers"]:
                        param_names_list = remove_numbers(param_names_list)
                    if "param-values" in args["no_numbers"]:
                        param_values_list = remove_numbers(param_values_list)
                if args["nonprintable"]:
                    directories_list = remove_nonprintable_chars(directories_list)
                    files_list = remove_nonprintable_chars(files_list)
                    param_names_list = remove_nonprintable_chars(param_names_list)
                    param_values_list = remove_nonprintable_chars(param_values_list)
                if args["all_files"]:
                    files_list = show_all_files(files_list)
        else:
            parser.print_help()
            sys.exit()
    except FileNotFoundError:
        sys.exit("No such file or directory.")

    wordlist["directories"] = directories_list
    wordlist["file"] = files_list
    wordlist["param names"] = param_names_list
    wordlist["param values"] = param_values_list
    for url, li in burp_request_response.items():
        wordlist[url] = li

    print_result(wordlist)

    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
    tracemalloc.stop()


if __name__ == "__main__":
    main()
