#!/usr/bin/env python
#
#
# VP21 RC
#
#
# Copyright 2016 Al Brown
#
# Epson Project Remote Control
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

a = Analysis(['vp21rc.py'])
a.datas += Tree('gui/ui', prefix='ui')

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts + [('O', '', 'OPTION')],
          a.binaries,
          a.zipfiles,
          a.datas,
          name='vp21rc',
          upx=True)