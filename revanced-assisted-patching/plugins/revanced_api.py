import requests


def get_available_patches():
    """Get the latest available patches from the ReVanced API v2

    Returns:
      Response: Output from the API as string
    """
    response = requests.get("https://api.revanced.app/v2/patches/latest")
    return str(response)
