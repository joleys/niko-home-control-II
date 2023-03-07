# Upgrade from 2.x to 3.0

**v3.0 is a major release and is not backwards compatible with 2.x. You will need to check your existing
automations, scenes, helpers, ... so do not just upgrade! Make sure you have time to reconfigure.**

This is a major release and includes several new features, improvements, and changes. Please note that this version is
not backwards compatible with 2.x, so you will need to check your existing automations, scenes, helpers, and
configurations after upgrading.

## New Features:

* Support for extra devices, now almost all documented devices are supported. The new supported devices are:
    * Energy Home
    * Generic Heating/Cooling Implementation
    * Generic Ventilation Implementation
    * Generic Warm Water Implementation
    * NHC Access Control Action
    * NHC Audio Control Action
    * NHC Basic Alarm Action
    * NHC BellButton Action
    * NHC Condition Action
    * NHC Heating Cooling Action
    * NHC House Mode Action
    * NHC HVAC Thermostat
    * NHC Mood Action
    * NHC Panic Mode Action
    * NHC PIR Action
    * NHC Presence Simulation Action
    * NHC Relay Action (switched-fan)
    * NHC Reynaers Action
    * NHC Thermostat (thermostat)
    * NHC Thermostat (touchswitch)
    * NHC Timeschedule Action Active
    * NHC Velux Action
    * RobinsIP
* A lot more sensors/entities for different Niko devices.
* Multiple callbacks per device, allowing for more entities.
* A massive code rewrite.

For a complete list of all supported devices and entities, please refer to the README file available
at [https://github.com/joleys/niko-home-control-II/tree/rewrite#readme](https://github.com/joleys/niko-home-control-II/tree/rewrite#readme).

If you are only using lights and switches (sockets), you may not need to change anything. However, please check your
dashboards, automations, scenes, helpers, and configurations to ensure that they are using the correct entities. Please
note that some entities may have changed names. More details below.

We have done our best to test this release extensively. However, if you encounter any issues or problems, please let us
know by creating an issue on Github
at [https://github.com/joleys/niko-home-control-II/issues](https://github.com/joleys/niko-home-control-II/issues).
Please provide as many details as possible to help us troubleshoot and resolve the issue.

## Known changes

### NHC Virtual flag

In the past this was a binary sensor, this is now a switch. The entity id has changed.

### NHC Zigbee Smart plug

In the Niko API the socket and the power measurement are two separate devices. In version v3.0 this is reflected. The
entity is replaced by the new Electrical Power entity.

Note that your historical data will be lost.

### Generic Zigbee Smart plug

The switch will not be available anymore. You will see a separate device that you should use. This device is only used
to report the electrical power usage.

### Electricity Metering module (with clamp)

The old entity containing the Electrical Power will not be available anymore. This entity is replaced by 3 new entities:

* Electrical Power, which is the same as the old one, but it will have a new entity id.
* Electrical Power Consumption, which represents the positive value of the Electrical Power.
* Electrical Power Production, which represents the negative value of the Electrical Power.

Note that your historical data will be lost.
