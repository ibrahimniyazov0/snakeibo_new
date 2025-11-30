[app]
title = Snakeibo
package.name = snakeibo
package.domain = org.snakeibo
version = 1.0

# Main file
source.dir = .
source.include_exts = py,png,jpg,kv,json,txt,atlas,so,a,dylib,wav

# Requirements
requirements = python3,kivy,pillow,kivmob

orientation = portrait
export_orientation = portrait
fullscreen = 0

# Permissions
android.permissions = INTERNET

# BUILD SETTINGS
android.api = 34
android.minapi = 21
android.sdk = 34

# >>> MOST IMPORTANT <<<
# FIX AIDL ERROR
android.build_tools_version = 30.0.3

# Stable NDK (25c problem yaradır)
android.ndk = 21b
android.ndk_api = 21

# Architecture
android.archs = arm64-v8a,armeabi-v7a

# AAB building
android.release = aab

# Disable unstable branches
# p4a.branch = develop
# p4a.kivy_fork = https://github.com/kivy/kivy
