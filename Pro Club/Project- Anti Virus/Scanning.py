import requests
import time 
import os 

url = 'https://www.virustotal.com/api/v3/files'
api_key = '70f9b90c35cb48d962a3bd27eb549977ca52e3400a6046250cc8a4780dabff09'
headers = {'x-apikey': api_key,}

def get_files(path):
    files_list = []
    if os.path.isfile(path): 
        files_list.append(path)
    elif os.path.isdir(path):  
        for root, _, files in os.walk(path):
            for file in files:
                full_path = os.path.join(root, file)
                files_list.append(full_path)
    else:
        raise ValueError("Invalid path provided")
    return files_list

def upload_file(file_path):
    with open(file_path, 'rb') as file_to_upload:
        files = {'file': (file_path, file_to_upload)}
        response = requests.post(url, headers=headers, files=files)
        return response.json()['data']['id']

class TooManyFilesScannedError(Exception):
    pass

def get_analysis_results(id_list, files_list):
    result_dict = {}#
    for i in range(len(id_list)):#
        analysis_url = f'https://www.virustotal.com/api/v3/analyses/{id_list[i]}'#
        response = requests.get(analysis_url, headers=headers)#

        if response.status_code == 200:#
            result_data = response.json()#
            if 'data' in result_data:#
                if result_data['data']['attributes']['status'] == 'completed':#
                    if result_data['data']['attributes']['stats']['malicious'] > 0:#
                        result_dict[files_list[i]] = 'THE FILE WAS FOUND AS MALICIOUS! BE AWARE'#
                    else:
                        result_dict[files_list[i]] = 'the FIle is safe to use!'
        else:
            error_message = f'Error {response.status_code}: {response.text}'
            result_dict[files_list[i]] = f'Error retrieving analysis results: {error_message}'


    return result_dict


