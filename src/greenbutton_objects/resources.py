#!/usr/bin/python

import bisect
import functools

from greenbutton_objects import utils
from greenbutton_objects import enums
from greenbutton_objects import objects

class Resource(object):
    def __init__(self, entry):
        self.link_self = utils.getLink(entry, 'self')
        self.link_up = utils.getLink(entry, 'up')
        self.link_related = utils.getLink(entry, 'related', True)
        self.title = utils.getEntity(entry, 'atom:title', lambda e: e.text)

    def __repr__(self):
        return '<%s (%s)>' % (self.__class__.__name__, self.title or self.link_self)

    def isParentOf(self, other):
        return other.link_self in self.link_related or other.link_up in self.link_related

    
class UsagePoint(Resource):
    def __init__(self, entry, meterReadings=[]):
        super(UsagePoint, self).__init__(entry)
        obj = entry.find('./atom:content/espi:UsagePoint', utils.ns)
        self.roleFlags = utils.getEntity(obj, 'espi:roleFlags', lambda e: int(e.text, 16))
        self.status = utils.getEntity(obj, 'espi:status', lambda e: int(e.text))
        self.serviceCategory = utils.getEntity(obj, './espi:ServiceCategory/espi:kind',
                                         lambda e: enums.ServiceKind(int(e.text)))
        
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

        obj = entry.find('./atom:content/espi:ReadingType', utils.ns)
        self.accumulationBehaviour = utils.getEntity(obj, 'espi:accumulationBehaviour',
                                               lambda e: enums.AccumulationBehaviourType(int(e.text)))
        self.commodity = utils.getEntity(obj, 'espi:commodity',
                                   lambda e: enums.CommodityType(int(e.text)))
        self.consumptionTier = utils.getEntity(obj, 'espi:consumptionTier',
                                         lambda e: enums.ConsumptionTierType(int(e.text)))
        self.currency = utils.getEntity(obj, 'espi:currency',
                                  lambda e: enums.CurrencyCode(int(e.text)))
        self.dataQualifier = utils.getEntity(obj, 'espi:dataQualifier',
                                       lambda e: enums.DataQualifierType(int(e.text)))
        self.defaultQuality = utils.getEntity(obj, 'espi:defaultQuality',
                                        lambda e: enums.QualityOfReading(int(e.text)))
        self.flowDirection = utils.getEntity(obj, 'espi:flowDirection',
                                       lambda e: enums.FlowDirectionType(int(e.text)))
        self.intervalLength = utils.getEntity(obj, 'espi:intervalLength', lambda e: int(e.text))
        self.kind = utils.getEntity(obj, 'espi:kind', lambda e: enums.KindType(int(e.text)))
        self.phase = utils.getEntity(obj, 'espi:phase', lambda e: enums.PhaseCode(int(e.text)))
        self.powerOfTenMultiplier = utils.getEntity(obj, 'espi:powerOfTenMultiplier',
                                              lambda e: int(e.text))
        self.timeAttribute = utils.getEntity(obj, 'espi:timeAttribute',
                                       lambda e: enums.TimeAttributeType(int(e.text)))
        self.tou = utils.getEntity(obj, 'espi:tou', lambda e: enums.TOUType(int(e.text)))
        self.uom = utils.getEntity(obj, 'espi:uom', lambda e: enums.UomType(int(e.text)))

        for mr in meterReadings:
            if mr.isParentOf(self):
                mr.setReadingType(self)


@functools.total_ordering
class IntervalBlock(Resource):
    def __init__(self, entry, meterReadings=[]):
        super(IntervalBlock, self).__init__(entry)
        self.meterReading = None

        obj = entry.find('./atom:content/espi:IntervalBlock', utils.ns)
        self.interval = utils.getEntity(obj, 'espi:interval', lambda e: objects.DateTimeInterval(e))
        self.intervalReadings = sorted([objects.IntervalReading(ir, self) for ir in obj.findall('espi:IntervalReading', utils.ns)])
            
        for mr in meterReadings:
            if mr.isParentOf(self):
                mr.addIntervalBlock(self)

    def __eq__(self, other):
        if not isinstance(other, IntervalBlock):
            return False
        return self.link_self == other.link_self
    
    def __lt__(self, other):
        return self.interval < other.interval
    
