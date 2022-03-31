#!/usr/bin/env python3
import os
import sys
import json
import time
import urllib
import urllib.request
import shutil
from datetime import datetime
import zipfile
import json

TIME_ZONE = "Europe/Paris"
NOTION_API = 'https://www.notion.so/api/v3'

data = {}
with open(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'config.json'))) as file:
    data = json.load(file)
    
NOTION_TOKEN_V2 = data["NOTION_TOKEN_V2"]
NOTION_SPACE_ID = data["NOTION_SPACE_ID"]
EXPORT_FILENAME = "export.zip"
TARGET_PATH = data["TARGET_PATH"]

ENQUEUE_TASK_PARAM = {
    "task": {
        "eventName": "exportSpace", "request": {
            "spaceId": NOTION_SPACE_ID,
            "exportOptions": {"exportType": "markdown", "timeZone": TIME_ZONE, "locale": "en"}
        }
    }
}

def request(endpoint: str, params: object):
    req = urllib.request.Request(
        f'{NOTION_API}/{endpoint}',
        data = json.dumps(params).encode('utf8'),
        headers = {
            'content-type': 'application/json',
            'cookie': f'token_v2={NOTION_TOKEN_V2}; '
        },
    )
    response = urllib.request.urlopen(req)
    return json.loads(response.read().decode('utf8'))


def export():
    try:
        task_id = request('enqueueTask', ENQUEUE_TASK_PARAM).get('taskId')
    except Exception as e:
        with open("C:\\Users\\Shockz\\Desktop\\NotionError.txt","w") as f:
            f.write(str(e))
        quit()

    print(f'Enqueued task {task_id}')

    while True:
        time.sleep(2)
        tasks = request("getTasks", {"taskIds": [task_id]}).get('results')
        task = next(t for t in tasks if t.get('id') == task_id)
        print(f'\rPages exported: {task.get("status").get("pagesExported")}', end="")

        if task.get('state') == 'success':
            break

    export_url = task.get('status').get('exportURL')
    print(f'\nExport created, downloading: \n{export_url}')

    urllib.request.urlretrieve(
        export_url, os.path.join(TARGET_PATH, EXPORT_FILENAME),
        reporthook = lambda c, bs, ts: print(f"\r{int(c * bs * 100 / ts)}%", end="")
    )
    print(f'\nDownload complete: {EXPORT_FILENAME}')
    save()

def save():
    
    today = datetime.today().strftime('%d-%m-%Y')
    
    SAVE_DIR= TARGET_PATH
    exported_file = os.path.join(SAVE_DIR, 'export.zip')
    name = "notion_export-" + today
    base_name = os.path.join(SAVE_DIR, "notion_export-")
    today_path = os.path.join(base_name + today)
    today_file =  today_path + ".zip"
    
    backups = [d for d in os.listdir(SAVE_DIR) if "notion_export" in d]
    
    
    if not os.path.exists(today_file):
        
        if len(backups) > 1:
            os.remove(base_name + datetime.strftime(min([datetime.strptime(str(back.split('export-')[1].replace('.zip','')),'%d-%m-%Y') for back in backups]),'%d-%m-%Y') + '.zip')
        
        if exported_file:
            with zipfile.ZipFile(exported_file) as zip:
                zip.extractall(today_path)
            os.remove(exported_file)
        
    """
    if not os.path.exists(today_path):
        if len(backups) > 1:
            shutil.rmtree(base_name + datetime.strftime(min([datetime.strptime(str(back.split('export-')[1]),'%d-%m-%Y') for back in backups]),'%d-%m-%Y'))
        
        if exported_file:
            with zipfile.ZipFile(exported_file) as zip:
                zip.extractall(today_path)
            os.remove(exported_file)
    """

        
    removing_identifiers(today_path, today_file)
def removing_identifiers(today_path : str, today_file : str):
    
    ids_files = []
    
    for base, dirs, files in os.walk(today_path):
        for file in files:
            if file.endswith('.md'):
                files_pattern = file.split(" ")[-1].split(".")[0]
                ids_files.append(files_pattern)
            
    ids_files = list(set(ids_files))
    
    temp_dirs = os.walk(today_path, topdown=False)
    for root, dirs, files in temp_dirs:
        for i in dirs:
            directory = os.path.join(root,i)
            try:
                os.rename(directory,directory.replace(directory.split(" ")[-1],""))
            except (FileExistsError,FileNotFoundError): # log file
                with open(os.path.join(TARGET_PATH, "log.txt"),'a', encoding="utf8") as f:
                    f.write(directory + '\n')
                
    
    temp_file = os.walk(today_path, topdown=False)
    for root, dirs, files in temp_file:
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root,file)
                new_path = file_path.replace(" "+file_path.split(" ")[-1].split(".")[0],"")
                
                lines = []
                with open(file_path,'r', encoding="utf8") as f:
                    lines = f.readlines()
                rem = False
                try:
                    with open(new_path, "w", encoding="utf8") as f:
                        for line in lines:
                            for idn in ids_files:
                                line = line.replace("%20"+idn,"")
                            f.write(line)
                            rem = True
                except:
                    with open(os.path.join(TARGET_PATH, "log.txt"),'a', encoding="utf8") as f:
                        f.write(new_path + '\n')
                    rem = False
                if rem and os.path.exists(new_path):
                    os.remove(file_path)
                else:
                    with open(os.path.join(TARGET_PATH, "log.txt"),'a', encoding="utf8") as f:
                        f.write("FAILING" + new_path + '\n')

    def zipdir(path, ziph):
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file), 
                        os.path.relpath(os.path.join(root, file), 
                                        os.path.join(path, '..')))

    with zipfile.ZipFile(f'{today_file}', 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir(f'{today_path}/', zipf)

    shutil.rmtree(today_path)

if __name__ == "__main__":
    export()