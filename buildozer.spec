[app]
version = 1.0
title = MAC Changer
package.name = macchanger
package.domain = org.macchanger
source.dir = .
requirements = python3,kivy==2.3.0
android.permissions = INTERNET, ACCESS_WIFI_STATE, CHANGE_WIFI_STATE
android.api = 30
android.minapi = 21
android.ndk = 23b

[buildozer]
log_level = 2

# ПРИНУДИТЕЛЬНО УКАЗЫВАЕМ ПУТЬ К SDK
# android.sdk_path = /home/runner/android-sdk
# android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r23b
# 3android.ant_path = /home/runner/.buildozer/android/platform/apache-ant-1.9.4
