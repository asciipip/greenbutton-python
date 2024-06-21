# Green Button Objects

This Python code parses an Energy Service Provider Interface
(ESPI), or "Green Button", XML file into Python objects.

Run `parse_feed()` from the `parse.py` file to get a list of `UsagePoint`
objects.  From there you should be able to explore all of the data in the
feed.  Documentation is a little lacking at the moment, but the class
members mostly match the names from the ESPI standard (or at least the XML
entities).

There's a bit of documentation in the `doc` directory about the ESPI
standard, mostly figured out from public sources and actual ESPI files.

Forked from the original repository [greenbutton-objects](https://github.com/asciipip/greenbutton-python)
and packaged to be published on PyPI.


## Development
Simple steps for development setup:

1. Clone the git repository.
3. Navigate to any directory and create a [virtual environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments) and activate it
4. The following commands can be run from inside the top-level greenbutton_objects folder while the virtual environment is active
2. `pip install -e .` builds the [python egg](https://stackoverflow.com/questions/2051192/what-is-a-python-egg) for greenbutton_objects and then installs greenbutton_objects
3. `pip install -r requirements-dev.txt` which installs the libraries required to develop greenbutton_objects

Then, you should be able to run `pytest`, also from any directory, and see the test run successfully.