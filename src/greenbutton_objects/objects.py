#!/usr/bin/python

import datetime
import functools

from greenbutton_objects import enums
from greenbutton_objects import utils


@functools.total_ordering
class DateTimeInterval:
    def __init__(self, entity):
        self.duration = utils.getEntity(entity, 'espi:duration',
                                  lambda e: datetime.timedelta(seconds=int(e.text)))
        self.start = utils.getEntity(entity, 'espi:start',
                               lambda e: datetime.datetime.fromtimestamp(int(e.text)))
        
    def __repr__(self):
        return '<DateTimeInterval (%s, %s)>' % (self.start, self.duration)

    def __eq__(self, other):
        if not isinstance(other, DateTimeInterval):
            return False
        return (self.start, self.duration) == (other.start, other.duration)
    
    def __lt__(self, other):
        if not isinstance(other, DateTimeInterval):
            return False
        return (self.start, self.duration) < (other.start, other.duration)

    
@functools.total_ordering
class IntervalReading:
    def __init__(self, entity, parent):
        self.intervalBlock = parent
        self.cost = utils.getEntity(entity, 'espi:cost', lambda e: int(e.text) / 100000.0)
        self.timePeriod = utils.getEntity(entity, 'espi:timePeriod',
                                    lambda e: DateTimeInterval(e))
        self._value = utils.getEntity(entity, 'espi:value', lambda e: int(e.text))

        self.readingQualities = set([ReadingQuality(rq, self) for rq in entity.findall('espi:ReadingQuality', utils.ns)])
        
    def __repr__(self):
        return '<IntervalReading (%s, %s: %s %s)>' % (self.timePeriod.start, self.timePeriod.duration, self.value, self.value_symbol)

    def __eq__(self, other):
        if not isinstance(other, IntervalReading):
            return False
        return (self.timePeriod, self.value) == (other.timePeriod, other.value)
    
    def __lt__(self, other):
        if not isinstance(other, IntervalReading):
            return False
        return (self.timePeriod, self.value) < (other.timePeriod, other.value)
    
    @property
    def value(self):
        if self.intervalBlock is not None and \
           self.intervalBlock.meterReading is not None and \
           self.intervalBlock.meterReading.readingType is not None and \
           self.intervalBlock.meterReading.readingType.powerOfTenMultiplier is not None:
            multiplier = 10 ** self.intervalBlock.meterReading.readingType.powerOfTenMultiplier
        else:
            multiplier = 1
        return self._value * multiplier

    @property
    def cost_units(self):
        if self.intervalBlock is not None and \
           self.intervalBlock.meterReading is not None and \
           self.intervalBlock.meterReading.readingType is not None and \
           self.intervalBlock.meterReading.readingType.currency is not None:
            return self.intervalBlock.meterReading.readingType.currency
        else:
            return enums.CurrencyCode.na

    @property
    def cost_symbol(self):
        return self.cost_units.symbol

    @property
    def value_units(self):
        if self.intervalBlock is not None and \
           self.intervalBlock.meterReading is not None and \
           self.intervalBlock.meterReading.readingType is not None and \
           self.intervalBlock.meterReading.readingType.uom is not None:
            return self.intervalBlock.meterReading.readingType.uom
        else:
            return enums.UomType.notApplicable

    @property
    def value_symbol(self):
        return enums.UOM_SYMBOLS[self.value_units]
        
class ReadingQuality:
    def __init__(self, entity, parent):
        self.intervalReading = parent
        self.quality = utils.getEntity(entity, 'espi:quality', lambda e: enums.QualityOfReading(int(e.text)))
