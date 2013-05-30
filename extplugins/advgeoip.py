# -*- coding: utf-8 -*-

# Advanced GeoIP plugin for BigBrotherBot(B3)
# Copyright (c) 2013 Harry Gabriel <rootdesign@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import b3
import b3.events
from b3.plugin import Plugin
from ConfigParser import NoOptionError

try:
    import pygeoip
except ImportError:
    print "Failed to load pygeoip modules :("

__author__ = 'ozon'
__version__ = '0.1.0'


class AdvgeoipPlugin(Plugin):
    _adminPlugin = None
    _geoip_db = 'GeoIP.dat'
    _geoip = None
    _geo_db_type = None

    def onLoadConfig(self):
        self._load_settings()

    def onStartup(self):
        # try to load admin plugin
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            self.error('Could not find admin plugin')
            return False
        # init geoip
        if self._geo_db_type == 'country':
            self._geoip = pygeoip.GeoIP(self._geoip_db, pygeoip.MEMORY_CACHE)
        elif self._geo_db_type == 'city':
            self._geoip = pygeoip.GeoIP(self._geoip_db)
        else:
            self.error('GeoIP initialization failed. Check your configuration.')
            return False

        # register commands and events
        self._register_commands()
        self.registerEvent(b3.events.EVT_CLIENT_AUTH)

    def onEvent(self, event):
        if event.type == b3.events.EVT_CLIENT_AUTH:
            # if City database - set country and city as attribute
            if self._geo_db_type == 'city':
                record = self._geoip.record_by_addr(event.client.ip)

                setattr(event.client, 'country_code', record.get('country_code'))
                setattr(event.client, 'city', record.get('city'))
            else:
                setattr(event.client, 'country_code', self._geoip.country_code_by_addr(event.client.ip))
                setattr(event.client, 'city', None)

    def cmd_geoip(self, data, client, cmd=None):
        """\
        <player name> - Returns the country name of the specified player.
        """

        sclient = None
        # Find the given player
        if data:
            sclient = self._adminPlugin.findClientPrompt(data, client=client)
        else:
            client.message('No player name given. Try !help geoip')
        # If we found the given player, get the Country name by IP
        if sclient:
            msg = 'B3 could not determine the country name.'
            if len(sclient.ip) > 0:
                _country = self._geoip.country_name_by_addr(sclient.ip)
                if len(_country) > 0:
                    msg = '%s is connected from %s.' % (sclient.name, _country)
            else:
                msg = 'B3 could not find %s\'s IP.' % sclient.name
            # Tell the client the results
            client.message(msg)
        # If no data given or the given player not exists - return
        return

    # -------------------------------------------------------------------------
    # plugin related helper methods

    def _getCmd(self, cmd):
        cmd = 'cmd_%s' % cmd
        if hasattr(self, cmd):
            func = getattr(self, cmd)
            return func

        return None

    def _register_commands(self):
        if 'commands' in self.config.sections():
            for cmd in self.config.options('commands'):
                level = self.config.get('commands', cmd)
                sp = cmd.split('-')
                alias = None
                if len(sp) == 2:
                    cmd, alias = sp

                func = self._getCmd(cmd)
                if func:
                    self._adminPlugin.registerCommand(self, cmd, level, func, alias)

    def _load_settings(self):
        if self.config.has_section('settings'):
            try:
                self._geoip_db = self.config.getpath('settings', 'geoip_db')
            except NoOptionError:
                self.warning('conf "geoip_db" not found, using defaults.')

            try:
                _geo_db_type = self.config.getpath('settings', 'db_type')
                if _geo_db_type not in ('city', 'country'):
                    raise NoOptionError
                self._geo_db_type = _geo_db_type
            except NoOptionError:
                self.error('conf "db_type" not found or wrong value, use "city" or "country".')

if __name__ == '__main__':
    # create a fake console which emulates B3
    from b3.fake import fakeConsole, joe, superadmin, simon

    p = AdvgeoipPlugin(fakeConsole, 'conf/plugin_advgeoip.ini')
    # call onStartup() as the real B3 would do
    p.onStartup()
    # make superadmin connect to the fake game server on slot 0
    joe.ip = '8.8.4.4'
    superadmin.connects(cid=1)
    # make joe connect to the fake game server on slot 1
    joe.ip = '8.8.8.8'
    joe.connects(cid=1)
    # make joe connect to the fake game server on slot 2

    simon.connects(cid=2)
    # superadmin put joe in group user
    #superadmin.says('!putgroup joe user')
    #superadmin.says('!putgroup simon user')