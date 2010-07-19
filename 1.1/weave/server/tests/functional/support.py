# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Sync Server
#
# The Initial Developer of the Original Code is the Mozilla Foundation.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Tarek Ziade (tarek@mozilla.com)
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****
""" Base test class, with an instanciated app.
"""
import os
import unittest
from ConfigParser import RawConfigParser

from webtest import TestApp
from weave.server.wsgiapp import make_app
from weave.server.storage import get_storage
import weave.server

_TOPDIR = _WEAVEDIR = os.path.dirname(weave.server.__file__)
for i in range(2):
    _TOPDIR = os.path.split(_TOPDIR)[0]

class TestWsgiApp(unittest.TestCase):

    def setUp(self):
        # loading tests.ini
        cfg = RawConfigParser()
        cfg.read(os.path.join(_TOPDIR, 'tests.ini'))
        config = dict(cfg.items('DEFAULT') + cfg.items('server:main'))
        storage_params = dict([(param.split('.')[-1], value)
                               for param, value in config.items()
                               if param.startswith('storage.')])
        self.storage = get_storage(config['storage'], **storage_params)
        self.sqlfile = storage_params['sqluri'].split('sqlite:///')[-1]
        self.app = TestApp(make_app(config))

    def tearDown(self):
        if os.path.exists(self.sqlfile):
            os.remove(self.sqlfile)
