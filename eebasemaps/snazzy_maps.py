import requests
import json
import argparse
from bs4 import BeautifulSoup


def snazzy(url):
    """This tool allows you to grab a snazzy basemap url from the main page and convert it into a GEE snippet

    [Snazzy maps is an open source js repo with multiple user contributed maps that can be repurposed an can be added to GEE]

    Arguments:
        url {[Snazzy maps url]} -- [Snazzy maps url for basemaps from snazzymaps.com]
    """
    bad_chars = ["*", "!", " ", "'"]
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    declaration = soup.title.string.strip().split("\n")[0]
    for i in bad_chars:
        declaration = declaration.replace(i, "")
    print("var {} = ".format(declaration))
    for a in soup.find("pre"):
        z = a.string
        data = json.loads(z)
        print(json.dumps(data, indent=2))
    mapadd = soup.title.string.strip().split("\n")[0]
    for i in bad_chars:
        mapadd = mapadd.replace(i, "")
    print(
        "Map.setOptions('mapStyle', {mapStyle: ".replace("mapStyle", mapadd)
        + mapadd
        + "})"
    )


# snazzy(url = "")


def eesnazzy_from_parser(args):
    snazzy(url=args.url)


def main(args=None):
    parser = argparse.ArgumentParser(
        description="Google Earth Engine Snazzy Basemaps tool"
    )
    parser.add_argument("--url", help="Snazzy maps URL from https://snazzymaps.com/", required=True)
    parser.set_defaults(func=eesnazzy_from_parser)
    args = parser.parse_args()

    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")
    func(args)


if __name__ == "__main__":
    main()
