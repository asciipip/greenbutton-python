The Energy Service Provider Interface Standard (ESPI) is published by the
[North American Energy Standard Board (NAESB)][NAESB] as standard REQ.21.
This is a copyrighted standard with a publication fee.  The information
here is derived from the OpenESPI project's Apache-licensed code and
direct inspection of ESPI files.

  [NAESB]: https://www.naesb.org

ESPI files are XML documents structured according to the [Atom Syndication
Format][Atom].  They use Atom to encapsulate their own custom XML entities
and express relationships between the entities.

  [Atom]: https://tools.ietf.org/html/rfc4287

Basically, there are a number of entity types than can be thought of as
"top-level" types.  Each instance of one of these is present in an `entry`
entity in the Atom feed, with the ESPI's entity being contained within the
Atom entry's `content` entity.  The Atom entry's `link` entities are used
to relate the top-level entities to each other.  The only relation type
the author has seen is "related", which means that the meaning of the
relation must be inferred from the relative types of the related entities.
Some ESPI feeds appear to have `title` entities in their Atom entries.
These can be used as friendly names for the ESPI entities being
represented.

As an example, the `MeterReading` entity will be related to one
`ReadingType` entity and one or more `IntervalBlock` entities, indicating
that readings within the `IntervalBlock`s all share the parameters defined
in the `ReadingType` entity.

There are a number of other, secondary entity types, which fall into more
or less one of two categories.  One category basically serves as
enumerated types (enums).  These are generally integer values where each
integer has a specific, distinct meaning.  An example is the `ServiceKind`
type, where a value of "0" indicates electricity service, "1" indicates
natural gas service, and so on.  The other category includes types that
serve to encapsulate groups of values, like the `DateTimeInterval` type,
which represents a period of time by giving its start time and duration.

Pretty much every child of every element is optional, so one ESPI feed
might look very different from another one.

The `*.uml` files in this directory give [PlantUML][] diagrams of some of
the relationships between the various types.

  [PlantUML]: http://plantuml.com/

Top-Level Types
===============

UsagePoint
----------

Represents a place where utility usage is measured.  In many cases, this
will be an electric or gas meter.

### Links

One or more `MeterReading` entries.

### Children

 * `roleFlags` (two-byte hex string)
 * `ServiceCategory` (encapsulation type `ServiceCategory`) - Indicates
 what type of utility is being measured by this `UsagePoint`.
 * `status` (unsigned byte)

MeterReading
------------

Represents a collection of measurements (readings) of usage for the
associated `UsagePoint` entry.  All of the readings share the same units
and other parameters, as defined by the associated `ReadingType` entry.

### Links

Exactly one `ReadingType` entry.

One or more `IntervalBlock` entries.

### Children

None.  This entry serves only to link `IntervalBlock` entries to
`ReadingType` entries.

ReadingType
-----------

Gives measurement units and other information common to a set of readings
connected to a `MeterReading` entry.

### Links

None.

### Children

 * `accumulationBehaviour` (enum `AccumulationBehaviourType`)
 * `commodity` (enum `CommodityType`)
 * `consumptionTier` (enum `ConsumptionTierType`)
 * `currency` (enum `CurrencyCode`) - The currency in which readings'
   costs are denominated.
 * `dataQualifier` (enum `DataQualifierType`)
 * `defaultQuality` (enum `QualityOfReading`)
 * `flowDirection` (enum `FlowDirectionType`)
 * `intervalLength` (unsigned 32-bit integer) - Default interval length
   for associated readings that do not specify their own interval.
 * `kind` (enum `KindType`)
 * `phase` (enum `PhaseCode`)
 * `powerOfTenMultiplier` (signed byte) - The power of ten by which
   associated readings should be multipled.  e.g. if
   `powerOfTenMultiplier` is "-3", a reading with a value of "25" should
   be interpreted as representing the actual reading "0.025".
 * `timeAttribute` (enum `TimeAttributeType`)
 * `tou` (enum `TOUType`)
 * `uom` (enum `UomType`) - The units of measurement for the set of
   associated readings.  e.g. a value of "72" indicates that the
   measurements are in Watt-hours.

IntervalBlock
-------------

Contains a series of `IntervalReading` encapsulation entities, each of
which gives a single usage reading for the associated `UsagePoint`.  An
associated `ReadingType` entry (connected via this entry's parent
`MeterReading` entry) gives the units and other parameters necessary to
interpret the readings.

### Links

None.

### Children

 * `interval` (encapsulation type `DateTimeInterval`) - Gives the total
   interval of time covered by this block.  It is assumed(?) that the
   individual readings are contiguous within this time interval.
 * `IntervalReading` (encapsulation type `IntervalReading`, may have an
   unlimited number of these entities) - The actual readings.


