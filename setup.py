"""
Setup script for building WhisperOSX as a macOS .app bundle
"""
from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'packages': ['tkinter', 'faster_whisper', 'ctranslate2', 'tokenizers', 'huggingface_hub'],
    'includes': ['PIL', 'av'],
    'excludes': ['matplotlib', 'scipy', 'pandas'],
    'iconfile': None,  # You can add an .icns file here later
    'plist': {
        'CFBundleName': 'WhisperOSX',
        'CFBundleDisplayName': 'WhisperOSX',
        'CFBundleGetInfoString': 'Audio/Video Transcription Tool',
        'CFBundleIdentifier': 'com.whisperosx.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'MIT License',
        'NSHighResolutionCapable': True,
    }
}

setup(
    name='WhisperOSX',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
