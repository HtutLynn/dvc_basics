import os
import argparse
from azure.storage.blob import BlobServiceClient

CONNECTION_STRING = os.environ['AZURE_STORAGE_CONNECTION_STRING']
CONTAINER_NAME = "cvblob"

service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = service_client.get_container_client(CONTAINER_NAME)

def upload_file(source, dest):

    '''
    Upload a single file to a path inside the container
    
    Parameters
    ----------

    source : string
             absolute to the single file at the local source

    dest : string
           path of the azure blob (single file) at the azure storage 
    '''
    print(f'Uploading {source} to {dest}')
    with open(source, 'rb') as data:
        container_client.upload_blob(name=dest, data=data, overwrite=True)

def upload_dir(source, dest):
    '''
    Upload a directory to a path inside the container

    Parameters
    ----------

    source : string
            path to the folder at the local source

    dest : string
           path to the folder at the azure storage
    '''
    for root, dirs, files in os.walk(source):
        for name in files:
            # dir_part = os.path.relpath(root, source)
            # dir_part = '' if dir_part == '.' else dir_part + '/'
            file_path = os.path.join(root, name)
            blob_path = dest + name
            upload_file(file_path, blob_path)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload folder to azure storage blob')
    parser.add_argument('--path', '-p', type=str, help='path to the folder at the local source')
    parser.add_argument('--dest', '-d', type=str, help='path to the folder at the azure storage')
    args = parser.parse_args()
    upload_dir(args.path, args.dest)