import argparse
import html
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
    ".bak",
    ".bat",
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

FIND_URLS = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:aaa|aarp|abarth|abb|abbott|abbvie|abc|able|abogado|abudhabi|ac|academy|accenture|accountant|accountants|aco|actor|ad|ads|adult|ae|aeg|aero|aetna|af|afl|africa|ag|agakhan|agency|ai|aig|airbus|airforce|airtel|akdn|al|alfaromeo|alibaba|alipay|allfinanz|allstate|ally|alsace|alstom|am|amazon|americanexpress|americanfamily|amex|amfam|amica|amsterdam|analytics|android|anquan|anz|ao|aol|apartments|app|apple|aq|aquarelle|ar|arab|aramco|archi|army|arpa|art|arte|as|asda|asia|associates|at|athleta|attorney|au|auction|audi|audible|audio|auspost|author|auto|autos|avianca|aw|aws|ax|axa|az|azure|ba|baby|baidu|banamex|bananarepublic|band|bank|bar|barcelona|barclaycard|barclays|barefoot|bargains|baseball|basketball|bauhaus|bayern|bb|bbc|bbt|bbva|bcg|bcn|bd|be|beats|beauty|beer|bentley|berlin|best|bestbuy|bet|bf|bg|bh|bharti|bi|bible|bid|bike|bing|bingo|bio|biz|bj|black|blackfriday|blockbuster|blog|bloomberg|blue|bm|bms|bmw|bn|bnpparibas|bo|boats|boehringer|bofa|bom|bond|boo|book|booking|bosch|bostik|boston|bot|boutique|box|br|bradesco|bridgestone|broadway|broker|brother|brussels|bs|bt|build|builders|business|buy|buzz|bv|bw|by|bz|bzh|ca|cab|cafe|cal|call|calvinklein|cam|camera|camp|canon|capetown|capital|capitalone|car|caravan|cards|care|career|careers|cars|casa|case|cash|casino|cat|catering|catholic|cba|cbn|cbre|cbs|cc|cd|center|ceo|cern|cf|cfa|cfd|cg|ch|chanel|channel|charity|chase|chat|cheap|chintai|christmas|chrome|church|ci|cipriani|circle|cisco|citadel|citi|citic|city|cityeats|ck|cl|claims|cleaning|click|clinic|clinique|clothing|cloud|club|clubmed|cm|cn|co|coach|codes|coffee|college|cologne|com|comcast|commbank|community|company|compare|computer|comsec|condos|construction|consulting|contact|contractors|cooking|cookingchannel|cool|coop|corsica|country|coupon|coupons|courses|cpa|cr|credit|creditcard|creditunion|cricket|crown|crs|cruise|cruises|cu|cuisinella|cv|cw|cx|cy|cymru|cyou|cz|dabur|dad|dance|data|date|dating|datsun|day|dclk|dds|de|deal|dealer|deals|degree|delivery|dell|deloitte|delta|democrat|dental|dentist|desi|design|dev|dhl|diamonds|diet|digital|direct|directory|discount|discover|dish|diy|dj|dk|dm|dnp|do|docs|doctor|dog|domains|dot|download|drive|dtv|dubai|dunlop|dupont|durban|dvag|dvr|dz|earth|eat|ec|eco|edeka|edu|education|ee|eg|email|emerck|energy|engineer|engineering|enterprises|epson|equipment|er|ericsson|erni|es|esq|estate|et|etisalat|eu|eurovision|eus|events|exchange|expert|exposed|express|extraspace|fage|fail|fairwinds|faith|family|fan|fans|farm|farmers|fashion|fast|fedex|feedback|ferrari|ferrero|fi|fiat|fidelity|fido|film|final|finance|financial|fire|firestone|firmdale|fish|fishing|fit|fitness|fj|fk|flickr|flights|flir|florist|flowers|fly|fm|fo|foo|food|foodnetwork|football|ford|forex|forsale|forum|foundation|fox|fr|free|fresenius|frl|frogans|frontdoor|frontier|ftr|fujitsu|fun|fund|furniture|futbol|fyi|ga|gal|gallery|gallo|gallup|game|games|gap|garden|gay|gb|gbiz|gd|gdn|ge|gea|gent|genting|george|gf|gg|ggee|gh|gi|gift|gifts|gives|giving|gl|glass|gle|global|globo|gm|gmail|gmbh|gmo|gmx|gn|godaddy|gold|goldpoint|golf|goo|goodyear|goog|google|gop|got|gov|gp|gq|gr|grainger|graphics|gratis|green|gripe|grocery|group|gs|gt|gu|guardian|gucci|guge|guide|guitars|guru|gw|gy|hair|hamburg|hangout|haus|hbo|hdfc|hdfcbank|health|healthcare|help|helsinki|here|hermes|hgtv|hiphop|hisamitsu|hitachi|hiv|hk|hkt|hm|hn|hockey|holdings|holiday|homedepot|homegoods|homes|homesense|honda|horse|hospital|host|hosting|hot|hoteles|hotels|hotmail|house|how|hr|hsbc|ht|hu|hughes|hyatt|hyundai|ibm|icbc|ice|icu|id|ie|ieee|ifm|ikano|il|im|imamat|imdb|immo|immobilien|in|inc|industries|infiniti|info|ing|ink|institute|insurance|insure|int|international|intuit|investments|io|ipiranga|iq|ir|irish|is|ismaili|ist|istanbul|it|itau|itv|jaguar|java|jcb|je|jeep|jetzt|jewelry|jio|jll|jm|jmp|jnj|jo|jobs|joburg|jot|joy|jp|jpmorgan|jprs|juegos|juniper|kaufen|kddi|ke|kerryhotels|kerrylogistics|kerryproperties|kfh|kg|kh|ki|kia|kids|kim|kinder|kindle|kitchen|kiwi|km|kn|koeln|komatsu|kosher|kp|kpmg|kpn|kr|krd|kred|kuokgroup|kw|ky|kyoto|kz|la|lacaixa|lamborghini|lamer|lancaster|lancia|land|landrover|lanxess|lasalle|lat|latino|latrobe|law|lawyer|lb|lc|lds|lease|leclerc|lefrak|legal|lego|lexus|lgbt|li|lidl|life|lifeinsurance|lifestyle|lighting|like|lilly|limited|limo|lincoln|linde|link|lipsy|live|living|lk|llc|llp|loan|loans|locker|locus|lol|london|lotte|lotto|love|lpl|lplfinancial|lr|ls|lt|ltd|ltda|lu|lundbeck|luxe|luxury|lv|ly|ma|madrid|maif|maison|makeup|man|management|mango|map|market|marketing|markets|marriott|marshalls|maserati|mattel|mba|mc|mckinsey|md|me|med|media|meet|melbourne|meme|memorial|men|menu|merckmsd|mg|mh|miami|microsoft|mil|mini|mint|mit|mitsubishi|mk|ml|mlb|mls|mm|mma|mn|mo|mobi|mobile|moda|moe|moi|mom|monash|money|monster|mormon|mortgage|moscow|moto|motorcycles|mov|movie|mp|mq|mr|ms|msd|mt|mtn|mtr|mu|museum|music|mutual|mv|mw|mx|my|mz|na|nab|nagoya|name|natura|navy|nba|nc|ne|nec|net|netbank|netflix|network|neustar|new|news|next|nextdirect|nexus|nf|nfl|ng|ngo|nhk|ni|nico|nike|nikon|ninja|nissan|nissay|nl|no|nokia|northwesternmutual|norton|now|nowruz|nowtv|np|nr|nra|nrw|ntt|nu|nyc|nz|obi|observer|office|okinawa|olayan|olayangroup|oldnavy|ollo|om|omega|one|ong|onl|online|ooo|open|oracle|orange|org|organic|origins|osaka|otsuka|ott|ovh|pa|page|panasonic|paris|pars|partners|parts|party|passagens|pay|pccw|pe|pet|pf|pfizer|pg|ph|pharmacy|phd|philips|phone|photo|photography|photos|physio|pics|pictet|pictures|pid|pin|ping|pink|pioneer|pizza|pk|pl|place|play|playstation|plumbing|plus|pm|pn|pnc|pohl|poker|politie|porn|post|pr|pramerica|praxi|press|prime|pro|prod|productions|prof|progressive|promo|properties|property|protection|pru|prudential|ps|pt|pub|pw|pwc|py|qa|qpon|quebec|quest|racing|radio|re|read|realestate|realtor|realty|recipes|red|redstone|redumbrella|rehab|reise|reisen|reit|reliance|ren|rent|rentals|repair|report|republican|rest|restaurant|review|reviews|rexroth|rich|richardli|ricoh|ril|rio|rip|ro|rocher|rocks|rodeo|rogers|room|rs|rsvp|ru|rugby|ruhr|run|rw|rwe|ryukyu|sa|saarland|safe|safety|sakura|sale|salon|samsclub|samsung|sandvik|sandvikcoromant|sanofi|sap|sarl|sas|save|saxo|sb|sbi|sbs|sc|sca|scb|schaeffler|schmidt|scholarships|school|schule|schwarz|science|scot|sd|se|search|seat|secure|security|seek|select|sener|services|seven|sew|sex|sexy|sfr|sg|sh|shangrila|sharp|shaw|shell|shia|shiksha|shoes|shop|shopping|shouji|show|showtime|si|silk|sina|singles|site|sj|sk|ski|skin|sky|skype|sl|sling|sm|smart|smile|sn|sncf|so|soccer|social|softbank|software|sohu|solar|solutions|song|sony|soy|spa|space|sport|spot|sr|srl|ss|st|stada|staples|star|statebank|statefarm|stc|stcgroup|stockholm|storage|store|stream|studio|study|style|su|sucks|supplies|supply|support|surf|surgery|suzuki|sv|swatch|swiss|sx|sy|sydney|systems|sz|tab|taipei|talk|taobao|target|tatamotors|tatar|tattoo|tax|taxi|tc|tci|td|tdk|team|tech|technology|tel|temasek|tennis|teva|tf|tg|th|thd|theater|theatre|tiaa|tickets|tienda|tiffany|tips|tires|tirol|tj|tjmaxx|tjx|tk|tkmaxx|tl|tm|tmall|tn|to|today|tokyo|tools|top|toray|toshiba|total|tours|town|toyota|toys|tr|trade|trading|training|travel|travelchannel|travelers|travelersinsurance|trust|trv|tt|tube|tui|tunes|tushu|tv|tvs|tw|tz|ua|ubank|ubs|ug|uk|unicom|university|uno|uol|ups|us|uy|uz|va|vacations|vana|vanguard|vc|ve|vegas|ventures|verisign|versicherung|vet|vg|vi|viajes|video|vig|viking|villas|vin|vip|virgin|visa|vision|viva|vivo|vlaanderen|vn|vodka|volkswagen|volvo|vote|voting|voto|voyage|vu|vuelos|wales|walmart|walter|wang|wanggou|watch|watches|weather|weatherchannel|webcam|weber|website|wed|wedding|weibo|weir|wf|whoswho|wien|wiki|williamhill|win|windows|wine|winners|wme|wolterskluwer|woodside|work|works|world|wow|ws|wtc|wtf|xbox|xerox|xfinity|xihuan|xin|xn--11b4c3d|xn--1ck2e1b|xn--1qqw23a|xn--2scrj9c|xn--30rr7y|xn--3bst00m|xn--3ds443g|xn--3e0b707e|xn--3hcrj9c|xn--3pxu8k|xn--42c2d9a|xn--45br5cyl|xn--45brj9c|xn--45q11c|xn--4dbrk0ce|xn--4gbrim|xn--54b7fta0cc|xn--55qw42g|xn--55qx5d|xn--5su34j936bgsg|xn--5tzm5g|xn--6frz82g|xn--6qq986b3xl|xn--80adxhks|xn--80ao21a|xn--80aqecdr1a|xn--80asehdb|xn--80aswg|xn--8y0a063a|xn--90a3ac|xn--90ae|xn--90ais|xn--9dbq2a|xn--9et52u|xn--9krt00a|xn--b4w605ferd|xn--bck1b9a5dre4c|xn--c1avg|xn--c2br7g|xn--cck2b3b|xn--cckwcxetd|xn--cg4bki|xn--clchc0ea0b2g2a9gcd|xn--czr694b|xn--czrs0t|xn--czru2d|xn--d1acj3b|xn--d1alf|xn--e1a4c|xn--eckvdtc9d|xn--efvy88h|xn--fct429k|xn--fhbei|xn--fiq228c5hs|xn--fiq64b|xn--fiqs8s|xn--fiqz9s|xn--fjq720a|xn--flw351e|xn--fpcrj9c3d|xn--fzc2c9e2c|xn--fzys8d69uvgm|xn--g2xx48c|xn--gckr3f0f|xn--gecrj9c|xn--gk3at1e|xn--h2breg3eve|xn--h2brj9c|xn--h2brj9c8c|xn--hxt814e|xn--i1b6b1a6a2e|xn--imr513n|xn--io0a7i|xn--j1aef|xn--j1amh|xn--j6w193g|xn--jlq480n2rg|xn--jvr189m|xn--kcrx77d1x4a|xn--kprw13d|xn--kpry57d|xn--kput3i|xn--l1acc|xn--lgbbat1ad8j|xn--mgb9awbf|xn--mgba3a3ejt|xn--mgba3a4f16a|xn--mgba7c0bbn0a|xn--mgbaakc7dvf|xn--mgbaam7a8h|xn--mgbab2bd|xn--mgbah1a3hjkrd|xn--mgbai9azgqp6j|xn--mgbayh7gpa|xn--mgbbh1a|xn--mgbbh1a71e|xn--mgbc0a9azcg|xn--mgbca7dzdo|xn--mgbcpq6gpa1a|xn--mgberp4a5d4ar|xn--mgbgu82a|xn--mgbi4ecexp|xn--mgbpl2fh|xn--mgbt3dhd|xn--mgbtx2b|xn--mgbx4cd0ab|xn--mix891f|xn--mk1bu44c|xn--mxtq1m|xn--ngbc5azd|xn--ngbe9e0a|xn--ngbrx|xn--node|xn--nqv7f|xn--nqv7fs00ema|xn--nyqy26a|xn--o3cw4h|xn--ogbpf8fl|xn--otu796d|xn--p1acf|xn--p1ai|xn--pgbs0dh|xn--pssy2u|xn--q7ce6a|xn--q9jyb4c|xn--qcka1pmc|xn--qxa6a|xn--qxam|xn--rhqv96g|xn--rovu88b|xn--rvc1e0am3e|xn--s9brj9c|xn--ses554g|xn--t60b56a|xn--tckwe|xn--tiq49xqyj|xn--unup4y|xn--vermgensberater-ctb|xn--vermgensberatung-pwb|xn--vhquv|xn--vuq861b|xn--w4r85el8fhu5dnra|xn--w4rs40l|xn--wgbh1c|xn--wgbl6a|xn--xhq521b|xn--xkc2al3hye2a|xn--xkc2dl3a5ee0h|xn--y9a3aq|xn--yfro4i67o|xn--ygbi2ammx|xn--zfr164b|xxx|xyz|yachts|yahoo|yamaxun|yandex|ye|yodobashi|yoga|yokohama|you|youtube|yt|yun|za|zappos|zara|zero|zip|zm|zone|zuerich|zw)/)(?:[^\s"()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[\\]?[.](?:aaa|aarp|abarth|abb|abbott|abbvie|abc|able|abogado|abudhabi|ac|academy|accenture|accountant|accountants|aco|actor|ad|ads|adult|ae|aeg|aero|aetna|af|afl|africa|ag|agakhan|agency|ai|aig|airbus|airforce|airtel|akdn|al|alfaromeo|alibaba|alipay|allfinanz|allstate|ally|alsace|alstom|am|amazon|americanexpress|americanfamily|amex|amfam|amica|amsterdam|analytics|android|anquan|anz|ao|aol|apartments|app|apple|aq|aquarelle|ar|arab|aramco|archi|army|arpa|art|arte|as|asda|asia|associates|at|athleta|attorney|au|auction|audi|audible|audio|auspost|author|auto|autos|avianca|aw|aws|ax|axa|az|azure|ba|baby|baidu|banamex|bananarepublic|band|bank|bar|barcelona|barclaycard|barclays|barefoot|bargains|baseball|basketball|bauhaus|bayern|bb|bbc|bbt|bbva|bcg|bcn|bd|be|beats|beauty|beer|bentley|berlin|best|bestbuy|bet|bf|bg|bh|bharti|bi|bible|bid|bike|bing|bingo|bio|biz|bj|black|blackfriday|blockbuster|blog|bloomberg|blue|bm|bms|bmw|bn|bnpparibas|bo|boats|boehringer|bofa|bom|bond|boo|book|booking|bosch|bostik|boston|bot|boutique|box|br|bradesco|bridgestone|broadway|broker|brother|brussels|bs|bt|build|builders|business|buy|buzz|bv|bw|by|bz|bzh|ca|cab|cafe|cal|call|calvinklein|cam|camera|camp|canon|capetown|capital|capitalone|car|caravan|cards|care|career|careers|cars|casa|case|cash|casino|cat|catering|catholic|cba|cbn|cbre|cbs|cc|cd|center|ceo|cern|cf|cfa|cfd|cg|ch|chanel|channel|charity|chase|chat|cheap|chintai|christmas|chrome|church|ci|cipriani|circle|cisco|citadel|citi|citic|city|cityeats|ck|cl|claims|cleaning|click|clinic|clinique|clothing|cloud|club|clubmed|cm|cn|co|coach|codes|coffee|college|cologne|com|comcast|commbank|community|company|compare|computer|comsec|condos|construction|consulting|contact|contractors|cooking|cookingchannel|cool|coop|corsica|country|coupon|coupons|courses|cpa|cr|credit|creditcard|creditunion|cricket|crown|crs|cruise|cruises|cu|cuisinella|cv|cw|cx|cy|cymru|cyou|cz|dabur|dad|dance|data|date|dating|datsun|day|dclk|dds|de|deal|dealer|deals|degree|delivery|dell|deloitte|delta|democrat|dental|dentist|desi|design|dev|dhl|diamonds|diet|digital|direct|directory|discount|discover|dish|diy|dj|dk|dm|dnp|do|docs|doctor|dog|domains|dot|download|drive|dtv|dubai|dunlop|dupont|durban|dvag|dvr|dz|earth|eat|ec|eco|edeka|edu|education|ee|eg|email|emerck|energy|engineer|engineering|enterprises|epson|equipment|er|ericsson|erni|es|esq|estate|et|etisalat|eu|eurovision|eus|events|exchange|expert|exposed|express|extraspace|fage|fail|fairwinds|faith|family|fan|fans|farm|farmers|fashion|fast|fedex|feedback|ferrari|ferrero|fi|fiat|fidelity|fido|film|final|finance|financial|fire|firestone|firmdale|fish|fishing|fit|fitness|fj|fk|flickr|flights|flir|florist|flowers|fly|fm|fo|foo|food|foodnetwork|football|ford|forex|forsale|forum|foundation|fox|fr|free|fresenius|frl|frogans|frontdoor|frontier|ftr|fujitsu|fun|fund|furniture|futbol|fyi|ga|gal|gallery|gallo|gallup|game|games|gap|garden|gay|gb|gbiz|gd|gdn|ge|gea|gent|genting|george|gf|gg|ggee|gh|gi|gift|gifts|gives|giving|gl|glass|gle|global|globo|gm|gmail|gmbh|gmo|gmx|gn|godaddy|gold|goldpoint|golf|goo|goodyear|goog|google|gop|got|gov|gp|gq|gr|grainger|graphics|gratis|green|gripe|grocery|group|gs|gt|gu|guardian|gucci|guge|guide|guitars|guru|gw|gy|hair|hamburg|hangout|haus|hbo|hdfc|hdfcbank|health|healthcare|help|helsinki|here|hermes|hgtv|hiphop|hisamitsu|hitachi|hiv|hk|hkt|hm|hn|hockey|holdings|holiday|homedepot|homegoods|homes|homesense|honda|horse|hospital|host|hosting|hot|hoteles|hotels|hotmail|house|how|hr|hsbc|ht|hu|hughes|hyatt|hyundai|ibm|icbc|ice|icu|id|ie|ieee|ifm|ikano|il|im|imamat|imdb|immo|immobilien|in|inc|industries|infiniti|info|ing|ink|institute|insurance|insure|int|international|intuit|investments|io|ipiranga|iq|ir|irish|is|ismaili|ist|istanbul|it|itau|itv|jaguar|java|jcb|je|jeep|jetzt|jewelry|jio|jll|jm|jmp|jnj|jo|jobs|joburg|jot|joy|jp|jpmorgan|jprs|juegos|juniper|kaufen|kddi|ke|kerryhotels|kerrylogistics|kerryproperties|kfh|kg|kh|ki|kia|kids|kim|kinder|kindle|kitchen|kiwi|km|kn|koeln|komatsu|kosher|kp|kpmg|kpn|kr|krd|kred|kuokgroup|kw|ky|kyoto|kz|la|lacaixa|lamborghini|lamer|lancaster|lancia|land|landrover|lanxess|lasalle|lat|latino|latrobe|law|lawyer|lb|lc|lds|lease|leclerc|lefrak|legal|lego|lexus|lgbt|li|lidl|life|lifeinsurance|lifestyle|lighting|like|lilly|limited|limo|lincoln|linde|link|lipsy|live|living|lk|llc|llp|loan|loans|locker|locus|lol|london|lotte|lotto|love|lpl|lplfinancial|lr|ls|lt|ltd|ltda|lu|lundbeck|luxe|luxury|lv|ly|ma|madrid|maif|maison|makeup|man|management|mango|map|market|marketing|markets|marriott|marshalls|maserati|mattel|mba|mc|mckinsey|md|me|med|media|meet|melbourne|meme|memorial|men|menu|merckmsd|mg|mh|miami|microsoft|mil|mini|mint|mit|mitsubishi|mk|ml|mlb|mls|mm|mma|mn|mo|mobi|mobile|moda|moe|moi|mom|monash|money|monster|mormon|mortgage|moscow|moto|motorcycles|mov|movie|mp|mq|mr|ms|msd|mt|mtn|mtr|mu|museum|music|mutual|mv|mw|mx|my|mz|na|nab|nagoya|name|natura|navy|nba|nc|ne|nec|net|netbank|netflix|network|neustar|new|news|next|nextdirect|nexus|nf|nfl|ng|ngo|nhk|ni|nico|nike|nikon|ninja|nissan|nissay|nl|no|nokia|northwesternmutual|norton|now|nowruz|nowtv|np|nr|nra|nrw|ntt|nu|nyc|nz|obi|observer|office|okinawa|olayan|olayangroup|oldnavy|ollo|om|omega|one|ong|onl|online|ooo|open|oracle|orange|org|organic|origins|osaka|otsuka|ott|ovh|pa|page|panasonic|paris|pars|partners|parts|party|passagens|pay|pccw|pe|pet|pf|pfizer|pg|ph|pharmacy|phd|philips|phone|photo|photography|photos|physio|pics|pictet|pictures|pid|pin|ping|pink|pioneer|pizza|pk|pl|place|play|playstation|plumbing|plus|pm|pn|pnc|pohl|poker|politie|porn|post|pr|pramerica|praxi|press|prime|pro|prod|productions|prof|progressive|promo|properties|property|protection|pru|prudential|ps|pt|pub|pw|pwc|py|qa|qpon|quebec|quest|racing|radio|re|read|realestate|realtor|realty|recipes|red|redstone|redumbrella|rehab|reise|reisen|reit|reliance|ren|rent|rentals|repair|report|republican|rest|restaurant|review|reviews|rexroth|rich|richardli|ricoh|ril|rio|rip|ro|rocher|rocks|rodeo|rogers|room|rs|rsvp|ru|rugby|ruhr|run|rw|rwe|ryukyu|sa|saarland|safe|safety|sakura|sale|salon|samsclub|samsung|sandvik|sandvikcoromant|sanofi|sap|sarl|sas|save|saxo|sb|sbi|sbs|sc|sca|scb|schaeffler|schmidt|scholarships|school|schule|schwarz|science|scot|sd|se|search|seat|secure|security|seek|select|sener|services|seven|sew|sex|sexy|sfr|sg|sh|shangrila|sharp|shaw|shell|shia|shiksha|shoes|shop|shopping|shouji|show|showtime|si|silk|sina|singles|site|sj|sk|ski|skin|sky|skype|sl|sling|sm|smart|smile|sn|sncf|so|soccer|social|softbank|software|sohu|solar|solutions|song|sony|soy|spa|space|sport|spot|sr|srl|ss|st|stada|staples|star|statebank|statefarm|stc|stcgroup|stockholm|storage|store|stream|studio|study|style|su|sucks|supplies|supply|support|surf|surgery|suzuki|sv|swatch|swiss|sx|sy|sydney|systems|sz|tab|taipei|talk|taobao|target|tatamotors|tatar|tattoo|tax|taxi|tc|tci|td|tdk|team|tech|technology|tel|temasek|tennis|teva|tf|tg|th|thd|theater|theatre|tiaa|tickets|tienda|tiffany|tips|tires|tirol|tj|tjmaxx|tjx|tk|tkmaxx|tl|tm|tmall|tn|to|today|tokyo|tools|top|toray|toshiba|total|tours|town|toyota|toys|tr|trade|trading|training|travel|travelchannel|travelers|travelersinsurance|trust|trv|tt|tube|tui|tunes|tushu|tv|tvs|tw|tz|ua|ubank|ubs|ug|uk|unicom|university|uno|uol|ups|us|uy|uz|va|vacations|vana|vanguard|vc|ve|vegas|ventures|verisign|versicherung|vet|vg|vi|viajes|video|vig|viking|villas|vin|vip|virgin|visa|vision|viva|vivo|vlaanderen|vn|vodka|volkswagen|volvo|vote|voting|voto|voyage|vu|vuelos|wales|walmart|walter|wang|wanggou|watch|watches|weather|weatherchannel|webcam|weber|website|wed|wedding|weibo|weir|wf|whoswho|wien|wiki|williamhill|win|windows|wine|winners|wme|wolterskluwer|woodside|work|works|world|wow|ws|wtc|wtf|xbox|xerox|xfinity|xihuan|xin|xn--11b4c3d|xn--1ck2e1b|xn--1qqw23a|xn--2scrj9c|xn--30rr7y|xn--3bst00m|xn--3ds443g|xn--3e0b707e|xn--3hcrj9c|xn--3pxu8k|xn--42c2d9a|xn--45br5cyl|xn--45brj9c|xn--45q11c|xn--4dbrk0ce|xn--4gbrim|xn--54b7fta0cc|xn--55qw42g|xn--55qx5d|xn--5su34j936bgsg|xn--5tzm5g|xn--6frz82g|xn--6qq986b3xl|xn--80adxhks|xn--80ao21a|xn--80aqecdr1a|xn--80asehdb|xn--80aswg|xn--8y0a063a|xn--90a3ac|xn--90ae|xn--90ais|xn--9dbq2a|xn--9et52u|xn--9krt00a|xn--b4w605ferd|xn--bck1b9a5dre4c|xn--c1avg|xn--c2br7g|xn--cck2b3b|xn--cckwcxetd|xn--cg4bki|xn--clchc0ea0b2g2a9gcd|xn--czr694b|xn--czrs0t|xn--czru2d|xn--d1acj3b|xn--d1alf|xn--e1a4c|xn--eckvdtc9d|xn--efvy88h|xn--fct429k|xn--fhbei|xn--fiq228c5hs|xn--fiq64b|xn--fiqs8s|xn--fiqz9s|xn--fjq720a|xn--flw351e|xn--fpcrj9c3d|xn--fzc2c9e2c|xn--fzys8d69uvgm|xn--g2xx48c|xn--gckr3f0f|xn--gecrj9c|xn--gk3at1e|xn--h2breg3eve|xn--h2brj9c|xn--h2brj9c8c|xn--hxt814e|xn--i1b6b1a6a2e|xn--imr513n|xn--io0a7i|xn--j1aef|xn--j1amh|xn--j6w193g|xn--jlq480n2rg|xn--jvr189m|xn--kcrx77d1x4a|xn--kprw13d|xn--kpry57d|xn--kput3i|xn--l1acc|xn--lgbbat1ad8j|xn--mgb9awbf|xn--mgba3a3ejt|xn--mgba3a4f16a|xn--mgba7c0bbn0a|xn--mgbaakc7dvf|xn--mgbaam7a8h|xn--mgbab2bd|xn--mgbah1a3hjkrd|xn--mgbai9azgqp6j|xn--mgbayh7gpa|xn--mgbbh1a|xn--mgbbh1a71e|xn--mgbc0a9azcg|xn--mgbca7dzdo|xn--mgbcpq6gpa1a|xn--mgberp4a5d4ar|xn--mgbgu82a|xn--mgbi4ecexp|xn--mgbpl2fh|xn--mgbt3dhd|xn--mgbtx2b|xn--mgbx4cd0ab|xn--mix891f|xn--mk1bu44c|xn--mxtq1m|xn--ngbc5azd|xn--ngbe9e0a|xn--ngbrx|xn--node|xn--nqv7f|xn--nqv7fs00ema|xn--nyqy26a|xn--o3cw4h|xn--ogbpf8fl|xn--otu796d|xn--p1acf|xn--p1ai|xn--pgbs0dh|xn--pssy2u|xn--q7ce6a|xn--q9jyb4c|xn--qcka1pmc|xn--qxa6a|xn--qxam|xn--rhqv96g|xn--rovu88b|xn--rvc1e0am3e|xn--s9brj9c|xn--ses554g|xn--t60b56a|xn--tckwe|xn--tiq49xqyj|xn--unup4y|xn--vermgensberater-ctb|xn--vermgensberatung-pwb|xn--vhquv|xn--vuq861b|xn--w4r85el8fhu5dnra|xn--w4rs40l|xn--wgbh1c|xn--wgbl6a|xn--xhq521b|xn--xkc2al3hye2a|xn--xkc2dl3a5ee0h|xn--y9a3aq|xn--yfro4i67o|xn--ygbi2ammx|xn--zfr164b|xxx|xyz|yachts|yahoo|yamaxun|yandex|ye|yodobashi|yoga|yokohama|you|youtube|yt|yun|za|zappos|zara|zero|zip|zm|zone|zuerich|zw)\b/?(?!@)))"""

COMMON_TLDS = r"""\.(com|net|org|jp|de|uk|fr|br|it|ru|es|me|gov|pl|ca|au|cn|co|in|nl|edu|info|eu|ch|id|at|kr|cz|mx|be|tv|se|tr|tw|al|ua|ir|vn|cl|sk|ly|cc|to|no|fi|us|pt|dk|ar|hu|tk|gr|il|news|ro|my|biz|ie|za|nz|sg|ee|th|io|xyz|pe|bg|hk|rs|lt|link|ph|club|si|site|mobi|by|cat|wiki|la|ga|xxx|cf|hr|ng|jobs|online|kz|ug|gq|ae|is|lv|pro|fm|tips|ms|sa|app|asia|ec|lk|uy|dev)(/|\.|\b)"""
# list of most popular TLDs
# COMMON_TLD = [
#     ".com",
#     ".net",
#     ".org",
#     ".jp",
#     ".de",
#     ".uk",
#     ".fr",
#     ".br",
#     ".it",
#     ".ru",
#     ".es",
#     ".me",
#     ".gov",
#     ".pl",
#     ".ca",
#     ".au",
#     ".cn",
#     ".co",
#     ".in",
#     ".nl",
#     ".edu",
#     ".info",
#     ".eu",
#     ".ch",
#     ".id",
#     ".at",
#     ".kr",
#     ".cz",
#     ".mx",
#     ".be",
#     ".tv",
#     ".se",
#     ".tr",
#     ".tw",
#     ".al",
#     ".ua",
#     ".ir",
#     ".vn",
#     ".cl",
#     ".sk",
#     ".ly",
#     ".cc",
#     ".to",
#     ".no",
#     ".fi",
#     ".us",
#     ".pt",
#     ".dk",
#     ".ar",
#     ".hu",
#     ".tk",
#     ".gr",
#     ".il",
#     ".news",
#     ".ro",
#     ".my",
#     ".biz",
#     ".ie",
#     ".za",
#     ".nz",
#     ".sg",
#     ".ee",
#     ".th",
#     ".io",
#     ".xyz",
#     ".pe",
#     ".bg",
#     ".hk",
#     ".rs",
#     ".lt",
#     ".link",
#     ".ph",
#     ".club",
#     ".si",
#     ".site",
#     ".mobi",
#     ".by",
#     ".cat",
#     ".wiki",
#     ".la",
#     ".ga",
#     ".xxx",
#     ".cf",
#     ".hr",
#     ".ng",
#     ".jobs",
#     ".online",
#     ".kz",
#     ".ug",
#     ".gq",
#     ".ae",
#     ".is",
#     ".lv",
#     ".pro",
#     ".fm",
#     ".tips",
#     ".ms",
#     ".sa",
#     ".app",
#     ".asia",
#     ".ec",
#     ".lk",
#     ".uy",
#     ".dev",
# ]
URLS = re.compile(FIND_URLS)
TLDS = re.compile(COMMON_TLDS)
CONTENT_TYPE_JSON = re.compile(r"Content-Type: application/json")
CONTENT_TYPE_JS = re.compile(r"Content-Type: ?(application|text)/(?:x-)?javascript")
API_ENDPOINTS = re.compile(r"\/api\/[a-zA-Z0-9-_.?&=/]*\b")


def print_result(wordlist):
    # print(wordlist)
    for k, v in wordlist.items():
        if len(v) > 0:
            print("--------")
            print(k, ":", len(v))
            print("--------")
            for i in v:
                print(i)


def write_dict_to_file(my_dict, dir_path):
    # Check if the user has write permissions to the directory
    if not os.access(dir_path, os.W_OK):
        print(
            f"You don't have write permissions to {dir_path}. Please choose a different directory."
        )
        return

    # Create the directory if it doesn't exist
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # Set the filename and check for conflicts
    filename = os.path.join(dir_path, "apis_found.txt")
    while os.path.exists(filename):
        overwrite = input(
            f"The file {filename} already exists. Enter a new filename or press Enter to overwrite: "
        )
        if overwrite == "":
            break
        filename = os.path.join(dir_path, overwrite)

    # Check if the user has write permissions to the file
    if not os.access(os.path.dirname(filename), os.W_OK):
        print(
            f"You don't have write permissions to {os.path.dirname(filename)}. Please choose a different directory."
        )
        return

    # Write the dictionary to the file
    with open(filename, "w") as f:
        for key, value in my_dict.items():
            if value:
                f.write(f"{key}:\n")
                for item in value:
                    f.write(f"{item}\n")
                f.write("\n")

    # Print a message confirming the write operation
    print(f"Dictionary written to file: {filename}")


def write_result(wordlist, output_dir):
    """
    Write the results to a file. It takes a dictionary of lists and it writes the files to a destination folder (it will create it if it doesn't exist), such as the filenames are the keys in the dictionary and the content of the files are the values in the lists
    """
    # Check if the user has write permissions to the directory
    if not os.access(output_dir, os.W_OK):
        print(
            f"You don't have write permissions to {output_dir}. Please choose a different directory."
        )
        return

    # create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # loop over the dictionary items and write the files
    for filename, lines in wordlist.items():
        new_filename = filename + "_wordlistmaker.txt"
        filepath = os.path.join(output_dir, new_filename)

        # Check if the user has write permissions to the file
        if os.path.exists(filepath) and not os.access(filepath, os.W_OK):
            print(
                f"You don't have write permissions to {filepath}. Please choose a different filename."
            )
            continue

        # Check if the file already exists and ask the user for a new filename if there's a conflict
        while os.path.exists(filepath):
            overwrite = input(
                f"The file {filepath} already exists. Enter a new filename or press Enter to overwrite: "
            )
            if overwrite == "":
                break
            new_filename = overwrite + "_wordlistmaker"
            filepath = os.path.join(output_dir, new_filename)

        if len(lines) > 0:
            with open(filepath, "w") as f:
                for line in lines:
                    f.write(line + "\n")


def find_api_endpoints_in_js(burp_file):
    """Find all the API endpoints inside all js responses of a Burp Suite XML file"""
    api_endpoints = set()
    api_found_in_js = dict()
    url = ""
    for event, elem in ET.iterparse(burp_file):
        if elem.tag == "url":
            url = elem.text
        if elem.tag == "response" and elem.attrib["base64"] == "true":
            decoded_text = str(base64.b64decode(elem.text))
            decoded_text = unquote(decoded_text)
            decoded_text = html.unescape(decoded_text)
            decoded_text = decoded_text.replace("\\", "").replace("u002F", "/")
            if CONTENT_TYPE_JS.search(decoded_text):
                # Look for API endpoints in decoded text
                endpoints = API_ENDPOINTS.findall(decoded_text)
                # api_endpoints.update(endpoints)
                # add each API endpoint to the dictionary
                api_found_in_js.setdefault(url, set()).update(endpoints)

        if elem.tag == "item":
            elem.clear()

    # Return the list of unique API endpoints found
    # api_endpoints_list = list(api_endpoints)
    # api_endpoints_list.sort()
    return api_found_in_js


def get_all_keys(json_obj):
    """
    Recursively extract all keys from a nested JSON object
    """
    keys = set()
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            keys.add(key)
            keys.update(get_all_keys(value))
    elif isinstance(json_obj, list):
        for item in json_obj:
            keys.update(get_all_keys(item))
    return keys


def get_json_keys(burp_file):
    """Find all the JSON keys inside a Burp Suite XML file"""
    json_keys = set()
    # Check the Content-Type inside the response. If it is application/json, then parse the JSON and extract all the keys.
    try:
        for event, elem in ET.iterparse(burp_file):
            if elem.tag == "response" and elem.attrib["base64"] == "true":
                decoded_text = str(base64.b64decode(elem.text))
                decoded_text = unquote(decoded_text)
                decoded_text = html.unescape(decoded_text)
                decoded_text = decoded_text.replace("\\", "").replace("u002F", "/")
                if CONTENT_TYPE_JSON.search(decoded_text):
                    # split the response into headers and body
                    headers, body = decoded_text.split("rnrn", 1)
                    # Remove any extra characters from the end of the body and load the JSON data
                    last_brace_index = body.rfind("}")
                    json_obj_str = body[: last_brace_index + 1]
                    body = json.loads(json_obj_str)
                    # Extract all the JSON keys from the body
                    json_keys.update(get_all_keys(body))
            elif elem.tag == "response" and elem.attrib["base64"] == "false":
                print(
                    'Looks like the requests and responses are not Base64 encoded. To get more results, make sure to select "Base64-encode requests and responses" when saving the items from Burp Suite Site map.'
                )
            if elem.tag == "item":
                elem.clear()
    except ET.ParseError as err:
        print(err)
    return json_keys


def filter_urls_by_domains(urls, domains):
    """
    Filters a list of URLs by a list of domains.

    Parameters:
        urls (list of str): The list of URLs to filter.
        domains (list of str): The list of domains to filter by.

    Returns:
        list of str: A new list containing only the URLs that contain any of the specified domains.

    Example:
        >>> urls = ['https://www.example.com/login.php', 'https://www.example.org/about.php']
        >>> domains = ['example.com']
        >>> filtered_urls = filter_urls_by_domains(urls, domains)
        >>> filtered_urls
        ['https://www.example.com/login.php']
    """
    if len(domains) == 0:
        return urls
    return [url for url in urls if any(domain in url for domain in domains)]


def get_endpoints(burp_file, in_scope_domains=[]):
    """
    Searches for endpoints in a Burp Suite XML file and returns them in a dictionary.

    Parameters:
        burp_file (str): The path to the Burp Suite XML file to process.
        in_scope_domains (list of str, optional): A list of domains to filter the results by. If empty (default), all endpoints found will be returned.

    Returns:
        dict: A dictionary containing the following keys:
            'urls' (list of str): A list of unique URLs found in the XML file.
            'javascript files' (list of str): A list of unique JavaScript file URLs found in the XML file.
            'probably false positives' (list of str): A list of unique URLs that might be false positives, i.e., not actual endpoints.

    Raises:
        xml.etree.ElementTree.ParseError: If there is an error parsing the XML file.

    Example:
        >>> burp_file = 'example.xml'
        >>> in_scope_domains = ['example.com']
        >>> endpoints = get_endpoints(burp_file, in_scope_domains)
        >>> endpoints['urls']
        ['https://www.example.com/login.php', 'https://www.example.com/logout.php']
        >>> endpoints['javascript files']
        ['https://www.example.com/js/jquery.min.js', 'https://www.example.com/js/bootstrap.min.js']
        >>> endpoints['probably false positives']
        ['abc.name']
    """
    urls_found = set()
    js_found = set()
    false_positives = set()
    endpoints_found = dict()
    try:
        for event, elem in ET.iterparse(burp_file):
            if elem.tag == "url":
                urls_found.update(filter_urls_by_domains([elem.text], in_scope_domains))

            if elem.tag == "request" and elem.attrib["base64"] == "true":
                elem.text = str(base64.b64decode(elem.text))
                elem.text = unquote(elem.text)
                urls = URLS.findall(elem.text)
                for url in urls:
                    suffix = Path(urlparse(url).path).suffix
                    if suffix != ".js" and suffix != ".map":
                        urls_found.update(
                            filter_urls_by_domains([url], in_scope_domains)
                        )
                    elif suffix == ".js" or suffix == ".map":
                        js_found.add(url)

            if elem.tag == "response" and elem.attrib["base64"] == "true":
                try:
                    decoded_text = str(base64.b64decode(elem.text))
                    decoded_text = unquote(decoded_text)
                    decoded_text = html.unescape(decoded_text)
                    decoded_text = decoded_text.replace("\\", "").replace("u002F", "/")
                    urls = URLS.findall(decoded_text)

                    for url in urls:
                        parsed_url = urlparse(url)
                        path_suffix = Path(parsed_url.path).suffix
                        
                        if not TLDS.search(url) and (path_suffix != ".js" and path_suffix != ".map"):
                            false_positives.add(url)
                        elif path_suffix == ".js" or path_suffix == ".map":
                            js_found.add(url)
                        elif TLDS.search(url) and url not in false_positives and url not in js_found:
                            urls_found.update(
                                filter_urls_by_domains([url], in_scope_domains)
                            )
                # catch a TypeError if the response is empty
                except TypeError:
                    pass
                    
            elif elem.tag == "response" and elem.attrib["base64"] == "false":
                print(
                    'Looks like the requests and responses are not Base64 encoded. To get more results, make sure to select "Base64-encode requests and responses" when saving the items from Burp Suite Site map.'
                )
            if elem.tag == "item":
                elem.clear()
    except ET.ParseError as err:
        print(err)

    url_list = list(urls_found)
    js_list = list(js_found)
    false_positives_list = list(false_positives)
    url_list.sort()
    js_list.sort()
    false_positives_list.sort()
    endpoints_found["urls"] = url_list
    endpoints_found["javascript_files"] = js_list
    endpoints_found["probably_false_positives"] = false_positives_list
    return endpoints_found


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
        # Non sono sicuro se voglio decodificare o no. Per decodificare, uncommentare la riga sotto.
        # word = unquote(Path(urlparse(url).path).name)
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
            if query[0] not in param_names_list and query[0] != "":
                param_names_list.append(query[0])
        else:
            query = query[::2]
            for param in query:
                if param not in param_names_list and param != "":
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
            if query[1] not in param_values_list and query[1] != "":
                param_values_list.append(query[1])
        else:
            query = query[1::2]
            for param in query:
                if param not in param_values_list and param != "":
                    param_values_list.append(param)
    param_values_list.sort()
    return param_values_list


def command_line_parser():
    parser = argparse.ArgumentParser(
        description="Take a list of URLs or a Burp Suite XML file as input and get a list of: directories, files, parameters names, parameters values and links."
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("-u", "--url", help="Path to a list of URLs.")
    input_group.add_argument("-b", "--burp-file", help="Path to a Burp XML file.")
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
    parser.add_argument("-is", "--in-scope", help="in-scope domains", nargs="*")
    parser.add_argument("-o", "--output", help="path to the output file")
    parser.add_argument(
        "-e",
        "--endpoints",
        help="find all endpoints from the Burp file",
        action="store_true",
    )
    parser.add_argument(
        "-jk", "--json-keys", help="find all json keys", action="store_true"
    )
    parser.add_argument("-A", "--all", help="find all", action="store_true")
    parser.add_argument(
        "-a", "--api", help="find all api endpoints", action="store_true"
    )

    return parser


def check_file(file_path):
    if not os.path.exists(file_path):
        sys.exit(f"No such file or directory: {file_path}")
    if os.stat(file_path).st_size == 0:
        sys.exit(f"The file is empty: {file_path}")


def get_all_items(args, source_list):
    items = {
        "directories": get_directories(source_list),
        "files": get_files(source_list),
        "param_names": get_param_names(source_list),
        "param_values": get_param_values(source_list),
    }
    if args["burp_file"]:
        items["json_keys"] = get_json_keys(args["burp_file"])
    return items


def remove_numbers_from_wordlist(wordlist, no_numbers):
    for key in no_numbers:
        if key in wordlist:
            wordlist[key] = remove_numbers(wordlist[key])
    return wordlist


def remove_nonprintable_chars_from_wordlist(wordlist):
    for key, value in wordlist.items():
        wordlist[key] = remove_nonprintable_chars(value)
    return wordlist


def main():
    """Takes input from the cli, pass it to the parsing functions and then returns
    the wordlist.
    """
    wordlist = {
        "directories": [],
        "files": [],
        "param_names": [],
        "param_values": [],
        "json_keys": [],
    }
    endpoints = dict()
    api_endpoints = dict()
    url_list = []

    parser = command_line_parser()
    args = vars(parser.parse_args())

    # if not args["output"]:
    #     sys.exit("Please provide a path where to save the wordlist with the -o option.")
    if args["burp_file"]:
        check_file(args["burp_file"])
        print("Parsing ", args["burp_file"], "...")
        if args["endpoints"]:
            if args["in_scope"]:
                endpoints = get_endpoints(args["burp_file"], args["in_scope"])
            else:
                endpoints = get_endpoints(args["burp_file"])
        if args["api"]:
            api_endpoints = find_api_endpoints_in_js(args["burp_file"])
    elif args["url"]:
        check_file(args["url"])
        with open((args["url"]), encoding="utf 8") as f:
            print("Parsing ", args["url"], "...")
            for line in f:
                url = line.strip()
                url_list.append(url)
    else:
        parser.print_help()
        sys.exit()

    source_list = None
    if args["burp_file"]:
        if args["endpoints"]:
            source_list = endpoints["urls"]
        else:
            source_list = get_endpoints(args["burp_file"])["urls"]
    elif args["url"]:
        source_list = url_list

    if args["all"]:
        wordlist.update(get_all_items(args, source_list))
    else:
        if args["directories"]:
            wordlist["directories"] = get_directories(source_list)
        if args["files"]:
            wordlist["files"] = get_files(source_list)
        if args["param_names"]:
            wordlist["param_names"] = get_param_names(source_list)
        if args["param_values"]:
            wordlist["param_values"] = get_param_values(source_list)
        if args["json_keys"]:
            if args["url"]:
                sys.exit(
                    "The --json-keys option is only available with the --burp-file option."
                )
            else:
                wordlist["json_keys"] = get_json_keys(args["burp_file"])
    if args["no_numbers"]:
        wordlist = remove_numbers_from_wordlist(wordlist, args["no_numbers"])

    if args["nonprintable"]:
        wordlist = remove_nonprintable_chars_from_wordlist(wordlist)

    if args["all_files"]:
        wordlist["files"] = show_all_files(wordlist["files"])

    wordlist.update(endpoints)
    if api_endpoints:
        write_dict_to_file(api_endpoints, args["output"])

    if any(wordlist.values()):
        # write_result(wordlist, args["output"])
        print_result(wordlist)

    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
    tracemalloc.stop()


if __name__ == "__main__":
    main()
