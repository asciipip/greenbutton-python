#!/usr/bin/python
# -*- coding: utf-8 -*-

from enum import Enum

class AccumulationBehaviourType(Enum):
    notApplicable = 0
    bulkQuantity = 1
    cumulative = 3
    deltaData = 4
    indicating = 6
    summation = 9
    instantaneous = 12
    
class CommodityType(Enum):
    notApplicable = 0
    electricity = 1
    air = 4
    naturalGas = 7
    propane = 8
    potableWater = 9
    steam = 10
    wastewater = 11
    heatingFluid = 12
    coolingFluid = 13
        
class ConsumptionTierType(Enum):
    notApplicable = 0
    blockTier1 = 1
    blockTier2 = 2
    blockTier3 = 3
    blockTier4 = 4
    blockTier5 = 5
    blockTier6 = 6
    blockTier7 = 7
    blockTier8 = 8
    blockTier9 = 9
    blockTier10 = 10
    blockTier11 = 11
    blockTier12 = 12
    blockTier13 = 13
    blockTier14 = 14
    blockTier15 = 15
    blockTier16 = 16
        
class CurrencyCode(Enum):
    na = 0
    aus = 36
    cad = 124
    usd = 840
    eur = 978

    @property
    def symbol(self):
        if self in [CurrencyCode.aus, CurrencyCode.cad, CurrencyCode.usd]:
            return '$'
        elif self is CurrencyCode.eur:
            return '€'
        else:
            return '¤'
        
class DataQualifierType(Enum):
    notApplicable = 0
    average = 2
    maximum = 8
    minimum = 9
    normal = 12
        
class FlowDirectionType(Enum):
    notApplicable = 0
    forward = 1
    reverse = 19
        
class KindType(Enum):
    notApplicable = 0
    currency = 3
    current = 4
    currentAngle = 5
    date = 7
    demand = 8
    energy = 12
    frequency = 15
    power = 37
    powerFactor = 38
    quantityPower = 40
    voltage = 54
    voltageAngle = 55
    distortionPowerFactor = 64
    volumetricFlow = 155
        
class PhaseCode(Enum):
    notApplicable = 0
    c = 32
    ca = 40
    b = 64
    bc = 66
    a = 128
    an = 129
    ab = 132
    abc = 224
    s2 = 256
    s2n = 257
    s1 = 512
    s1n = 513
    s1s2 = 768
    s1s2n = 769
        
class QualityOfReading(Enum):
    valid = 0
    manuallyEdited = 7
    estimatedUsingReferenceDay = 8
    estimatedUsingLinearInterpolation = 9
    questionable = 10
    derived = 11
    projected = 12
    mixed = 13
    raw = 14
    normalizedForWeather = 15
    other = 16
    validated = 17
    verified = 18
        
class ServiceKind(Enum):
    electricity = 0
    naturalGas = 1
    water = 2
    pressure = 4
    heat = 5
    cold = 6
    communication = 7
    time = 8

class TimeAttributeType(Enum):
    notApplicable = 0
    tenMinutes = 1
    fifteenMinutes = 2
    twentyFourHours = 4
    thirtyMinutes = 5
    sixtyMinutes = 7
    daily = 11
    monthly = 13
    present = 15
    previous = 16
    weekly = 24
    forTheSpecifiedPeriod = 32
    daily30MinuteFixedBlock = 79

class UomType(Enum):
    notApplicable = 0
    amps = 5
    volts = 29
    joules = 31
    hertz = 33
    watts = 38
    cubicMeters = 42
    voltAmps = 61
    voltAmpsReactive = 63
    cosine = 65
    voltsSquared = 67
    ampsSquared = 69
    voltAmpHours = 71
    wattHours = 72
    voltAmpReactiveHours = 73
    ampHours = 106
    cubicFeet = 119
    cubicFeetPerHour = 122
    cubicMetersPerHour = 125
    usGallons = 128
    usGallonsPerHour = 129
    imperialGallons = 130
    imperialGallonsPerHour = 131
    britishThermalUnits = 132
    britishThermalUnitsPerHour = 133
    liters = 134
    litersPerHour = 137
    gaugePascals = 140
    absolutePascals = 155
    therms = 169

UOM_SYMBOLS = {
    UomType.notApplicable: '',
    UomType.amps: 'A',
    UomType.volts: 'V',
    UomType.joules: 'J',
    UomType.hertz: 'Hz',
    UomType.watts: 'W',
    UomType.cubicMeters: 'm³',
    UomType.voltAmps: 'VA',
    UomType.voltAmpsReactive: 'VAr',
    UomType.cosine: 'cos',
    UomType.voltsSquared: 'V²',
    UomType.ampsSquared: 'A²',
    UomType.voltAmpHours: 'VAh',
    UomType.wattHours: 'Wh',
    UomType.voltAmpReactiveHours: 'VArh',
    UomType.ampHours: 'Ah',
    UomType.cubicFeet: 'ft³',
    UomType.cubicFeetPerHour: 'ft³/h',
    UomType.cubicMetersPerHour: 'm³/h',
    UomType.usGallons: 'US gal',
    UomType.usGallonsPerHour: 'US gal/h',
    UomType.imperialGallons: 'IMP gal',
    UomType.imperialGallonsPerHour: 'IMP gal/h',
    UomType.britishThermalUnits: 'BTU',
    UomType.britishThermalUnitsPerHour: 'BTU/h',
    UomType.liters: 'L',
    UomType.litersPerHour: 'L/h',
    UomType.gaugePascals: 'Pag',
    UomType.absolutePascals: 'Pa',
    UomType.therms: 'thm',
}
