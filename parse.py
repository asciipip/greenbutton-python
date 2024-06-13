#!/usr/bin/python

import sys
import xml.etree.ElementTree as ET

from resources import *

def parse_feed(filename):
    tree = ET.parse(filename)

    usagePoints = []
    for entry in tree.getroot().findall('atom:entry/atom:content/espi:UsagePoint/../..', ns):
        up = UsagePoint(entry)
        usagePoints.append(up)
    
    meterReadings = []    
    for entry in tree.getroot().findall('atom:entry/atom:content/espi:MeterReading/../..', ns):
        mr = MeterReading(entry, usagePoints=usagePoints)
        meterReadings.append(mr)

    readingTypes = []
    for entry in tree.getroot().findall('atom:entry/atom:content/espi:ReadingType/../..', ns):
        rt = ReadingType(entry, meterReadings=meterReadings)
        readingTypes.append(rt)

    intervalBlocks = []
    for entry in tree.getroot().findall('atom:entry/atom:content/espi:IntervalBlock/../..', ns):
        ib = IntervalBlock(entry, meterReadings=meterReadings)
        intervalBlocks.append(ib)
    
    return usagePoints

if __name__ == '__main__':
    ups = parse_feed(sys.argv[1])
    for up in ups:
        print('UsagePoint (%s) %s %s:' % (up.title, up.serviceCategory.name, up.status))
        for mr in up.meterReadings:
            print('  Meter Reading (%s) %s:' % (mr.title, mr.readingType.uom.name))
            for ir in mr.intervalReadings:
                print('    %s, %s: %s %s' % (ir.timePeriod.start, ir.timePeriod.duration, ir.value, ir.value_symbol),
                      end=' ')
                if ir.cost is not None:
                    print('(%s%s)' % (ir.cost_symbol, ir.cost), end=' ')
                if len(ir.readingQualities) > 0:
                    print('[%s]' % ', '.join([rq.quality.name for rq in ir.readingQualities]), end=' ')
                print()