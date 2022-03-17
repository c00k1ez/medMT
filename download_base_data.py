import requests
import os
import zipfile


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


def open_zip(file_path, target_dir):
    with zipfile.ZipFile(file_path,"r") as zip_ref:
        zip_ref.extractall(target_dir)


if __name__ == "__main__":
    base_dir = './train_test_data'
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    file_id = '163LCsGjr2YKY_PZ11nd-r79TRRanrWvj'
    destination = f'{base_dir}/data.zip'
    download_file_from_google_drive(file_id, destination)
    open_zip(destination, base_dir)
