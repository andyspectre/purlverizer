import argparse


def start_cli_parser():
    parser = argparse.ArgumentParser(
        description="Take a list of URLs or a Burp Suite XML file as input and get a list of: directories, files, parameters names, parameters values and links."
    )
    parser.add_argument(
        "-u", "--url", help="Path to a list of URLs."
    )
    parser.add_argument(
        "-x", "--xml", help="Path to a Burp XML file."
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
