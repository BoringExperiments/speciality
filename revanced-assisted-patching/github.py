import functools
import requests

try:
    import gnupg
except ImportError:
    print(
        "⚠️ Unable to import gnupg, please install it using 'pip install python-gnupg'"
    )
    gpg = False

try:
    gpg = gnupg.GPG()
except RuntimeError as e:
    print("⚠️ Unable to initialise GPG, this might be a problem with our dependency!")
    print(e.with_traceback(e.__traceback__))
    gpg = False


@functools.lru_cache(maxsize=10, typed=True)
def _info(
    authorisation: str = "",
    organisation: tuple = ("ReVanced", "ReVanced", "ReVanced"),
    repository: tuple = ("revanced-cli", "revanced-patches", "revanced-integrations"),
) -> dict:
    """Return the latest version of the ReVanced CLI, Patches, and Integrations"""

    auth = ""
    if authorisation:
        auth = {"Authorization": f"token {authorisation}"}

    get_cli = requests.get(
        f"https://api.github.com/repos/{organisation[0]}/{repository[0]}/releases/latest",
        headers=auth,
    ).json()
    get_patches = requests.get(
        f"https://api.github.com/repos/{organisation[1]}/{repository[1]}/releases/latest",
        headers=auth,
    ).json()
    get_integrations = requests.get(
        f"https://api.github.com/repos/{organisation[2]}/{repository[2]}/releases/latest",
        headers=auth,
    ).json()

    print("⚠️ This has been pinged, try not to request this multiple times!")

    return {"cli": get_cli, "patches": get_patches, "integrations": get_integrations}


def download_tools(data: dict, tool: str = "cli", verify: bool = True, gpg: gnupg = gnupg.GPG) -> None:
    valid_tools = ["cli", "patches", "integrations"]
    if tool.lower() not in valid_tools:
        raise ValueError(f"💥 Invalid tool specified. Expected one of {valid_tools}.")

    try:
        print(f"🔨 Downloading {tool} tools...")
        print(f"🔗 Downloading {data[tool]['name']} {data[tool]['tag_name']}")
    except Exception as e:
        print("💥 It's likely that you have hit ratelimit!")
        print(f"📝 {data[tool]}")
        print(e.with_traceback(e.__traceback__))

    for items in data[tool]["assets"]:
        if items["content_type"] in (
            "application/vnd.android.package-archive",
            "application/java-archive",
            "application/pgp-keys",
        ):
            asset_url = items["browser_download_url"]
            try:
                response = requests.get(asset_url)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"💥 Error downloading {items['name']}: {e}")
                continue

            file_path = f"tools/{items['name']}"
            try:
                with open(file_path, "wb") as f:
                    f.write(response.content)
            except IOError as e:
                print(f"💥 Error writing to file {file_path}: {e}")
                continue

            if gpg and items["name"].endswith(".asc") and verify:
                sig_file = items["name"].replace(".asc", "")
                asc_verify(f"tools/{sig_file}", gpg)
            else:
                print(f"⚠️ GPG Verification is skipped for {items["name"].replace(".asc", "")}, exercise caution!")


def asc_verify(file_path: str, gpg: gnupg) -> bool:
    #print(file_path)
    with open(file_path, "rb") as stream:
        verified = bool(gpg.verify_file(stream))
        print(
            "   💥 Unable to verify the signature!"
            if not verified
            else "✅ Signature verified!"
        )
    return verified


if __name__ == "__main__":
    print("Running directly will be skipped!")
