import errno
import os
import sys
import tracemalloc
import burpxml
import cliparser
import filters
import output
import urllist



def wordstree():
    """Takes input from the cli, pass it to the parsing functions and then returns
    the wordlist.
    """
    wordlist = dict()
    directories_list = []
    files_list = []
    param_names_list = []
    param_values_list = []
    # new_urls = []
    parser = cliparser.start_cli_parser()
    args = vars(parser.parse_args())

    try:
        if args["xml"]:
            if os.stat(args["xml"]).st_size == 0:
                sys.exit("The file is empty.")
            if args["directories"]:
                directories_list = burpxml.get_directories(args["xml"])
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
                    directories_list = urllist.get_directories(url_list)
                if args["files"]:
                    files_list = urllist.get_files(url_list)
                if args["param_names"]:
                    param_names_list = urllist.get_param_names(url_list)
                if args["param_values"]:
                    param_values_list = urllist.et_param_values(url_list)
                if args["no_numbers"]:
                    if "dirs" in args["no_numbers"]:
                        directories_list = filters.remove_numbers(directories_list)
                    if "files" in args["no_numbers"]:
                        files_list = filters.remove_numbers(files_list)
                    if "param-names" in args["no_numbers"]:
                        param_names_list = filters.remove_numbers(param_names_list)
                    if "param-values" in args["no_numbers"]:
                        param_values_list = filters.remove_numbers(param_values_list)
                if args["nonprintable"]:
                    directories_list = filters.remove_nonprintable_chars(directories_list)
                    files_list = filters.remove_nonprintable_chars(files_list)
                    param_names_list = filters.remove_nonprintable_chars(param_names_list)
                    param_values_list = filters.remove_nonprintable_chars(param_values_list)
                if args["all_files"]:
                    files_list = filters.show_all_files(files_list)   
        else:
            parser.print_help()
            sys.exit()
    except FileNotFoundError:
        sys.exit("No such file or directory.")

    wordlist["directories"] = directories_list
    wordlist["file"] = files_list
    wordlist["param names"] = param_names_list
    wordlist["param values"] = param_values_list

    output.print_result(wordlist)

