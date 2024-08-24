# import PyAPKDownloader

from PyAPKDownloader.aptoide import Aptoide
from PyAPKDownloader.apkpure import ApkPure


def yoink(type=1):
    if type == 1:
        Downloader = ApkPure()
        Downloader.download_by_package_name(
            package_name="com.google.android.apps.youtube.music",
            file_name="YouTube_Music",
            version="latest",
            app_ext="xapk",
            in_background=False,
            #limit=30,
        )
    elif type == 2:
        Downloader = Aptoide()
        Downloader.download_by_package_name(
            package_name="com.google.android.apps.youtube.music",
            file_name="YouTube_Music",
            version="latest",
            in_background=False,
            limit=10,
        )


yoink()
