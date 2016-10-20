# pq

`pq` is a command line xml and json processor for xpath and css selectors, inspired by [`jq`](https://github.com/stedolan/jq).

`pq` uses [`parsel`](https://github.com/scrapy/parsel) with the help of [`dicttoxml`](https://github.com/quandyfactory/dicttoxml) to parse `json` or `xml` files using **xpath** or **css selectors**.

Try it out with:

    pip install git+https://github.com/granitosaurus/pq


# usage

    Usage: pq [OPTIONS] QUERY [INFILE]

      Command line xml and json processor for xpath and css selectors.

    Options:
      --css            use css selectors instead of xpath
      -t, --text       get only the text (no markup)
      -c, --compact    compact instead of pretty-printed output
      -tt, --text_all  like to_text but gets all text including node's children
      -f, --first      only the first element
      --help           Show this message and exit.

# examples
## parse xml
To parse xml/html text we can use xpath or css.  
We can parse this `example.xml` file:

    <widget>
        <image src="Images/Sun.png" name="sun1">
            <hOffset>250</hOffset>
            <vOffset>250</vOffset>
            <alignment>center</alignment>
        </image>
    </widget>

By piping it's content to `pq` and supplying either xpath or css selector:

    # default xpath
    $ cat example.xml | pq "//image/voffset/text()"  
    # or css
    $ cat example.xml | pq "image voffset::text" --css
    [
        "250"
    ]

## parse json    
Same with json:

    {"widget": {
        "image": { 
            "src": "Images/Sun.png",
            "name": "sun1",
            "hOffset": 250,
            "vOffset": 250,
            "alignment": "center"
        },
    }}  

And to parse it:

    masterdex@~/projects/parsel-query
    $ cat example.json | pq "//image/voffset/text()"  
    [
        "250"
    ]

## recipes

Use curl to download json source and parse it:

    $ curl "https://httpbin.org/get" -s | pq '//host' --text --first
    "httpbin.org"

Same with html:
    
    $ curl "https://github.com" -s | pq "//h2" --text --first
    "Welcome home, developers"
    
Sometimes css is shorter and prettier than xpath:

    $ curl "https://github.com" -s | pq ".pricing-card-text" --first --css --text
    "\n        Public projects are always free. Work together across unlimited private repositories for $7 / month.\n      "
