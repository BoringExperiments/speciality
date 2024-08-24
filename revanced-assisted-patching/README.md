# `> ReVanced_Assisted_Patcher`
This spaghetti tool is designed to automatically patch application using ReVanced

The rewrite is complete with 
* Cache for the GitHub API to ensures less ratelimiting experience;
* GPG check for automatically downloaded tools
* Built-in APK downloader using APKPure, Aptoide and APK-dl (Disabled, insanely slow and unreliable, APKMirror still better)
* Experimental RVP format compatibility (WIP, Togglable, but setup have to be made)
* Experimental parallel patching (WIP, Disabled)
* Better error handling

| Python version | Support status               |
| -------------- | ---------------------------- |
| 3.12           | :white_check_mark: Supported |
| 3.11           | :white_check_mark: Supported |
| 3.10           | :white_check_mark: Supported |
| 3.9            | :gear: Best effort           |
| =<3.8          | :x: Not Supported            |


## `> RVAP // Usage`
Supply the APK that you want to patch in `apk` folder, 
run `github.py` to automatically grab the latest stable release of 
CLI, Patches and Integrations

After that, run `main.py` to run the patch

> [!CAUTION]
> ReVanced CLI may have `all` suffix (*-all), RVAP is little cringey at detecting this, 
> so it's must be sanitised (remove `all` suffix from the name)

| Emoji | Meaning    |
| ----- | ---------- |
| 💥    | Error      |
| ⚠️    | Warning    |
| 🗿    | Processing |
| 🥞/✅ | Success    |

## `> RVAP // Contributing`
Interested in contributing? See the [contributing guide](docs/CONTRIBUTING.md)
