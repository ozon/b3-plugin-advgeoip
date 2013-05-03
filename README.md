Advanced GeoIP plugin for [B3](http://www.bigbrotherbot.net/ "BigBrotherBot")
=============================================================================
This plugin extends B3, so that he can retrieve the country name of players.
It does the same as [krsanky's geoip](https://github.com/krsanky/b3-geoip) plugin.


## Usage

### Requirements
- [BigBrotherBot](http://bigbrotherbot.net/)
- [MaxMind's GeoLite Country db](http://dev.maxmind.com/geoip/legacy/geolite)
- [Pure Python GeoIP API](https://github.com/appliedsec/pygeoip/)

### Installation
1. Copy the file [extplugins/advgeoip.py](extplugins/advgeoip.py) into your `b3/extplugins` folder and
[extplugins/conf/plugin_advgeoip.ini](extplugins/conf/plugin_advgeoip.ini) into your `b3/conf` folder

2. This plugin requires the pygeoip module. That can be installed with the command `easy_install pygeoip`.
  If you are unsure or do not want to install pygeoip, also copy the folder [extplugins/pygeoip](extplugins/pygeoip) to your into your `b3/extplugins` directory.

3. Obtain the [GeoIP Lite Country Database](http://dev.maxmind.com/geoip/legacy/geolite) and extract the GeoIP.dat to a folder of your choice. Preferably you place the GeoIP.dat in your plugin directory.

4. Add the following line in your b3.xml file (below the other plugin lines)
```xml
<plugin name="advgeoip" config="@conf/plugin_advgeoip.ini"/>
```

### Settings
Setup the Path to the GeoIP.dat into the `plugin_advgeoip.ini` file.

## FAQ
**Q**: Why you do not fork [krsanky's geoip](https://github.com/krsanky/b3-geoip) plugin and created improved?
**A**: The code is trivial and my changes are the same as new write.

## Thanks
- [pygeoip](https://github.com/appliedsec/pygeoip/)