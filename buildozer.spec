[app]
title = Snakeibo Oyunu
package.name = com.snakeibo.oyun
package.domain = com.snakeibo
source.dir = .
source.exclude_dirs = bin, build, __pycache__
version = 1.0
app.mainclass = snakeibo
requirements = python3,kivy,kivmob,hostpython3,setuptools
orientation = landscape

android.api = 33
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a
android.minapi = 21

android.sdk_build_tools = 33.0.2

android.gradle_dependencies = com.google.android.gms:play-services-ads:23.0.0
android.release = 1
android.build_tool = aab

[buildozer]
log_level = 2

