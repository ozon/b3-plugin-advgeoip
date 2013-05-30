Advanced GeoIP plugin for [B3](http://www.bigbrotherbot.net/ "BigBrotherBot")
=============================================================================
This plugin extends B3, so that he can retrieve the country name of players.
It does the same as [krsanky's geoip](https://github.com/krsanky/b3-geoip) plugin.

The Client Object gets a new properties that includes the country name, country code and the city.
This is useful if other plugins require the country code.

## Usage

### Requirements
- [BigBrotherBot](http://bigbrotherbot.net/)
- [MaxMind's GeoLite Country db](http://dev.maxmind.com/geoip/legacy/geolite)
- [Pure Python GeoIP API](https://github.com/appliedsec/pygeoip/)

### Installation
1. Copy the file [extplugins/advgeoip.py](extplugins/advgeoip.py) into your `b3/extplugins` folder and
[extplugins/conf/plugin_advgeoip.ini](extplugins/conf/plugin_advgeoip.ini) into your `b3/conf` folder

2. This plugin requires the pygeoip module. That can be installed with the command `easy_install pygeoip`.
  If you are unsure or do not want to install pygeoip, also copy the folder [extplugins/pygeoip](extplugins/pygeoip) to your into your `b3/` directory.
  If you are using for example the Windows Binary Releases of B3, copy the folder `pygeoip` to the B3 installation Directory.

3. Obtain the [GeoIP Lite Country Database](http://dev.maxmind.com/geoip/legacy/geolite) and extract the GeoIP.dat to a folder of your choice. Preferably you place the GeoIP.dat in your plugin directory.

4. Add the following line in your b3.xml file (below the other plugin lines)
```xml
<plugin name="advgeoip" config="@conf/plugin_advgeoip.ini"/>
```

### Settings
Setup the Path to the GeoIP.dat into the `plugin_advgeoip.ini` file.

### Commands
- `!geoip <playername>` Displays the country and the city (if city db used) of the specified player is connected

## Changelog
### v0.2
- allows the use of the city database
- rename client attributes

## Thanks
- [pygeoip](https://github.com/appliedsec/pygeoip/)

