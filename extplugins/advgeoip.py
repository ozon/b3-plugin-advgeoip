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
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__)))
    try:
        import pygeoip
    except ImportError:
        print "Failed to load pygeoip modules :("

__author__ = 'ozon'
__version__ = '0.2.1'


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
        self.registerEvent(b3.events.EVT_PUNKBUSTER_NEW_CONNECTION)

    def _add_geoattr(self, client):
        _data = dict(country_code='US', country='', city='')
        if len(client.ip) > 0:
            if self._geo_db_type == 'city':
                record = self._geoip.record_by_addr(client.ip)

                _data['country_code'] = record.get('country_code')
                _data['country'] = record.get('country_name')
                _data['city'] = record.get('city')
            else:
                _data['country_code'] = self._geoip.country_code_by_addr(client.ip)
                _data['country'] = self._geoip.country_code_by_addr(client.ip)

        [setattr(client, k, v) for k, v in _data.items()]
        return client

    def onEvent(self, event):
        if event.type == b3.events.EVT_CLIENT_AUTH:
            self._add_geoattr(event.client)
        elif event.type == b3.events.EVT_PUNKBUSTER_NEW_CONNECTION:
            self._add_geoattr(event.client)

    def cmd_geoip(self, data, client, cmd=None):
        """\
        <player name> - Returns the country name of the specified player.
        """

        sclient = None
        _old_or_now = 'is'
        # Find the given player
        if data:
            sclient = self._adminPlugin.findClientPrompt(data)

            # if bo client found on current session, look on DB
            if not sclient:
                _search = {'id': data[1:]} if data.startswith('#') else {'name': data}
                try:
                    result = self.console.storage.getClientsMatching(_search)[0]
                    _old_or_now = 'has'
                    sclient = self._add_geoattr(result)
                except IndexError:
                    client.message('No players found.')
        else:
            client.message('No player name given. Try !help geoip')
        # If we found the given player, get the Country name by IP
        if sclient:
            msg = 'B3 could not determine the country name.'
            if sclient.city:
                msg = '%s %s connected from %s, %s.' % (sclient.name, _old_or_now, sclient.city, sclient.country)
            elif sclient.country:
                msg = '%s %s connected from %s.' % (sclient.name, _old_or_now, sclient.country)
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
