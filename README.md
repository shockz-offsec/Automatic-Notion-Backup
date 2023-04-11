# Automatic-Notion-Backup
This script automates the backup process of Notion data into Markdown and CSV formats. Additionally, the script processes the data to remove any AWS identifiers that may be present in the Markdown files, folders, and internal references to other files in the backup.

It should be noted that the script always keeps two backups: the current one and the previous one.

> !! At no time is the information (credentials, tokens) used in the script recompiled.!!

## Requirements & Installation
To use this tool, you need to have the Selenium module installed. You can install it by running the following command in your terminal:

```bash
pip install selenium
pip install requests
```

After that, you can download the repository by running the following commands:

```bash
git clone https://github.com/shockz-offsec/Automatic-Notion-Backup.git
cd Automatic-Notion-Backup
```

### Compatibility

This script is compatible with both Windows and Linux operating systems and requires Python 3.

## Configuration

The script's configuration is defined in the config.json file, which has the following structure:

```json
{
    "REMOVE_IDS": true,
    "NOTION_SPACE_ID":"Your_space_id",
    "DOWNLOAD_PATH": "C:\\Users\\YourUsername\\Downloads",
    "TARGET_PATH": "C:\\path\\to\\your\\backup\\folder",
    "DEBUG_PATH": "C:\\path\\to\\your\\logs\\folder",
    "EMAIL":"your_notion_email",
    "PASSWORD":"your_password"
}
```

* `REMOVE_IDS`: a boolean parameter that indicates whether the script should remove AWS identifiers from the downloaded files.
* `NOTION_SPACE_ID`: The space id of your notion notes.
* `DOWNLOAD_PATH`: the path where the downloaded files will be stored.
* `TARGET_PATH`: the path where the processed backup files will be stored.
* `DEBUG_PATH`: the path where the script logs will be saved.
* `EMAIL`: the email address associated with the Notion account.
* `PASSWORD`: the password associated with the Notion account.

## UPDATE 2023
Notion has recently added security measures by creating a Notion backup link through internal API calls that require authentication and authorization, using token_v2 and space_id. 

Therefore, we have implemented web scraping authentication on the Notion account to enable downloading the export. This approach combines web scraping authentication with export requests via the internal API. 

Although the acquisition of token_v2 has been automated, it is still necessary to obtain the space_id of the Notion notes to be exported manually

## How it works

The script automates the web scraping authentication process in the background, eliminating the need for user intervention. Subsequently, the script obtains the token_v2 and requests an export using Notion's internal calls, generating an export URL. 

The export is downloaded and processed according to the user's choice in the configuration file, which can remove AWS identifiers from markdown files, folders, and internal file references. Old backups are then deleted, leaving only the current and most recent backups. 

The processed export is compressed into a zip file with the format `notion_export-dd-mm-yyyy.zip`. 

Additionally, the script generates a log file of all the actions performed during the process, using the `debug-dd-mm-yyyy.log` format.

The script uses the Firefox webdriver (geckodriver), which is automatically installed during the setup process.


## Getting NOTION_TOKEN and SPACE_ID for using Notion API

- Open your Notion in the browser
- Right-click anywhere on the page and select "Inspect Element".
  - 1º click on the "Network" tab, refresh the page (you can press F5).
  - 2º Search for "getPublicSpaceData" and select one occurrence.
  - 3º Your space ID is the first value associated with the first "id" field in the "response" tab.
  - 4º Copy and paste that ID into the *config.json* file under the "NOTION_SPACE_ID" field.
  
![STEPS](https://user-images.githubusercontent.com/67438760/230782980-9794d5d9-1045-4f2a-923b-396b0725f255.png)

## Usage

```bash
python3 notion_backup.py"
```

## Automating backups

In Windows, you can automate the script by creating a scheduled task with the Windows Task Scheduler. This can be done by creating a `.bat` file with the following contents:

```batch
@echo off
C:\Python3\python.exe "C:\path\to\notion_backup.py"
```
This will allow the script to run automatically at specified intervals without requiring manual intervention.

In Linux you can use Cron for example.

## Complete web-scraping version removing the need for tokens and private Notion APIs

The backup process is entirely carried out in the background using web scraping, without requiring any user input.

[Link to the Github repository](https://github.com/shockz-offsec/Scraping-Notion-Backup)
