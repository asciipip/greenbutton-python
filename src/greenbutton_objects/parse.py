#!/usr/bin/python

import sys
import xml.etree.ElementTree as ET

from greenbutton_objects import resources
from greenbutton_objects import utils

def parse_feed(filename):
    tree = ET.parse(filename)

    usagePoints = []
    for entry in tree.getroot().findall('atom:entry/atom:content/espi:UsagePoint/../..', utils.ns):
        up = resources.UsagePoint(entry)
        usagePoints.append(up)
    
    meterReadings = []    
    for entry in tree.getroot().findall('atom:entry/atom:content/espi:MeterReading/../..', utils.ns):
        mr = resources.MeterReading(entry, usagePoints=usagePoints)
        meterReadings.append(mr)

    readingTypes = []
    for entry in tree.getroot().findall('atom:entry/atom:content/espi:ReadingType/../..', utils.ns):
        rt = resources.ReadingType(entry, meterReadings=meterReadings)
        readingTypes.append(rt)

    intervalBlocks = []
    for entry in tree.getroot().findall('atom:entry/atom:content/espi:IntervalBlock/../..', utils.ns):
        ib = resources.IntervalBlock(entry, meterReadings=meterReadings)
        intervalBlocks.append(ib)
    
    return usagePoints


def parse_feed_representation(usage_points) -> str:
    """
    Return a string representation of the parsing result.

    The representation includes the Usage Points, Meter Readings, and
    Interval Readings.
    """
    result = []
    for up in usage_points:
        result.append(
            "UsagePoint (%s) %s %s:" % (up.title, up.serviceCategory.name, up.status)
        )
        for mr in up.meterReadings:
            result.append(
                "  Meter Reading (%s) %s:" % (mr.title, mr.readingType.uom.name)
            )
            result.append("\n")
            for ir in mr.intervalReadings:
                result.append(
                    "    %s, %s: %s %s"
                    % (
                        ir.timePeriod.start,
                        ir.timePeriod.duration,
                        ir.value,
                        ir.value_symbol,
                    )
                )
                if ir.cost is not None:
                    result.append("(%s%s)" % (ir.cost_symbol, ir.cost))
                if len(ir.readingQualities) > 0:
                    result.append(
                        "[%s]"
                        % ", ".join([rq.quality.name for rq in ir.readingQualities])
                    )
                result.append("\n\n")
    return "".join(result)


if __name__ == "__main__":
    usage_points = parse_feed(sys.argv[1])
    representation = parse_feed_representation(usage_points)
    print(representation)