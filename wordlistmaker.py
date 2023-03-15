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
from pathlib import Path
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
TLD = [
    ".aaa",
    ".aarp",
    ".abarth",
    ".abb",
    ".abbott",
    ".abbvie",
    ".abc",
    ".able",
    ".abogado",
    ".abudhabi",
    ".ac",
    ".academy",
    ".accenture",
    ".accountant",
    ".accountants",
    ".aco",
    ".actor",
    ".ad",
    ".ads",
    ".adult",
    ".ae",
    ".aeg",
    ".aero",
    ".aetna",
    ".af",
    ".afl",
    ".africa",
    ".ag",
    ".agakhan",
    ".agency",
    ".ai",
    ".aig",
    ".airbus",
    ".airforce",
    ".airtel",
    ".akdn",
    ".al",
    ".alfaromeo",
    ".alibaba",
    ".alipay",
    ".allfinanz",
    ".allstate",
    ".ally",
    ".alsace",
    ".alstom",
    ".am",
    ".amazon",
    ".americanexpress",
    ".americanfamily",
    ".amex",
    ".amfam",
    ".amica",
    ".amsterdam",
    ".analytics",
    ".android",
    ".anquan",
    ".anz",
    ".ao",
    ".aol",
    ".apartments",
    ".app",
    ".apple",
    ".aq",
    ".aquarelle",
    ".ar",
    ".arab",
    ".aramco",
    ".archi",
    ".army",
    ".arpa",
    ".art",
    ".arte",
    ".as",
    ".asda",
    ".asia",
    ".associates",
    ".at",
    ".athleta",
    ".attorney",
    ".au",
    ".auction",
    ".audi",
    ".audible",
    ".audio",
    ".auspost",
    ".author",
    ".auto",
    ".autos",
    ".avianca",
    ".aw",
    ".aws",
    ".ax",
    ".axa",
    ".az",
    ".azure",
    ".ba",
    ".baby",
    ".baidu",
    ".banamex",
    ".bananarepublic",
    ".band",
    ".bank",
    ".bar",
    ".barcelona",
    ".barclaycard",
    ".barclays",
    ".barefoot",
    ".bargains",
    ".baseball",
    ".basketball",
    ".bauhaus",
    ".bayern",
    ".bb",
    ".bbc",
    ".bbt",
    ".bbva",
    ".bcg",
    ".bcn",
    ".bd",
    ".be",
    ".beats",
    ".beauty",
    ".beer",
    ".bentley",
    ".berlin",
    ".best",
    ".bestbuy",
    ".bet",
    ".bf",
    ".bg",
    ".bh",
    ".bharti",
    ".bi",
    ".bible",
    ".bid",
    ".bike",
    ".bing",
    ".bingo",
    ".bio",
    ".biz",
    ".bj",
    ".black",
    ".blackfriday",
    ".blockbuster",
    ".blog",
    ".bloomberg",
    ".blue",
    ".bm",
    ".bms",
    ".bmw",
    ".bn",
    ".bnpparibas",
    ".bo",
    ".boats",
    ".boehringer",
    ".bofa",
    ".bom",
    ".bond",
    ".boo",
    ".book",
    ".booking",
    ".bosch",
    ".bostik",
    ".boston",
    ".bot",
    ".boutique",
    ".box",
    ".br",
    ".bradesco",
    ".bridgestone",
    ".broadway",
    ".broker",
    ".brother",
    ".brussels",
    ".bs",
    ".bt",
    ".build",
    ".builders",
    ".business",
    ".buy",
    ".buzz",
    ".bv",
    ".bw",
    ".by",
    ".bz",
    ".bzh",
    ".ca",
    ".cab",
    ".cafe",
    ".cal",
    ".call",
    ".calvinklein",
    ".cam",
    ".camera",
    ".camp",
    ".canon",
    ".capetown",
    ".capital",
    ".capitalone",
    ".car",
    ".caravan",
    ".cards",
    ".care",
    ".career",
    ".careers",
    ".cars",
    ".casa",
    ".case",
    ".cash",
    ".casino",
    ".cat",
    ".catering",
    ".catholic",
    ".cba",
    ".cbn",
    ".cbre",
    ".cbs",
    ".cc",
    ".cd",
    ".center",
    ".ceo",
    ".cern",
    ".cf",
    ".cfa",
    ".cfd",
    ".cg",
    ".ch",
    ".chanel",
    ".channel",
    ".charity",
    ".chase",
    ".chat",
    ".cheap",
    ".chintai",
    ".christmas",
    ".chrome",
    ".church",
    ".ci",
    ".cipriani",
    ".circle",
    ".cisco",
    ".citadel",
    ".citi",
    ".citic",
    ".city",
    ".cityeats",
    ".ck",
    ".cl",
    ".claims",
    ".cleaning",
    ".click",
    ".clinic",
    ".clinique",
    ".clothing",
    ".cloud",
    ".club",
    ".clubmed",
    ".cm",
    ".cn",
    ".co",
    ".coach",
    ".codes",
    ".coffee",
    ".college",
    ".cologne",
    ".com",
    ".comcast",
    ".commbank",
    ".community",
    ".company",
    ".compare",
    ".computer",
    ".comsec",
    ".condos",
    ".construction",
    ".consulting",
    ".contact",
    ".contractors",
    ".cooking",
    ".cookingchannel",
    ".cool",
    ".coop",
    ".corsica",
    ".country",
    ".coupon",
    ".coupons",
    ".courses",
    ".cpa",
    ".cr",
    ".credit",
    ".creditcard",
    ".creditunion",
    ".cricket",
    ".crown",
    ".crs",
    ".cruise",
    ".cruises",
    ".cu",
    ".cuisinella",
    ".cv",
    ".cw",
    ".cx",
    ".cy",
    ".cymru",
    ".cyou",
    ".cz",
    ".dabur",
    ".dad",
    ".dance",
    ".data",
    ".date",
    ".dating",
    ".datsun",
    ".day",
    ".dclk",
    ".dds",
    ".de",
    ".deal",
    ".dealer",
    ".deals",
    ".degree",
    ".delivery",
    ".dell",
    ".deloitte",
    ".delta",
    ".democrat",
    ".dental",
    ".dentist",
    ".desi",
    ".design",
    ".dev",
    ".dhl",
    ".diamonds",
    ".diet",
    ".digital",
    ".direct",
    ".directory",
    ".discount",
    ".discover",
    ".dish",
    ".diy",
    ".dj",
    ".dk",
    ".dm",
    ".dnp",
    ".do",
    ".docs",
    ".doctor",
    ".dog",
    ".domains",
    ".dot",
    ".download",
    ".drive",
    ".dtv",
    ".dubai",
    ".dunlop",
    ".dupont",
    ".durban",
    ".dvag",
    ".dvr",
    ".dz",
    ".earth",
    ".eat",
    ".ec",
    ".eco",
    ".edeka",
    ".edu",
    ".education",
    ".ee",
    ".eg",
    ".email",
    ".emerck",
    ".energy",
    ".engineer",
    ".engineering",
    ".enterprises",
    ".epson",
    ".equipment",
    ".er",
    ".ericsson",
    ".erni",
    ".es",
    ".esq",
    ".estate",
    ".et",
    ".etisalat",
    ".eu",
    ".eurovision",
    ".eus",
    ".events",
    ".exchange",
    ".expert",
    ".exposed",
    ".express",
    ".extraspace",
    ".fage",
    ".fail",
    ".fairwinds",
    ".faith",
    ".family",
    ".fan",
    ".fans",
    ".farm",
    ".farmers",
    ".fashion",
    ".fast",
    ".fedex",
    ".feedback",
    ".ferrari",
    ".ferrero",
    ".fi",
    ".fiat",
    ".fidelity",
    ".fido",
    ".film",
    ".final",
    ".finance",
    ".financial",
    ".fire",
    ".firestone",
    ".firmdale",
    ".fish",
    ".fishing",
    ".fit",
    ".fitness",
    ".fj",
    ".fk",
    ".flickr",
    ".flights",
    ".flir",
    ".florist",
    ".flowers",
    ".fly",
    ".fm",
    ".fo",
    ".foo",
    ".food",
    ".foodnetwork",
    ".football",
    ".ford",
    ".forex",
    ".forsale",
    ".forum",
    ".foundation",
    ".fox",
    ".fr",
    ".free",
    ".fresenius",
    ".frl",
    ".frogans",
    ".frontdoor",
    ".frontier",
    ".ftr",
    ".fujitsu",
    ".fun",
    ".fund",
    ".furniture",
    ".futbol",
    ".fyi",
    ".ga",
    ".gal",
    ".gallery",
    ".gallo",
    ".gallup",
    ".game",
    ".games",
    ".gap",
    ".garden",
    ".gay",
    ".gb",
    ".gbiz",
    ".gd",
    ".gdn",
    ".ge",
    ".gea",
    ".gent",
    ".genting",
    ".george",
    ".gf",
    ".gg",
    ".ggee",
    ".gh",
    ".gi",
    ".gift",
    ".gifts",
    ".gives",
    ".giving",
    ".gl",
    ".glass",
    ".gle",
    ".global",
    ".globo",
    ".gm",
    ".gmail",
    ".gmbh",
    ".gmo",
    ".gmx",
    ".gn",
    ".godaddy",
    ".gold",
    ".goldpoint",
    ".golf",
    ".goo",
    ".goodyear",
    ".goog",
    ".google",
    ".gop",
    ".got",
    ".gov",
    ".gp",
    ".gq",
    ".gr",
    ".grainger",
    ".graphics",
    ".gratis",
    ".green",
    ".gripe",
    ".grocery",
    ".group",
    ".gs",
    ".gt",
    ".gu",
    ".guardian",
    ".gucci",
    ".guge",
    ".guide",
    ".guitars",
    ".guru",
    ".gw",
    ".gy",
    ".hair",
    ".hamburg",
    ".hangout",
    ".haus",
    ".hbo",
    ".hdfc",
    ".hdfcbank",
    ".health",
    ".healthcare",
    ".help",
    ".helsinki",
    ".here",
    ".hermes",
    ".hgtv",
    ".hiphop",
    ".hisamitsu",
    ".hitachi",
    ".hiv",
    ".hk",
    ".hkt",
    ".hm",
    ".hn",
    ".hockey",
    ".holdings",
    ".holiday",
    ".homedepot",
    ".homegoods",
    ".homes",
    ".homesense",
    ".honda",
    ".horse",
    ".hospital",
    ".host",
    ".hosting",
    ".hot",
    ".hoteles",
    ".hotels",
    ".hotmail",
    ".house",
    ".how",
    ".hr",
    ".hsbc",
    ".ht",
    ".hu",
    ".hughes",
    ".hyatt",
    ".hyundai",
    ".ibm",
    ".icbc",
    ".ice",
    ".icu",
    ".id",
    ".ie",
    ".ieee",
    ".ifm",
    ".ikano",
    ".il",
    ".im",
    ".imamat",
    ".imdb",
    ".immo",
    ".immobilien",
    ".in",
    ".inc",
    ".industries",
    ".infiniti",
    ".info",
    ".ing",
    ".ink",
    ".institute",
    ".insurance",
    ".insure",
    ".int",
    ".international",
    ".intuit",
    ".investments",
    ".io",
    ".ipiranga",
    ".iq",
    ".ir",
    ".irish",
    ".is",
    ".ismaili",
    ".ist",
    ".istanbul",
    ".it",
    ".itau",
    ".itv",
    ".jaguar",
    ".java",
    ".jcb",
    ".je",
    ".jeep",
    ".jetzt",
    ".jewelry",
    ".jio",
    ".jll",
    ".jm",
    ".jmp",
    ".jnj",
    ".jo",
    ".jobs",
    ".joburg",
    ".jot",
    ".joy",
    ".jp",
    ".jpmorgan",
    ".jprs",
    ".juegos",
    ".juniper",
    ".kaufen",
    ".kddi",
    ".ke",
    ".kerryhotels",
    ".kerrylogistics",
    ".kerryproperties",
    ".kfh",
    ".kg",
    ".kh",
    ".ki",
    ".kia",
    ".kids",
    ".kim",
    ".kinder",
    ".kindle",
    ".kitchen",
    ".kiwi",
    ".km",
    ".kn",
    ".koeln",
    ".komatsu",
    ".kosher",
    ".kp",
    ".kpmg",
    ".kpn",
    ".kr",
    ".krd",
    ".kred",
    ".kuokgroup",
    ".kw",
    ".ky",
    ".kyoto",
    ".kz",
    ".la",
    ".lacaixa",
    ".lamborghini",
    ".lamer",
    ".lancaster",
    ".lancia",
    ".land",
    ".landrover",
    ".lanxess",
    ".lasalle",
    ".lat",
    ".latino",
    ".latrobe",
    ".law",
    ".lawyer",
    ".lb",
    ".lc",
    ".lds",
    ".lease",
    ".leclerc",
    ".lefrak",
    ".legal",
    ".lego",
    ".lexus",
    ".lgbt",
    ".li",
    ".lidl",
    ".life",
    ".lifeinsurance",
    ".lifestyle",
    ".lighting",
    ".like",
    ".lilly",
    ".limited",
    ".limo",
    ".lincoln",
    ".linde",
    ".link",
    ".lipsy",
    ".live",
    ".living",
    ".lk",
    ".llc",
    ".llp",
    ".loan",
    ".loans",
    ".locker",
    ".locus",
    ".lol",
    ".london",
    ".lotte",
    ".lotto",
    ".love",
    ".lpl",
    ".lplfinancial",
    ".lr",
    ".ls",
    ".lt",
    ".ltd",
    ".ltda",
    ".lu",
    ".lundbeck",
    ".luxe",
    ".luxury",
    ".lv",
    ".ly",
    ".ma",
    ".macys",
    ".madrid",
    ".maif",
    ".maison",
    ".makeup",
    ".man",
    ".management",
    ".mango",
    ".map",
    ".market",
    ".marketing",
    ".markets",
    ".marriott",
    ".marshalls",
    ".maserati",
    ".mattel",
    ".mba",
    ".mc",
    ".mckinsey",
    ".md",
    ".me",
    ".med",
    ".media",
    ".meet",
    ".melbourne",
    ".meme",
    ".memorial",
    ".men",
    ".menu",
    ".merckmsd",
    ".mg",
    ".mh",
    ".miami",
    ".microsoft",
    ".mil",
    ".mini",
    ".mint",
    ".mit",
    ".mitsubishi",
    ".mk",
    ".ml",
    ".mlb",
    ".mls",
    ".mm",
    ".mma",
    ".mn",
    ".mo",
    ".mobi",
    ".mobile",
    ".moda",
    ".moe",
    ".moi",
    ".mom",
    ".monash",
    ".money",
    ".monster",
    ".mormon",
    ".mortgage",
    ".moscow",
    ".moto",
    ".motorcycles",
    ".mov",
    ".movie",
    ".mp",
    ".mq",
    ".mr",
    ".ms",
    ".msd",
    ".mt",
    ".mtn",
    ".mtr",
    ".mu",
    ".museum",
    ".music",
    ".mutual",
    ".mv",
    ".mw",
    ".mx",
    ".my",
    ".mz",
    ".na",
    ".nab",
    ".nagoya",
    ".name",
    ".natura",
    ".navy",
    ".nba",
    ".nc",
    ".ne",
    ".nec",
    ".net",
    ".netbank",
    ".netflix",
    ".network",
    ".neustar",
    ".new",
    ".news",
    ".next",
    ".nextdirect",
    ".nexus",
    ".nf",
    ".nfl",
    ".ng",
    ".ngo",
    ".nhk",
    ".ni",
    ".nico",
    ".nike",
    ".nikon",
    ".ninja",
    ".nissan",
    ".nissay",
    ".nl",
    ".no",
    ".nokia",
    ".northwesternmutual",
    ".norton",
    ".now",
    ".nowruz",
    ".nowtv",
    ".np",
    ".nr",
    ".nra",
    ".nrw",
    ".ntt",
    ".nu",
    ".nyc",
    ".nz",
    ".obi",
    ".observer",
    ".office",
    ".okinawa",
    ".olayan",
    ".olayangroup",
    ".oldnavy",
    ".ollo",
    ".om",
    ".omega",
    ".one",
    ".ong",
    ".onl",
    ".online",
    ".ooo",
    ".open",
    ".oracle",
    ".orange",
    ".org",
    ".organic",
    ".origins",
    ".osaka",
    ".otsuka",
    ".ott",
    ".ovh",
    ".pa",
    ".page",
    ".panasonic",
    ".paris",
    ".pars",
    ".partners",
    ".parts",
    ".party",
    ".passagens",
    ".pay",
    ".pccw",
    ".pe",
    ".pet",
    ".pf",
    ".pfizer",
    ".pg",
    ".ph",
    ".pharmacy",
    ".phd",
    ".philips",
    ".phone",
    ".photo",
    ".photography",
    ".photos",
    ".physio",
    ".pics",
    ".pictet",
    ".pictures",
    ".pid",
    ".pin",
    ".ping",
    ".pink",
    ".pioneer",
    ".pizza",
    ".pk",
    ".pl",
    ".place",
    ".play",
    ".playstation",
    ".plumbing",
    ".plus",
    ".pm",
    ".pn",
    ".pnc",
    ".pohl",
    ".poker",
    ".politie",
    ".porn",
    ".post",
    ".pr",
    ".pramerica",
    ".praxi",
    ".press",
    ".prime",
    ".pro",
    ".prod",
    ".productions",
    ".prof",
    ".progressive",
    ".promo",
    ".properties",
    ".property",
    ".protection",
    ".pru",
    ".prudential",
    ".ps",
    ".pt",
    ".pub",
    ".pw",
    ".pwc",
    ".py",
    ".qa",
    ".qpon",
    ".quebec",
    ".quest",
    ".racing",
    ".radio",
    ".re",
    ".read",
    ".realestate",
    ".realtor",
    ".realty",
    ".recipes",
    ".red",
    ".redstone",
    ".redumbrella",
    ".rehab",
    ".reise",
    ".reisen",
    ".reit",
    ".reliance",
    ".ren",
    ".rent",
    ".rentals",
    ".repair",
    ".report",
    ".republican",
    ".rest",
    ".restaurant",
    ".review",
    ".reviews",
    ".rexroth",
    ".rich",
    ".richardli",
    ".ricoh",
    ".ril",
    ".rio",
    ".rip",
    ".ro",
    ".rocher",
    ".rocks",
    ".rodeo",
    ".rogers",
    ".room",
    ".rs",
    ".rsvp",
    ".ru",
    ".rugby",
    ".ruhr",
    ".run",
    ".rw",
    ".rwe",
    ".ryukyu",
    ".sa",
    ".saarland",
    ".safe",
    ".safety",
    ".sakura",
    ".sale",
    ".salon",
    ".samsclub",
    ".samsung",
    ".sandvik",
    ".sandvikcoromant",
    ".sanofi",
    ".sap",
    ".sarl",
    ".sas",
    ".save",
    ".saxo",
    ".sb",
    ".sbi",
    ".sbs",
    ".sc",
    ".sca",
    ".scb",
    ".schaeffler",
    ".schmidt",
    ".scholarships",
    ".school",
    ".schule",
    ".schwarz",
    ".science",
    ".scot",
    ".sd",
    ".se",
    ".search",
    ".seat",
    ".secure",
    ".security",
    ".seek",
    ".select",
    ".sener",
    ".services",
    ".seven",
    ".sew",
    ".sex",
    ".sexy",
    ".sfr",
    ".sg",
    ".sh",
    ".shangrila",
    ".sharp",
    ".shaw",
    ".shell",
    ".shia",
    ".shiksha",
    ".shoes",
    ".shop",
    ".shopping",
    ".shouji",
    ".show",
    ".showtime",
    ".si",
    ".silk",
    ".sina",
    ".singles",
    ".site",
    ".sj",
    ".sk",
    ".ski",
    ".skin",
    ".sky",
    ".skype",
    ".sl",
    ".sling",
    ".sm",
    ".smart",
    ".smile",
    ".sn",
    ".sncf",
    ".so",
    ".soccer",
    ".social",
    ".softbank",
    ".software",
    ".sohu",
    ".solar",
    ".solutions",
    ".song",
    ".sony",
    ".soy",
    ".spa",
    ".space",
    ".sport",
    ".spot",
    ".sr",
    ".srl",
    ".ss",
    ".st",
    ".stada",
    ".staples",
    ".star",
    ".statebank",
    ".statefarm",
    ".stc",
    ".stcgroup",
    ".stockholm",
    ".storage",
    ".store",
    ".stream",
    ".studio",
    ".study",
    ".style",
    ".su",
    ".sucks",
    ".supplies",
    ".supply",
    ".support",
    ".surf",
    ".surgery",
    ".suzuki",
    ".sv",
    ".swatch",
    ".swiss",
    ".sx",
    ".sy",
    ".sydney",
    ".systems",
    ".sz",
    ".tab",
    ".taipei",
    ".talk",
    ".taobao",
    ".target",
    ".tatamotors",
    ".tatar",
    ".tattoo",
    ".tax",
    ".taxi",
    ".tc",
    ".tci",
    ".td",
    ".tdk",
    ".team",
    ".tech",
    ".technology",
    ".tel",
    ".temasek",
    ".tennis",
    ".teva",
    ".tf",
    ".tg",
    ".th",
    ".thd",
    ".theater",
    ".theatre",
    ".tiaa",
    ".tickets",
    ".tienda",
    ".tiffany",
    ".tips",
    ".tires",
    ".tirol",
    ".tj",
    ".tjmaxx",
    ".tjx",
    ".tk",
    ".tkmaxx",
    ".tl",
    ".tm",
    ".tmall",
    ".tn",
    ".to",
    ".today",
    ".tokyo",
    ".tools",
    ".top",
    ".toray",
    ".toshiba",
    ".total",
    ".tours",
    ".town",
    ".toyota",
    ".toys",
    ".tr",
    ".trade",
    ".trading",
    ".training",
    ".travel",
    ".travelchannel",
    ".travelers",
    ".travelersinsurance",
    ".trust",
    ".trv",
    ".tt",
    ".tube",
    ".tui",
    ".tunes",
    ".tushu",
    ".tv",
    ".tvs",
    ".tw",
    ".tz",
    ".ua",
    ".ubank",
    ".ubs",
    ".ug",
    ".uk",
    ".unicom",
    ".university",
    ".uno",
    ".uol",
    ".ups",
    ".us",
    ".uy",
    ".uz",
    ".va",
    ".vacations",
    ".vana",
    ".vanguard",
    ".vc",
    ".ve",
    ".vegas",
    ".ventures",
    ".verisign",
    ".versicherung",
    ".vet",
    ".vg",
    ".vi",
    ".viajes",
    ".video",
    ".vig",
    ".viking",
    ".villas",
    ".vin",
    ".vip",
    ".virgin",
    ".visa",
    ".vision",
    ".viva",
    ".vivo",
    ".vlaanderen",
    ".vn",
    ".vodka",
    ".volkswagen",
    ".volvo",
    ".vote",
    ".voting",
    ".voto",
    ".voyage",
    ".vu",
    ".vuelos",
    ".wales",
    ".walmart",
    ".walter",
    ".wang",
    ".wanggou",
    ".watch",
    ".watches",
    ".weather",
    ".weatherchannel",
    ".webcam",
    ".weber",
    ".website",
    ".wed",
    ".wedding",
    ".weibo",
    ".weir",
    ".wf",
    ".whoswho",
    ".wien",
    ".wiki",
    ".williamhill",
    ".win",
    ".windows",
    ".wine",
    ".winners",
    ".wme",
    ".wolterskluwer",
    ".woodside",
    ".work",
    ".works",
    ".world",
    ".wow",
    ".ws",
    ".wtc",
    ".wtf",
    ".xbox",
    ".xerox",
    ".xfinity",
    ".xihuan",
    ".xin",
    ".xn--11b4c3d",
    ".xn--1ck2e1b",
    ".xn--1qqw23a",
    ".xn--2scrj9c",
    ".xn--30rr7y",
    ".xn--3bst00m",
    ".xn--3ds443g",
    ".xn--3e0b707e",
    ".xn--3hcrj9c",
    ".xn--3pxu8k",
    ".xn--42c2d9a",
    ".xn--45br5cyl",
    ".xn--45brj9c",
    ".xn--45q11c",
    ".xn--4dbrk0ce",
    ".xn--4gbrim",
    ".xn--54b7fta0cc",
    ".xn--55qw42g",
    ".xn--55qx5d",
    ".xn--5su34j936bgsg",
    ".xn--5tzm5g",
    ".xn--6frz82g",
    ".xn--6qq986b3xl",
    ".xn--80adxhks",
    ".xn--80ao21a",
    ".xn--80aqecdr1a",
    ".xn--80asehdb",
    ".xn--80aswg",
    ".xn--8y0a063a",
    ".xn--90a3ac",
    ".xn--90ae",
    ".xn--90ais",
    ".xn--9dbq2a",
    ".xn--9et52u",
    ".xn--9krt00a",
    ".xn--b4w605ferd",
    ".xn--bck1b9a5dre4c",
    ".xn--c1avg",
    ".xn--c2br7g",
    ".xn--cck2b3b",
    ".xn--cckwcxetd",
    ".xn--cg4bki",
    ".xn--clchc0ea0b2g2a9gcd",
    ".xn--czr694b",
    ".xn--czrs0t",
    ".xn--czru2d",
    ".xn--d1acj3b",
    ".xn--d1alf",
    ".xn--e1a4c",
    ".xn--eckvdtc9d",
    ".xn--efvy88h",
    ".xn--fct429k",
    ".xn--fhbei",
    ".xn--fiq228c5hs",
    ".xn--fiq64b",
    ".xn--fiqs8s",
    ".xn--fiqz9s",
    ".xn--fjq720a",
    ".xn--flw351e",
    ".xn--fpcrj9c3d",
    ".xn--fzc2c9e2c",
    ".xn--fzys8d69uvgm",
    ".xn--g2xx48c",
    ".xn--gckr3f0f",
    ".xn--gecrj9c",
    ".xn--gk3at1e",
    ".xn--h2breg3eve",
    ".xn--h2brj9c",
    ".xn--h2brj9c8c",
    ".xn--hxt814e",
    ".xn--i1b6b1a6a2e",
    ".xn--imr513n",
    ".xn--io0a7i",
    ".xn--j1aef",
    ".xn--j1amh",
    ".xn--j6w193g",
    ".xn--jlq480n2rg",
    ".xn--jvr189m",
    ".xn--kcrx77d1x4a",
    ".xn--kprw13d",
    ".xn--kpry57d",
    ".xn--kput3i",
    ".xn--l1acc",
    ".xn--lgbbat1ad8j",
    ".xn--mgb9awbf",
    ".xn--mgba3a3ejt",
    ".xn--mgba3a4f16a",
    ".xn--mgba7c0bbn0a",
    ".xn--mgbaakc7dvf",
    ".xn--mgbaam7a8h",
    ".xn--mgbab2bd",
    ".xn--mgbah1a3hjkrd",
    ".xn--mgbai9azgqp6j",
    ".xn--mgbayh7gpa",
    ".xn--mgbbh1a",
    ".xn--mgbbh1a71e",
    ".xn--mgbc0a9azcg",
    ".xn--mgbca7dzdo",
    ".xn--mgbcpq6gpa1a",
    ".xn--mgberp4a5d4ar",
    ".xn--mgbgu82a",
    ".xn--mgbi4ecexp",
    ".xn--mgbpl2fh",
    ".xn--mgbt3dhd",
    ".xn--mgbtx2b",
    ".xn--mgbx4cd0ab",
    ".xn--mix891f",
    ".xn--mk1bu44c",
    ".xn--mxtq1m",
    ".xn--ngbc5azd",
    ".xn--ngbe9e0a",
    ".xn--ngbrx",
    ".xn--node",
    ".xn--nqv7f",
    ".xn--nqv7fs00ema",
    ".xn--nyqy26a",
    ".xn--o3cw4h",
    ".xn--ogbpf8fl",
    ".xn--otu796d",
    ".xn--p1acf",
    ".xn--p1ai",
    ".xn--pgbs0dh",
    ".xn--pssy2u",
    ".xn--q7ce6a",
    ".xn--q9jyb4c",
    ".xn--qcka1pmc",
    ".xn--qxa6a",
    ".xn--qxam",
    ".xn--rhqv96g",
    ".xn--rovu88b",
    ".xn--rvc1e0am3e",
    ".xn--s9brj9c",
    ".xn--ses554g",
    ".xn--t60b56a",
    ".xn--tckwe",
    ".xn--tiq49xqyj",
    ".xn--unup4y",
    ".xn--vermgensberater-ctb",
    ".xn--vermgensberatung-pwb",
    ".xn--vhquv",
    ".xn--vuq861b",
    ".xn--w4r85el8fhu5dnra",
    ".xn--w4rs40l",
    ".xn--wgbh1c",
    ".xn--wgbl6a",
    ".xn--xhq521b",
    ".xn--xkc2al3hye2a",
    ".xn--xkc2dl3a5ee0h",
    ".xn--y9a3aq",
    ".xn--yfro4i67o",
    ".xn--ygbi2ammx",
    ".xn--zfr164b",
    ".xxx",
    ".xyz",
    ".yachts",
    ".yahoo",
    ".yamaxun",
    ".yandex",
    ".ye",
    ".yodobashi",
    ".yoga",
    ".yokohama",
    ".you",
    ".youtube",
    ".yt",
    ".yun",
    ".za",
    ".zappos",
    ".zara",
    ".zero",
    ".zip",
    ".zm",
    ".zone",
    ".zuerich",
    ".zw",
]
CHARS = [".", " ", "<", ">", "+", "*", ";", ":", '"', "{", "}", "|", "^", "`", "#"]

