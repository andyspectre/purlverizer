# Pu(r)lverizer

Purlverizer is a tool that can help you generate custom wordlists based on various inputs. At the moment it's an offline only tool that works by parsing Burp Suite project files or lists of URLs.

It can find:

-   Directories
-   Files
-   Parameter names
-   Parameter values
-   Endpoints
-   API endpoints
-   JSON keys

## Inspirations

- [Scavenger](https://github.com/0xDexter0us/Scavenger) by 0xDexter0us
- [LinkFinder](https://github.com/GerbenJavado/LinkFinder) by GerbenJavado
- [GAP](https://github.com/xnl-h4ck3r/GAP-Burp-Extension) and [xnLinkFinder](https://github.com/xnl-h4ck3r/xnLinkFinder) by xnl-h4ck3r

## Usage

To use Pu(r)lverizer, run the script and pass in the appropriate command line arguments. The basic format is as follows:

```
python purlverizer.py [options]
```

Here are the available options:

### General Options

-   `-b`, `--burp-file`: Path to a Burp XML file
-   `-u`, `--urls-list`: Path to a list of URLs
-   `-o`, `--output`: Path where to save the output file

### Action Options

-   `-e`, `--endpoints`: Search endpoints in a Burp XML file
-   `-a`, `--api`: Search API endpoints inside JavaScript files found in Burp XML file
-   `-jk`, `--json-keys`: Search JSON keys in a Burp XML file
-   `-d`, `--directories`: Get a directories wordlist (both a URLs list and a Burp XML file are accepted)
-   `-p`, `--param-names`: Get a parameters names wordlist (both a URLs list and a Burp XML file are accepted)
-   `-v`, `--param-values`: Get a parameters values wordlist (both a URLs list and a Burp XML file are accepted)
-   `-f`, `--files`: Get a files wordlist (both a URLs list and a Burp XML file are accepted)
-   `-A`, `--all`: Find all (execute all the actions with no filters)

### Filter Options

-   `--in-scope`: Specify one or more in-scope domains (e.g. --in-scope test.com test01.com)
-   `--no-numbers`: Exclude results that contain numbers. Accepted values: directories, files, param\_names, param\_values
-   `--every-file`: Include results that contain every kind of file (such as jpg, png, etc.)
-   `--nonprintable`: Include results that contain nonprintable characters

For a detailed description of each option, run the script with the `-h` or `--help` option.

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
