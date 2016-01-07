#!/usr/bin/python

import bisect
import functools

from utils import *
from enums import *
from objects import *

class Resource(object):
    def __init__(self, entry):
        self.link_self    = getLink(entry, 'self')
        self.link_up      = getLink(entry, 'up')
        self.link_related = getLink(entry, 'related', True)
        self.title = getEntity(entry, 'atom:title', lambda e: e.text)

    def __repr__(self):
        return '<%s (%s)>' % (self.__class__.__name__, self.title or self.link_self)

    def isParentOf(self, other):
        return other.link_self in self.link_related or other.link_up in self.link_related

    
class UsagePoint(Resource):
    def __init__(self, entry, meterReadings=[]):
        super(UsagePoint, self).__init__(entry)
        obj = entry.find('./atom:content/espi:UsagePoint', ns)
        self.roleFlags = getEntity(obj, 'espi:roleFlags', lambda e: int(e.text, 16))
        self.status = getEntity(obj, 'espi:status', lambda e: int(e.text))
        self.serviceCategory = getEntity(obj, './espi:ServiceCategory/espi:kind',
                                         lambda e: ServiceKind(int(e.text)))
        
        self.meterReadings = set()
        for mr in meterReadings:
            if self.isParentOf(mr):
                self.addMeterReading(mr)

    def addMeterReading(self, meterReading):
        assert self.isParentOf(meterReading)
        self.meterReadings.add(meterReading)
        meterReading.usagePoint = self

        
class MeterReading(Resource):
    def __init__(self, entry, usagePoints=[], readingTypes=[], intervalBlocks=[]):
        super(MeterReading, self).__init__(entry)

        self.usagePoint = None
        self.readingType = None
        self.intervalBlocks = []
        for up in usagePoints:
            if up.isParentOf(self):
                up.addMeterReading(self)
        for rt in readingTypes:
            if self.isParentOf(rt):
                self.setReadingType(rt)
        for ib in intervalBlocks:
            if self.isParentOf(ib):
                self.addIntervalBlock(r)

    @property
    def intervalReadings(self):
        for ib in self.intervalBlocks:
            for ir in ib.intervalReadings:
                yield ir
                
    def setReadingType(self, readingType):
        assert self.isParentOf(readingType)
        assert self.readingType is None or self.readingType.link_self == readingType.link_self
        self.readingType = readingType
        readingType.meterReading = self

    def addIntervalBlock(self, intervalBlock):
        assert self.isParentOf(intervalBlock)
        bisect.insort(self.intervalBlocks, intervalBlock)
        intervalBlock.meterReading = self


class ReadingType(Resource):
    def __init__(self, entry, meterReadings=[]):
        super(ReadingType, self).__init__(entry)
        self.meterReading = None

        obj = entry.find('./atom:content/espi:ReadingType', ns)
        self.accumulationBehaviour = getEntity(obj, 'espi:accumulationBehaviour',
                                               lambda e: AccumulationBehaviourType(int(e.text)))
        self.commodity = getEntity(obj, 'espi:commodity',
                                   lambda e: CommodityType(int(e.text)))
        self.consumptionTier = getEntity(obj, 'espi:consumptionTier',
                                         lambda e: ConsumptionTierType(int(e.text)))
        self.currency = getEntity(obj, 'espi:currency',
                                  lambda e: CurrencyCode(int(e.text)))
        self.dataQualifier = getEntity(obj, 'espi:dataQualifier',
                                       lambda e: DataQualifierType(int(e.text)))
        self.defaultQuality = getEntity(obj, 'espi:defaultQuality',
                                        lambda e: QualityOfReading(int(e.text)))
        self.flowDirection = getEntity(obj, 'espi:flowDirection',
                                       lambda e: FlowDirectionType(int(e.text)))
        self.intervalLength = getEntity(obj, 'espi:intervalLength', lambda e: int(e.text))
        self.kind = getEntity(obj, 'espi:kind', lambda e: KindType(int(e.text)))
        self.phase = getEntity(obj, 'espi:phase', lambda e: PhaseCode(int(e.text)))
        self.powerOfTenMultiplier = getEntity(obj, 'espi:powerOfTenMultiplier',
                                              lambda e: int(e.text))
        self.timeAttribute = getEntity(obj, 'espi:timeAttribute',
                                       lambda e: TimeAttributeType(int(e.text)))
        self.tou = getEntity(obj, 'espi:tou', lambda e: TOUType(int(e.text)))
        self.uom = getEntity(obj, 'espi:uom', lambda e: UomType(int(e.text)))

        for mr in meterReadings:
            if mr.isParentOf(self):
                mr.setReadingType(self)


@functools.total_ordering
class IntervalBlock(Resource):
    def __init__(self, entry, meterReadings=[]):
        super(IntervalBlock, self).__init__(entry)
        self.meterReading = None

        obj = entry.find('./atom:content/espi:IntervalBlock', ns)
        self.interval = getEntity(obj, 'espi:interval', lambda e: DateTimeInterval(e))
        self.intervalReadings = sorted([IntervalReading(ir, self) for ir in obj.findall('espi:IntervalReading', ns)])
            
        for mr in meterReadings:
            if mr.isParentOf(self):
                mr.addIntervalBlock(self)

    def __eq__(self, other):
        if not isinstance(other, IntervalBlock):
            return False
        return self.link_self == other.link_self
    
    def __lt__(self, other):
        return self.interval < other.interval
    
