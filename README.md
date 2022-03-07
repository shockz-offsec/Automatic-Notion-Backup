# Automatic-Notion-Backup
A script to automate the process of downloading Markdown and CSV backups of Notion. In addition, the data is processed to remove the AWS identifier present in the files.
Pd: Always keeps 2 backups (actual, and older)

# Installation
```
git clone https://github.com/jmlgomez73/Automatic-Notion-Backup.git
cd Automatic-Notion-Backup
```

# Getting NOTION_TOKEN and SPACE_ID for using Notion API

- 1º Open your Notion in the browser
- 2º Right click anywhere inside the page and select "Inspect Element"
- 3º Locate "Application" and select "Cookies." Here you should be able to find "token_v2." Copy the property next to it called "Value." and paste it in the "NOTION_TOKEN_V2" field of the *config.json* file.
- 4º 
![Image](https://user-images.githubusercontent.com/67438760/147504406-7ebbddd9-eca3-4edd-9bec-48f724387d37.png)


Now go to the Network tab, as shown on a screenshot below Enable "XHR" filter (1), clear console (2), start the export (3), select "enqueueTask" (4).
  
Now scroll to the very bottom and under the “Request Payload” section you will see something like (6):
spaceId: "4489c211-09d6-4069-ae3b-1665e25d6c03"

Copy the value inside quotes and paste it in the NOTION_SPACE_ID field of the *config.json* file

- 5º Finally, type where you want your backups to be stored in the "TARGET_PATH" field of the *config.json* file.

> Each 2-3 months the notion token v2 will expire, so u'll get it again

# Usage

```
python3 notion_backup.py"
```

# Automating backups

In Windows it can be done by creating a scheduled task with the Windows task scheduler.
In Linux using Cron for example.
