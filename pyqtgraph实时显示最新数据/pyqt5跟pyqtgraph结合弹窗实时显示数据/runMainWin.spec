# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(5000)

block_cipher = None

# 路径最后的空格，一定要添加，否则会报错找不到相关文件
SETUP_DIR = 'D:\\Python_project\\Common Python modules\\pyqtgraph实时显示最新数据\\pyqt5跟pyqtgraph结合弹窗实时显示数据\\'


a = Analysis(['runMainWin.py',
               'test.py', ],
             pathex=['D:\\Python_project\\Common Python modules\\pyqtgraph实时显示最新数据\\pyqt5跟pyqtgraph结合弹窗实时显示数据\\'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='RF_Automate',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='RF_Automate')
