import glob
import os
import re
import subprocess
import sys
from tabulate import tabulate

print(sys.version_info)

experimental_rvp = False


def get_tools_list(tools_folder: str = "tools") -> dict:
    """
    Get a list of tools and their versions from the specified folder.

    Args:
        tools_folder (str): The folder where tools are stored.

    Returns:
        tools (dict): A dictionary with tool types as keys and lists of tuples (filename, version) as values.
    """
    tools = {"cli": [], "patches": [], "integrations": []}

    version_pattern = re.compile(r"(\d+\.\d+\.\d+(?:\+[a-zA-Z0-9\-]+)?)")

    for tool_type in tools.keys():
            if tool_type == "integrations":
                patterns = [os.path.join(tools_folder, f"revanced-{tool_type}-*.apk")]
            else:
                patterns = [os.path.join(tools_folder, f"revanced-{tool_type}-*.jar"),
                            os.path.join(tools_folder, f"revanced-{tool_type}-*.rvp")]

            files = []
            for pattern in patterns:
                files.extend(glob.glob(pattern))

            for file in files:
                match = version_pattern.search(file)
                if match:
                    tools[tool_type].append((file, match.group(1)))

    return tools


def print_tools_list(tools: dict):
    """
    Print the list of tools and their versions.
    """
    tool_data = []
    for tool_type, tool_list in tools.items():
        if not tool_list:
            print(f"\n💥 ReVanced {tool_type.capitalize()} Tools:")
            print("  💥 None")
        else:
            print(f"\n✨ ReVanced {tool_type.capitalize()} Tools:")
            for file, version in tool_list:
                tool_data.append([tool_type.capitalize(), file, version])
                print(f"  👷 {file} (Version: {version})")

    headers = ["✨ Tool Type", "📁 File", "⏳ Version"]
    print("\n")
    print(tabulate(tool_data, headers=headers, tablefmt="github"))


def get_latest_version(tools: dict, tool_type: str) -> str:
    """
    Get the latest version of a tool from the list.

    Args:
        tools (dict): A dictionary with tool types as keys and lists of tuples (filename, version) as values.
        tool_type (str): The type of tool to get the latest version for.

    Returns:
        version (str): The latest version of the tool.
    """
    if tool_type not in tools or not tools[tool_type]:
        return None

    # Sort versions
    tools[tool_type].sort(key=lambda x: tuple(map(any, x[1].split("."))), reverse=True)
    latest_file, latest_version = tools[tool_type][0]
    return latest_version


def run_instance(
    cli_version,
    patches_version,
    integrations_version,
    output_path,
    input_apk,
    cache_parallel,
    experimental_rvp=False,
):
    """
    Run a single instance of the revanced-cli command.
    """
    command = (
        f"java -jar tools/revanced-cli-{cli_version}.jar patch "
        f"--purge "
        f"--temporary-files-path {cache_parallel} --force "
        f"--patch-bundle tools/revanced-patches-{patches_version}.{"rvp" if experimental_rvp else "jar"} "
        f"--merge tools/revanced-integrations-{integrations_version}.apk "
        #f'--out "{output_path}" '
        f'"{input_apk}"'
    )
    print(f"🚀 Running command: {command}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            #capture_output=True,
            text=True,
            stderr=sys.stderr,
            stdout=sys.stdout,
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"🔥 An error occurred while processing {input_apk}: {e}")
        print(f"Command: {e.cmd}")
        print(f"Return code: {e.returncode}")
        print(f"Output: {e.output}")
        print(f"Error: {e.stderr}")
        return False


