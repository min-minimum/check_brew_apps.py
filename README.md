# check_brew_apps.py
Simple python script that checks your applications folder for any apps that can be replaced with a brew cask.

## Installation
Clone the repository and run:
```bash
git clone https://github.com/min-minimum/check_brew_apps.py.git check_brew_apps
cd check_brew_apps
python3 check_brew_apps.py
```

## Notes
* Does not support Windows

*  Always double-check outputted brew casks if they actually match the original app (script may get confused with generic names)

* Some results may not appear if they are only available as a different release (e.g osu@tachyon)

* Scans only the system applications folder on MacOS

* Recommended to have Homebrew installed and requires Python


## Development
Basic type checking by [BasedPyright](https://docs.basedpyright.com/latest/)

No external dependencies used

MIT licensed
