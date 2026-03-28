here[app]
# (str) Title of your application
title = Sanatani Bandhan

# (str) Package name
package.name = shda

# (str) Package domain (needed for unique APK identification)
package.domain = org.sanatanibandhan

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (file extensions)
source.include_exts = py,png,jpg,kv,atlas,ttf,md

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
# SQLite3, reportlab for PDF, requests for Firebase sync.
requirements = python3,kivy==2.2.1,sqlite3,requests==2.31.0,reportlab==4.0.4,urllib3,certifi,charset-normalizer,idna

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# --- Assets Integration (UPDATED) ---

# (str) Icon of the application (Square 512x512 recommended)
# Ensure you save your downloaded logo as 'assets/icon.png'
icon.filename = %(source.dir)s/assets/icon.png

# (str) Presplash of the application (Loading Screen)
# Ensure you save your downloaded logo as 'assets/presplash.png'
presplash.filename = %(source.dir)s/assets/presplash.png

# --- Android Specific Configuration ---

# (list) Permissions (REQUIRED for Internet Sync and PDF creation)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
# Android 13 (Tiramisu) is API 33.
android.api = 33

# (int) Minimum API your APP will support.
android.minapi = 21

# (bool) Use --private data storage (True) or --public (False)
android.private_storage = True

# (bool) If True, automatically accept SDK license agreements.
android.accept_sdk_license = True

# (str) The Android arch to build for.
android.archs = arm64-v8a, armeabi-v7a

# --- Buildozer Specific ---
[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
