# check_brew_apps.py
Simple python script that checks your applications folder for any apps that can be replaced with a Homebrew cask.

## Installation & Setup
Clone this repository:
```bash
git clone https://github.com/min-minimum/check_brew_apps.py.git check_brew_apps
```

Then run the script:
```bash
cd check_brew_apps
python3 check_brew_apps.py
```


## Notes
* Only supports MacOS and Linux

*  Always double-check outputted brew casks if they actually match the original app (script may get confused with generic names)

* Some results may appear only as a different release (e.g obs@beta is shown over obs)

* Scans only the system applications folder for MacOS

* Recommended to have Homebrew installed and requires Python


## Development
Basic type checking by [BasedPyright](https://docs.basedpyright.com/latest/)

No external dependencies used

MIT licensed
