# -*- mode: python -*-

"""
This is a umling spec file.
"""

debug = False

block_cipher = None

a = Analysis(['umling\\__main__.py'],
             pathex=['C:\\Program Files (x86)\\Windows Kits\\10\\Redist\\ucrt\\DLLs\\x64', 'C:\\Users\\vanya\\AppData\\Roaming\\Python\\Python37\\site-packages', 'D:\\Projects\\Python\\_umling'],
             datas=[
             ( 'umling\\static\\*.js', 'static' ), ( 'umling\\static\\*.css', 'static' ), ( 'umling\\static\\*.html', 'static' ), ( 'umling\\static\\*.ico', 'static' ),
             ( 'umling\\static\\cdn\\*.js', 'static\\cdn' ), ( 'umling\\static\\cdn\\*.css', 'static\\cdn' ),
             ( 'C:\\Utils\\graphviz-2.38', 'graphviz' ),
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
