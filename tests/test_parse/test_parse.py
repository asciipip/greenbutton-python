"""
asdf
"""

import os
import pathlib
from pathlib import Path

from greenbutton_objects import parse

_ROOT_DIR = pathlib.Path(__file__).parent


def _save_representation(test_xml_path: Path, test_output_path: Path) -> None:
    """
    Parse an XML feed, generate a representation, and save it to a text
    file.
    """
    parsed_feed = parse.parse_feed(test_xml_path)
    representation = parse.parse_feed_representation(parsed_feed)
    with open(test_output_path, "w") as f:
        f.write(representation)


def save_expected_results():
    """
    Save the expected results of parsing each XML file of test data.

    Should be run only to update the expected results of parsing XML
    data or representing parsed data.
    """
    data_path = _ROOT_DIR / "data"
    expected_results_path = _ROOT_DIR / "expected_results"

    def save(energy_source):
        for data_file_name in os.listdir(data_path / energy_source):
            result_file_name = data_file_name.strip("xml") + "txt"
            _save_representation(
                data_path / energy_source / data_file_name,
                expected_results_path / energy_source / result_file_name,
            )

    save("electricity")
    save("natural_gas")


def test_parse_feed():
    """
    Verify that parsing an XML file works as intended.

    Compares the string form of a parsed XML to a saved text file.
    """
    data_path = _ROOT_DIR / "data"
    expected_results_path = _ROOT_DIR / "expected_results"

    def verify(energy_source):
        for data_file_name in os.listdir(data_path / energy_source):
            parsed_feed = parse.parse_feed(data_path / energy_source / data_file_name)
            parsed_feed_representation = parse.parse_feed_representation(parsed_feed)
            result_file_name = data_file_name.strip("xml") + "txt"
            expected_results_file = (
                expected_results_path / energy_source / result_file_name
            )
            with open(expected_results_file) as f:
                assert f.read() == parsed_feed_representation

    verify("electricity")
    verify("natural_gas")


if __name__ == "__main__":
    save_expected_results()
