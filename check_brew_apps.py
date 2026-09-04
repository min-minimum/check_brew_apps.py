#!/usr/bin/env python3
import os
import json
import urllib.request
import platform
import re
import subprocess

def get_installed_casks():
    try:
        result = subprocess.run(
            ['brew', 'list', '--cask'], 
            capture_output=True, 
            text=True, 
            check=True
        )
        casks = set(line.strip() for line in result.stdout.strip().split('\n') if line.strip())
        return casks
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Note: Could not check installed casks (is Homebrew in your PATH?). Assuming none.")
        return set()

def fetch_brew_casks():
    url = "https://formulae.brew.sh/api/cask.json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        cask_mapping = {}
        for cask in data:
            token = cask.get('token')
            names = cask.get('name', [])
            
            cask_mapping[token.lower()] = token
            for name in names:
                cask_mapping[name.lower()] = token
                norm_name = re.sub(r'[\s\-]', '', name.lower())
                cask_mapping[norm_name] = token
                
        return cask_mapping
    except Exception as e:
        print(f"Error fetching cask data: {e}")
        return {}

def scan_macos_apps():
    """Scans standard macOS application directories."""
    apps = []
    paths = ['/Applications', os.path.expanduser('~/Applications')]
    for path in paths:
        if os.path.exists(path):
            for item in os.listdir(path):
                if item.endswith('.app'):
                    app_name = item[:-4]
                    apps.append(app_name)
    return apps

def scan_linux_apps():
    apps = []
    xdg_data_home = os.environ.get('XDG_DATA_HOME', os.path.expanduser('~/.local/share'))
    
    paths = [
        '/usr/share/applications',
        '/usr/local/share/applications',
        os.path.join(xdg_data_home, 'applications')
    ]
    
    for path in paths:
        if os.path.exists(path):
            for item in os.listdir(path):
                if item.endswith('.desktop'):
                    file_path = os.path.join(path, item)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            for line in f:
                                if line.startswith('Name='):
                                    apps.append(line.strip().split('=', 1)[1])
                                    break
                    except Exception:
                        apps.append(item[:-8])
    return apps

def find_cask_matches(installed_apps, cask_mapping, already_installed_casks):
    matches = {}
    for app in installed_apps:
        app_lower = app.lower()
        variations = [
            app_lower,                                  
            re.sub(r'[\s\-]', '', app_lower),           
            app_lower.replace(' ', '-'),                
        ]
        
        no_version = re.sub(r'\s+\d+$', '', app_lower)
        if no_version != app_lower:
            variations.extend([
                no_version,
                re.sub(r'[\s\-]', '', no_version),
                no_version.replace(' ', '-')
            ])

        for var in variations:
            if var in cask_mapping:
                matched_cask = cask_mapping[var]
                if matched_cask not in already_installed_casks:
                    matches[app] = matched_cask
                break
                
    return matches

def main():
    system = platform.system()
    if system not in ('Darwin', 'Linux'):
        print(f"Unsupported OS: {system}. This script supports macOS and Linux.")
        return

    print("Checking for already installed Homebrew casks...")
    installed_casks = get_installed_casks()
    if installed_casks:
        print(f"Found {len(installed_casks)} casks already managed by Homebrew.")

    print("Fetching the latest Homebrew cask list... (this may take a few seconds)")
    casks = fetch_brew_casks()
    if not casks:
        print("Failed to fetch cask data. Exiting.")
        return

    print(f"Scanning installed applications on {system}...")
    if system == 'Darwin':
        installed_apps = scan_macos_apps()
    else:
        installed_apps = scan_linux_apps()

    installed_apps = list(set(installed_apps))

    print("Matching applications to Homebrew casks...")
    matches = find_cask_matches(installed_apps, casks, installed_casks)

    if matches:
        print(f"\nFound {len(matches)} apps that can be replaced with Homebrew Casks:")
        print("-" * 65)
        for app, cask in sorted(matches.items()):
            print(f"{app.ljust(35)} -> brew install --cask {cask}")
        print("-" * 65)
    else:
        print("\nAll of your installed apps are either already managed by Homebrew, or no matching casks were found.")

if __name__ == "__main__":
    main()