Encapsulation Types
===================

DateTimeInterval
----------------

Represents a discrete interval of time, specified by a start time and a
duration.

### Children

 * `duration` (unsigned 32-bit integer) - The length of the interval in
   seconds.
 * `start` (signed 64-bit integer) - The time the interval started,
   represented as Unix epoch seconds (the number of seconds since the
   start of January 1st, 1970, UTC).

IntervalReading
---------------

Represents a single reading from the associated `UsagePoint`, subject to
the parameters in the associated `ReadingType`.  The reading can be
interpreted as saying, "Over the time given by `timePeriod`, a quantity of
`value` units of the relevant utility were used."

`timePeriod` is optional.  If it's not present, each reading is assumed to
cover a duration given by the associated `ReadingType` entry's
`intervalLength` child, with the first reading starting at the beginning
of the enclosing `IntervalBlock` and each subsequent reading starting
immediately after the previous one ends.

`value` and `cost` are optional, but any useful reading should have at
least one or the other.

`value` must be interpreted in the light of the `powerOfTenMultiplier` and
`uom` children of the associated `ReadingType` entity.  `uom` simply gives
the units for the measurement.  `powerOfTenMultiplier` gives a scale
factor for the reading.  If `powerOfTenMultiplier` is "6", then every
`value` should be multiplied by 10^6 to get the actual reading.  Note that
`powerOfTenMultiplier` can be negative.

### Children

 * `cost` (unsigned 48-bit integer) - The total cost of the resource
   measured in this reading, in 1/100,000 of the currency given in the
   associated `ReadingType`.  e.g. if the currency were US dollars, a
   `cost` of "8192" would represent an actual cost of $0.08192.
 * `ReadingQuality` (encapsulation type `ReadingQuality`, may have an
   unlimited number of these entities) - An indication of how good or
   accurate this reading should be considered to be.  May occur more than
   once, probably for entities that represent more than one real-world
   reading.
 * `timePeriod` (encapsulation type `DateTimeInterval`) - The time period
   over which the `value` of this reading was consumed.  See note above
   about cases when this isn't present.
 * `value` (unsigned 48-bit integer) - The actual value of the reading.
   See note above for how to interpret this value.

ServiceCategory
---------------

This is kind of a weird type that simply encapsulates a single value, the
kind of service being measured.

### Children

 * `kind` (enum `ServiceKind`, required) - the kind of service being
   measured, e.g. "0" for electricity, "1" for natural gas, etc.


Enum Types
==========

CurrencyCode
------------

An ISO 4217 currency code.

### Known Values

 * 0 - Not Applicable
 * 36 - Australian Dollar
 * 124 - Canadian Dollar
 * 840 - US Dollar
 * 978 - Euro

ServiceKind
-----------

The general kind of service being measured.

### Known Values

 * 0 - electricity
 * 1 - gas
 * 2 - water
 * 4 - pressure
 * 5 - heat
 * 6 - cold
 * 7 - communication
 * 8 - time

UomType
-------

The units in which a service is measured.

### Known Values

 * 0 - Not Applicable
 * 5 - A (Amps, Current)
 * 29 - V (Volts, Voltage)
 * 31 - J (Joules, Energy)
 * 33 - Hz (Frequency)
 * 38 - W (Watts, Real Power)
 * 42 - m³ (Cubic Meters, Volume)
 * 61 - VA (Volt-Amps, Apparent Power)
 * 63 - VAr (Volt-Amps Reactive, Reactive Power)
 * 65 - Cos (Cosine, Power Factor)
 * 67 - V² (Volts Squared)
 * 69 - A² (Amps Squared)
 * 71 - VAh (Volt-Amp Hours, Apparent Energy)
 * 72 - Wh (Watt-Hours, Real Energy)
 * 73 - VArh (Volt-Amp Reactive Hours, Reactive Energy)
 * 106 - Ah (Amp-Hours, Available Charge)
 * 119 - ft³ (Cubic Feet, Volume)
 * 122 - ft³/h (Cubic Feet per Hour, Flow)
 * 125 - m³/h (Cubic Meters per Hour, Flow)
 * 128 - US gal (US Gallons, Volume)
 * 129 - US gal/h (US Gallons per Hour, Flow)
 * 130 - IMP gal (Imperial Gallons, Volume)
 * 131 - IMP gal/h (Imperial Gallons per Hour, Flow)
 * 132 - BTU (British Thermal Units, Energy)
 * 133 - BTU/h (British Thermal Units per Hour, Power)
 * 134 - L (Liters, Volume)
 * 137 - L/h (Liters per Hour, Flow)
 * 140 - Pag (Pascals (Gauge), Pressure)
 * 155 - Pa (Pascals (Absolute), Pressure)
 * 169 - thm (Therms, Energy)
