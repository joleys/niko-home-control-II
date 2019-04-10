# hass-nhc2

License: MIT

This is in pre-alpha state... things will explode :p

This 'custom_component' provides you with a NHC2 Platform

__Niko Home Control II / Connected controller__

__LIMITED__ to switches/lights as it stands now

## How to get it running

1. Add all the files inside a folder called `<CONFIG_FOLDER>/custom_components/nhc2/`
2. Add 'nhc2' to the static list `FLOWS` in `homeassistant/config_entries.py` (this in until HA can auto populate this for custom components)
3. Create credentials (see next paragraph)
4. Do the __Niko Connected Controller__ setup in `Setting > Integrations` the Web Ui  

see: [Home Assistant dev docs - Integration Configuration](https://developers.home-assistant.io/docs/en/config_entries_config_flow_handler.html) 
## The credentials

First you will need to add a touchscreen profile to the controller setup.
(see [Creating and modifying touchscreen profiles](http://guide.niko.eu/pages/viewpage.action?pageId=10978290))
The password you enter there, will be the password you will need for the connection.
The username is the ID this profile gets. There are 3 ways of extracting this information.

### Method 1 - Not Yet Available
 In a later version of the integration, I hope to make Method 3 automatic, so the user can select the profile from a dropdown in the Web UI

### Method 2 - Zip & SQLite
 1. The project file from the Niko software is a zip,
    extract it using your (un)zip tool of choice.
 2. Open the Config.sqlite with [DB Browser for SQLite](https://sqlitebrowser.org/dl/)
 3. Go to tab 'Browse Data' and open the table called __Profile__
 4. Look for the __CreationId__ that corresponds with the desired profile, that's the username 
 
### Method 3 - MQTT Client
 1. Connect to the MQTT broker on the Connected Controller, on port 8883, 
 using the CA cert you can find in this repo
 2. Subscribe to the topic `public/authentication/rsp`
 3. Publish on topic `public/authentication/cmd` with payload `{"Method":"profiles.list"}`
 4. Extract the __Uuid__ that corresponds with the desired profile

## What is supported

 * Baisc configuration trough the integration UI
 * NHC2 'light' as a HA Light (light connected to switch using a Basic Action)
 * NHC2 'switched-generic' as a ha Switch (virtual output connected to switch using a Basic Action)
 
## What can you do to help?

 * Contribute to this project with constructive issues, suggestions, PRs, etc.
 * Help me in any way to get support for more entities (eg dimmer)
