"""
Condé Nast API example

(c) leocelis.com
"""
import pprint
from io import BytesIO

import requests
import ujson
from PIL import Image
from pygments import highlight, lexers, formatters

# print format
pp = pprint.PrettyPrinter(indent=4)

# Conde Nast APIs
covers_api = "http://covers.condenast.co.uk/api/v1/{}/current/image/"
brands_api = "http://covers.condenast.co.uk/api/v1"

try:
    # get brands list
    r = requests.get(brands_api, )
    brands_list = r.json()
    formatted_json = ujson.dumps(brands_list, sort_keys=True, indent=4)
    colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
    print(colorful_json)

    # for each brand
    for b in brands_list.get('data', {}).get('brands', {}):
        slug = b.get('slug')

        # get current cover
        if slug:
            wired_cover = covers_api.format(slug)
            r = requests.get(wired_cover)
            img = Image.open(BytesIO(r.content))
            img.show()

except (requests.ConnectionError, requests.Timeout) as e:
    print("Oops! {}".format(str(e)))
