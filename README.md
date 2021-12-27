# Automatic-Notion-Backup
A script to automate the process of downloading Markdown and CSV backups of Notion. In addition, the data is processed to remove the AWS identifier present in the files.

# Instalation
```
git clone https://github.com/jmlgomez73/Automatic-Notion-Backup.git
cd Automatic-Notion-Backup
```

# Usage

```
python3 notion_backup.py "target_path"
```

# Automating backups

In Windows it can be done by creating a scheduled task with the Windows task scheduler.
In Linux using cron for example.
