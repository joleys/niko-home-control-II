# Upgrade from 2.x to 3.0

**Version 3.0 is a major release and is not backwards compatible with 2.x. You will need to check your existing
automations, scenes, helpers, ... so do not just upgrade!**

In v3.0 support for a lot of devices is added that were not supported before. But for the existing supported devices a
lot of new entities are exposed.

If you are only using lights and switches (sockets) you will probably not have to change anything. But it could be that
entities have changed names.

Please check your dashboards, automations, scenes, helpers, ... and make sure they are using the correct entities.

## Socket Energy Measurement

In the Niko API the socket and the power measurement are two separate devices. In version v3.0 this is reflected.

The entities that are representing the power measurement will not be available anymore, but they will be present under a
Naso (Smartplug) device.

