#!/usr/bin/env python3
import os
import sys
import json
import time
import requests
import urllib.request
from datetime import datetime
import json

TIME_ZONE = "Europe/Paris"
NOTION_API = 'https://www.notion.so/api/v3'

data = {}
with open(os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)),'config.json'))) as file:
    data = json.load(file)
    
NOTION_TOKEN_V2 = data["NOTION_TOKEN_V2"]
NOTION_SPACE_ID = data["NOTION_SPACE_ID"]
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
    req =  requests.post(
        f'{NOTION_API}/{endpoint}',
        data = json.dumps(params).encode('utf8'),
        headers = {
            'content-type': 'application/json',
            'cookie': f'token_v2={NOTION_TOKEN_V2}; '
        },
    )
    return req.json()


def export():
    try:
        task_id = request('enqueueTask', ENQUEUE_TASK_PARAM).get('taskId')
    except Exception as e:
        with open("C:\\Users\\Shockz\\Desktop\\NotionError.txt","w") as f:
            f.write(str(e))
            f.write("\nActualiza NOTION_TOKEN_V2 (cogiendolo del web browsers, en Application)")
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

    today = datetime.today().strftime('%d-%m-%Y')
    SAVE_DIR= TARGET_PATH
    EXPORT_FILENAME = "notion_export-" + today + ".zip"
    base_name = os.path.join(SAVE_DIR, "notion_export-")
    today_path = os.path.join(base_name +  "notion_export-" + today + ".zip")
    
    backups = [d for d in os.listdir(SAVE_DIR) if "notion_export" in d]
    
    if not os.path.exists(today_path):
        if len(backups) >= 2:
            os.remove(base_name + datetime.strftime(min([datetime.strptime(str(back.split('export-')[1].replace('.zip','')),'%d-%m-%Y') for back in backups]),'%d-%m-%Y') + '.zip')

    urllib.request.urlretrieve(
        export_url, os.path.join(TARGET_PATH, EXPORT_FILENAME),
        reporthook = lambda c, bs, ts: print(f"\r{int(c * bs * 100 / ts)}%", end="")
    )
    
    print(f'\nDownload complete: {EXPORT_FILENAME}')

if __name__ == "__main__":
    export()
