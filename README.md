## Install

```
git clone https://github.com/Skywire/magediff.git
cd magediff
pip install -r requirements.txt
```

## Usage

Use composer to install a vanilla copy of the version you are comparing against (previous version)

`composer create-project --repository-url=https://repo.magento.com/ magento/project-community-edition:<veresion> <directory>`

Run the tool with

`python main.py <path to current installation> <path to previous version>`

You will then get a list of files in your app/design where the vendor files have changed between versions.

At this time only Magento core modules are checked.