# regex_str = r"""
#   \b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b
# """

FIND_URLS = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s"()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
URLS = re.compile(FIND_URLS, re.VERBOSE)

# JSON = r"JSON\.parse(\(\"{.*?}\"\))|JSON.parse(\(\".*?\"\))"
MATCH_JSON_PARSE = r"JSON\.parse(\(\".+\"\);)"
JSON_PARSE = re.compile(MATCH_JSON_PARSE)

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def print_result(wordlist):
    # print(wordlist)
    for k, v in wordlist.items():
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
    json_obj_list = []
    not_real_urls = []
    js_files = []
    directories_list = []
    url_n = 0
    js_n = 0
    urls_found = dict()

    html = False
    n = 0
    try:
        for event, elem in ET.iterparse(burpfile):
            if elem.tag == "url" and elem.text not in url_list:
                url_list.append(elem.text)
            if elem.tag == "method" and elem.text == "GET":
                continue
            if elem.tag == "mimetype" and elem.text == "HTML":
                html = True
            if elem.tag == "response" and elem.attrib["base64"] == "true":
                elem.text = str(base64.b64decode(elem.text))
                # print(elem.text)
                if html:
                    urls = URLS.findall(elem.text)
                    # for group in urls:
                    #     for url in group:
                    #         if url not in url_list and url != '':
                    #             url_list.append(url)
                    for url in urls:
                        # print(Path(urlparse(url).path).suffix)
                        if (
                            Path(urlparse(url).path).suffix in TLD
                            or Path(urlparse(url).netloc).suffix in TLD
                        ):
                            if urlparse(url).scheme == "" and not urlparse(
                                url
                            ).path.startswith("."):
                                url = "https://" + url
                            elif urlparse(url).scheme == "" and urlparse(
                                url
                            ).path.startswith("."):
                                url = "https://www" + url
                            if (
                                Path(urlparse(url).path).suffix != ".js"
                                and url not in url_list
                            ):
                                url_list.append(url)
                            elif (
                                Path(urlparse(url).path).suffix == ".js"
                                and url not in js_files
                            ):
                                js_files.append(url)

                    json_parse_data = JSON_PARSE.findall(elem.text)
                    print(json_parse_data)
                    # print(json_obj)
                    # inner_data = [d.encode().decode("unicode-escape") for d in json_parse_data]
                    # inner_data = [d.encode().decode("unicode-escape") for d in json_parse_data]
                    
                    #print(inner_data)
                    # json_parse_data = [inner_data.encode().decode("unicode-escape") for inner_data in json_parse_data]
                    # print(json_parse_data)
                    # json_obj = [e.encode().decode("unicode-escape") for e in json_obj]
                    # print(json_obj)

                    # urls_in_jsonparse = []

                    # for t in json_obj:
                    #     urls_in_jsonparse = URLS.findall(t)

                    # for url in urls_in_jsonparse:
                    #     if url not in url_list:
                    #         url_list.append(url)
            elif elem.tag == "response" and elem.attrib["base64"] == "false":
                if html:
                    urls = URLS.findall(elem.text)
                    # for group in urls:
                    #     for url in group:
                    #         if url not in url_list and url != '':
                    #             url_list.append(url)
                    for url in urls:
                        # print(Path(urlparse(url).path).suffix)
                        if (
                            Path(urlparse(url).path).suffix in TLD
                            or Path(urlparse(url).netloc).suffix in TLD
                        ):
                            if urlparse(url).scheme == "" and not urlparse(
                                url
                            ).path.startswith("."):
                                url = "https://" + url
                            elif urlparse(url).scheme == "" and urlparse(
                                url
                            ).path.startswith("."):
                                url = "https://www" + url
                            if (
                                Path(urlparse(url).path).suffix != ".js"
                                and url not in url_list
                            ):
                                url_list.append(url)
                            elif (
                                Path(urlparse(url).path).suffix == ".js"
                                and url not in js_files
                            ):
                                js_files.append(url)

                    json_obj = JSON_PARSE.findall(elem.text)
                    # print(json_obj)
                    json_obj = [e.encode().decode("unicode-escape") for e in json_obj]
                    # print(json_obj)
                    json_obj = [e.encode().decode("unicode-escape") for e in json_obj]
                    # print(json_obj)
                    urls_in_jsonparse = []

                    for t in json_obj:
                        urls_in_jsonparse = URLS.findall(t)

                    for url in urls_in_jsonparse:
                        if url not in url_list:
                            url_list.append(url)

                    #     o = o.encode('utf-8')
                    # print(json_obj)
                    # json_obj = ' '.join([str(elem) for elem in json_obj])

                    # print(json.loads(json_obj))
                    # print(json_obj)
                    # elif Path(urlparse(url).path).suffix not in TLD or Path(urlparse(url).netloc).suffix not in TLD:
                    #     if Path(urlparse(url).path).suffix != '' and url not in not_real_urls:
                    #         not_real_urls.append(url)

            if elem.tag == "item":
                n += 1
            elem.clear()
        print("Reached the end", n, "times.")

        # print("Real URLs:", len(url_list))
        # for url in url_list:
        # urls_found = check_url(url_list)

        # for status, url_list in urls_found.items():
        #     print(status)
        #     for url in url_list:
        #         print(url)
        # for char in url:
        #     if char in CHARS:
        #         char = quote(char)
        #     print(url)
        # print()
        # print("------------------------")
        # print("JS files:", len(js_files))
        # print("------------------------")
        # for js in js_files:
        #     print(js)
        # print()
        # print("------------------------")
        # print("Not real URLs")
        # print("------------------------")
        # for url in not_real_urls:
        #     print(url)
        # directories_list = get_directories(url_list)

    except ET.ParseError as err:
        print(err)
    # urls_found["urls"] = url_list
    # urls_found["javascript files"] = js_files
    # return urls_found


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