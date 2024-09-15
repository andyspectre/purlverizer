# Pu(r)lverizer

**Disclaimer**: this is totally a not finished tool and as of september 2024 I haven't look at it in a long while. This tool was started just to improve my python skills, understand better how certain things work and have fun. Other tools (also mentioned down below) will most probably work better than this.  

Pulverize every URL found in the requests and responses of a Burp Suite file to craft target specific wordlists, or find potentially interesting endpoints. At the moment this is an offline only tool that works by parsing Burp Suite project files or lists of URLs.

It can find:

-   Directories
-   Files
-   Parameter names
-   Parameter values
-   Endpoints
-   API endpoints
-   JSON keys
-   Custom regex

## Inspirations

- [Scavenger](https://github.com/0xDexter0us/Scavenger) by 0xDexter0us
- [LinkFinder](https://github.com/GerbenJavado/LinkFinder) by GerbenJavado
- [GAP](https://github.com/xnl-h4ck3r/GAP-Burp-Extension) and [xnLinkFinder](https://github.com/xnl-h4ck3r/xnLinkFinder) by xnl-h4ck3r

## Usage

```
usage: purlverizer.py [-h] (-b  | -u ) [-o] [-e] [-a] [-jk] [-d] [-p] [-v] [-f] [-A] [-r] [--in-scope [...]] [--no-numbers [...]] [--every-file] [--nonprintable]

pu(r)lverizer. Take a Burp Suite XML file and find potentially interesting stuff such as URLs or API endpoints; or pulverize every URL found in the requests and responses to craft target specific wordlists. You can also pass a list of URLs to create the wordlists.

options:
  -h, --help           show this help message and exit

General:
  These options can be used to specify the input and the output of the script.

  -b , --burp-file     Path to a Burp XML file
  -u , --urls-list     Path to a list of URLs
  -o , --output        Path where to save the output file

Actions:
  Use these options to specify what to do with the provided input. If no action is specified, the script will only print the URLs found in the provided input.

  -e, --endpoints      Search endpoints in a Burp XML file
  -a, --api            Search API endpoints inside JavaScript files found in Burp XML file
  -jk, --json-keys     Search JSON keys in a Burp XML file
  -d, --directories    Get a directories wordlist (both a URLs list and a Burp XML file are accepted)
  -p, --param-names    Get a parameters names wordlist (both a URLs list and a Burp XML file are accepted)
  -v, --param-values   Get a parameters values wordlist (both a URLs list and a Burp XML file are accepted)
  -f, --files          Get a files wordlist (both a URLs list and a Burp XML file are accepted)
  -A, --all            Find all (execute all the actions with no filters)
  -r , --regex         Regex pattern to search in the request body

Filters:
  These options can be used to filter the results

  --in-scope [ ...]    Specify one or more in-scope domains (e.g. --in-scope test.com test01.com)
  --no-numbers [ ...]  Exclude results that contain numbers. Accepted values: directories, files, param_names, param_values
  --every-file         Include results that contain every kind of file (such as jpg, png, etc.)
  --nonprintable       Include results that contain nonprintable characters
```

### Example usage:

Generate a wordlist of all directories found in the Burp Suite project file `burp_project.xml` and save it to the current directory:

```
python purlverizer.py -b burp_project.xml -d -o .
```

Find all endpoints (in all requests and responses) in the Burp Suite project file `burp_project.xml` and save it to the current directory:

```
python purlverizer.py -b burp_project.xml -e -o .
```

Generate a wordlist of all files found in a list of URLs and save it to the current directory:

```
python purlverizer.py -u urls.txt -f -o .
```

Generate a wordlist of all parameter values found in the Burp Suite project file `burp_project.xml`, excluding those that contains numbers, and save it to the current directory:

```
python purlverizer.py -b burp_project.xml -v --no-numbers param_values -o .
```


## Requirements

Pu(r)lverizer requires Python 3.6 or later.
