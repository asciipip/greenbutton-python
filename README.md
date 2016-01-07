This is some python code to parse an Energy Service Provider Interface
(ESPI), or "Green Button" XML file into Python objects.

Run `parse_feed()` from the `parse.py` file to get a list of `UsagePoint`
objects.  From there you should be able to explore all of the data in the
feed.  Documentation is a little lacking at the moment, but the class
members mostly match the names from the ESPI standard (or at least the XML
entities).

There's a bit of documentation in the `doc` directory about the ESPI
standard, mostly figured out from public sources and actual ESPI files.
