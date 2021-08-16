## Install

```
git clone https://github.com/Skywire/magediff.git
cd magediff
pip install -r requirements.txt
```

## Usage

Use composer to install a vanilla copy of the version you are comparing against (previous version)

`composer create-project --repository-url=https://repo.magento.com/ magento/project-community-edition:<version> <directory>`

Run the tool from you Magento project directory with

```
python <path_to_tool>main.py <path to previous version>
```

You will then get a list of files in your app/design where the vendor files have changed between versions.

At this time only Magento core modules are checked.

### Diff and merge

There are 3 diff and merge options, you must have Beyond Compare Installed to use the diff and merge features, additional tools may be added in the future

#### Merge

`main.py -m <path to previous version>`

This will run a 3 way merge between the app/design files, the current version vendor file, and the compare version vendor file

#### Theme Diff

`main.py -dt <path to previous version>`

This will run a diff between the app/design and current version vendor files

#### Vendor Diff

`main.py -dv <path to previous version>`

This will run a diff between the current version and compare version vendor files