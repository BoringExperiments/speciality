import glob
import github

try:
    #import plugins.yoink
    False
except ImportError:
    #yoink = False
    False


github._info()

github.download_tools

gpg = False

try:
    import gnupg
    print("🔑 GPG is available!")
    gpg = True
except ImportError:
    print(
        "⚠️ Unable to import gnupg, please install it using 'pip install python-gnupg'"
    )

try:
    gpg = gnupg.GPG()
    print("🔑 GPG is initialised!")
    gpg = True
except RuntimeError as e:
    print("⚠️ Unable to initialise GPG, this might be a problem with our dependency!")
    print(e.with_traceback(e.__traceback__))


def main():
    tools_to_check = [
        ("tools/revanced-cli-*.jar", "cli"),
        ("tools/revanced-patches-*.jar", "patches"),
        ("tools/revanced-integrations-*.apk", "integrations"),
    ]

    for pattern, tool in tools_to_check:
        if not glob.glob(pattern):
            github.download_tools(github._info(), tool, True, gpg)
    print(github._info.cache_info())


main()
