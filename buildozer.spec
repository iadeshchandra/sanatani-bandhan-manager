[app]
title = Sanatani Bandhan
package.name = shda
package.domain = org.sanatanibandhan
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,md
version = 1.0.0
requirements = python3,kivy,sqlite3,requests,reportlab
orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/presplash.png
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.private_storage = True
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
