# -*- mode: python -*-

# Copyright (c) 2019 Ivan Semkin.
#
# This file is part of umling
#
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
"""
This is a umling spec file.
"""

debug = False

block_cipher = None

UCRT_PATH = 'C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\ucrt\\DLLs\\x64'
PYTHON_PATH = 'C:\\Users\\vanya\\AppData\\Roaming\\Python\\Python37\\site-packages'
GRAPHVIZ_PATH = 'C:\\Utils\\graphviz-2.38'

a = Analysis(['umling\\__main__.py'],
             pathex=[UCRT_PATH, PYTHON_PATH],
             datas=[
                 ('umling\\static\\*.js', 'static'), ('umling\\static\\*.css', 'static'),
                 ('umling\\static\\*.html', 'static'), ('umling\\static\\*.ico', 'static'),
                 ('umling\\static\\cdn\\*.js', 'static\\cdn'), ('umling\\static\\cdn\\*.css', 'static\\cdn'),
                 (GRAPHVIZ_PATH, 'graphviz'),
             ],
             hookspath=['.'],
             excludes=['telegram'],
             win_no_prefer_redirects=True,
             win_private_assemblies=True,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='umling',
          debug=debug,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=debug,
          icon='umling/static/favicon.ico',
          version='version.txt')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='umling')