def run():
    tools = get_tools_list()

    print_tools_list(tools)

    # Check if all necessary tools are present
    missing_tools = []
    for tool_type in ["cli", "patches", "integrations"]:
        if not tools[tool_type]:
            missing_tools.append(tool_type.capitalize())
            print(f"🔥 Requirements for {tool_type} not met!")

    if missing_tools:
        print("🔥 Missing tools:")
        print(
            tabulate(
                [[tool] for tool in missing_tools],
                headers=["🔥 Missing Tool"],
                tablefmt="github",
            )
        )
        return

    # Get the latest versions
    cli_version = get_latest_version(tools, "cli")
    patches_version = get_latest_version(tools, "patches")
    integrations_version = get_latest_version(tools, "integrations")

    # cli_version = "4.6.0+dsl-all"
    # patches_version = "4.10.0-dev.14+dsl"
    # integrations_version = "1.12.0-dev.9"

    if not all([cli_version, patches_version, integrations_version]):
        print("🔥 Could not determine the latest version for some tools!")
        return

    apk_files = glob.glob("apk/*.apk")

    if not apk_files:
        print("🔥 No APK files found in the 'apk' folder!")
        return

    patch_results = []
    patch_results_signature = []
    patch_results_tool = []

    for apk in apk_files:
        output_path = f"patched/{os.path.basename(apk)}"
        status = run_instance(
            cli_version,
            patches_version,
            integrations_version,
            output_path,
            apk,
            "revanced-cache",
            False
        )
        status_message = (
            "✅ Processed successfully" if status else "🔥 Unable to process"
        )

        apk_name_command = f"""aapt dump badging {apk} | findstr \"application-label:'\" | sed -e \"s/.*application-label:'//\" -e \"s/'.*//\""""
        version_name_command = f"""aapt dump badging {apk} | findstr \"versionName='\" | sed -e \"s/.*versionName='//\" -e \"s/'.*//\""""
        min_sdk_command = f"""aapt dump badging {apk} | findstr \"sdkVersion:'\" | sed -e \"s/.*sdkVersion:'//\" -e \"s/'.*//\""""
        target_sdk_command = f"""aapt dump badging {apk} | findstr \"targetSdkVersion:'\" | sed -e \"s/.*targetSdkVersion:'//\" -e \"s/'.*//\""""
        aapt_version_command = "aapt v"
        apksigner_version_command = "apksigner version"
        apksigner_signature_command = f"apksigner verify --print-certs {apk}"
        result_command = []
        for command in [
            apk_name_command,
            version_name_command,
            min_sdk_command,
            target_sdk_command,
            aapt_version_command,
            apksigner_version_command,
            apksigner_signature_command,
        ]:
            print(f"🚀 Running command: {command}")
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    check=True,
                    text=True,
                    capture_output=True,
                )
                print(result.stdout)
                result_command.append(result.stdout.strip())
            except subprocess.CalledProcessError as e:
                print(f"🔥 An error occurred while processing {apk}: {e}")
                result_command.append("Unknown (Error)")

        print(
            f"🛠️ {apk} - {result_command[0]} - {result_command[1]} | {result_command[2]} - {result_command[3]} | {status_message}"
        )

        patch_results.append(
            [
                apk,
                result_command[0],
                result_command[1],
                f"{result_command[2]} - {result_command[3]}",
                status_message,
            ]
        )
        patch_results_signature.append(
            [
                apk,
                result_command[6],
            ]
        )
        patch_results_tool.append(
            [
                apk,
                cli_version,
                patches_version,
                integrations_version if not experimental_rvp else "N/A",
                result_command[4],
                result_command[5],
                "NotImplemented",
            ]
        )

    headers = [
        "📁 APK File",
        "🪪 APK Name",
        "⏳ APK Version",
        "🎯 SDK Range",
        "🚦 Patch Status",
    ]
    tool_headers = [
        "📁 APK File",
        "🧑‍💻 ReVanced CLI",
        "🧩 ReVanced Patches",
        "🔩 ReVanced Integrations",
        "💁 APK Parsing Tool",
        "💁 Apksigner Version",
        "🚦 Signature Status",
    ]
    signature_headers = [
        "📁 APK File",
        "🔑 Signature",
    ]
    print("\n")
    print(tabulate(patch_results, headers=headers, tablefmt="github"))
    print("\n")
    print(tabulate(patch_results_tool, headers=tool_headers, tablefmt="github"))
    print("\n")
    print(tabulate(patch_results_signature, headers=signature_headers, tablefmt="github"))


if __name__ == "__main__":

    run()
    # run()
