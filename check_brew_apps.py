from pathlib import Path
from os import environ
import urllib.request
import platform
import json

def applications_folder() -> Path:
    print("[*]: Finding applications folder...")
    current_os: str = platform.system()
    if current_os == "Darwin":
        return Path("/Applications")
    elif current_os == "Linux":
        xdg_data_home: str | None = environ.get("XDG_DATA_HOME")
        if xdg_data_home:
            linux_path: Path = Path(xdg_data_home) / "applications"
        else:
            linux_path = Path.home() / ".local" / "share" / "applications"       
        return linux_path
    else:
        raise OSError(f"[X]: \033[31mUnsupported operating system: {current_os}\033[0m") 

def get_brew_list() -> list:
    print("[*]: Fetching Homebrew Cask database... (this may take a few seconds)")
    url = "https://formulae.brew.sh/api/cask.json"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return json.loads(s=response.read().decode())
    except Exception as e:
        raise RuntimeError(f"[X]: Failed to fetch Homebrew data: \033[31m{e}\033[0m")

def main() -> None:
    print("(check_brew_apps): Initialised")
    directory_path: Path = applications_folder()
    local_apps: dict[str, str] = {}
    for app in directory_path.glob(pattern="*.app"):
        local_apps[app.stem.lower()] = app.stem
        
    brew_database: list[dict] = get_brew_list()
    brew_lookup: dict[str, str] = {}

    for cask in brew_database:
        token = cask.get("token", "")
        if not token:
            continue
            
        token_lower = token.lower()
        
        if "artifacts" in cask:
            for artifact in cask["artifacts"]:
                if isinstance(artifact, dict) and "app" in artifact:
                    app_data = artifact["app"]
                    items_to_process = app_data if isinstance(app_data, list) else [app_data]
                    
                    for item in items_to_process:
                        target_str = ""
                        if isinstance(item, dict):
                            target_str = item.get("target") or list(item.values())[0]
                        elif isinstance(item, str):
                            target_str: str = item
                            
                        if isinstance(target_str, str):
                            app_name_lower: str = Path(target_str).stem.lower()
                            if app_name_lower == token_lower:
                                brew_lookup[app_name_lower] = token
    
    print("[+] --- Match Results ---")
    for local_lower, local_display in sorted(local_apps.items()):
        if local_lower in brew_lookup:
            print(f" -> '{local_display}' can be managed via: brew install --cask --force {brew_lookup[local_lower]}")
    
    print("[!]: Always double-check brew casks if they actually match the original app (script may get confused with generic names)\n[!]: Some results may not appear if they are only available as a different release (e.g osu@tachyon)")

if __name__ == "__main__":
    main()
