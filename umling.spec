# -*- mode: python -*-

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
             ( 'umling\\static\\*.js', 'static' ), ( 'umling\\static\\*.css', 'static' ), ( 'umling\\static\\*.html', 'static' ), ( 'umling\\static\\*.ico', 'static' ),
             ( 'umling\\static\\cdn\\*.js', 'static\\cdn' ), ( 'umling\\static\\cdn\\*.css', 'static\\cdn' ),
             ( GRAPHVIZ_PATH, 'graphviz' ),
             ],
             hookspath=['.'],
             excludes=[ 'telegram' ],
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
