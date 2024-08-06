import requests as refresh_requests
import os

from langchain.tools import BaseTool, StructuredTool, tool
import json
from langchain_community.utilities import Requests
from langchain.pydantic_v1 import BaseModel, Field
import uuid


token = '7353d23703a37d3a5554e63aa448bbc509b0cec0'
# Headers including the Authorization token (if needed)
headers = {'Authorization': f'Token {token}'}

requests = Requests(headers=headers)
root_url = 'http://adma.hopto.org'

class ADMA_get_meta_data_input_schema(BaseModel):
    file_path: str = Field(description="The path or name of the file in the ADMA system. The full path is like /username/ag_data/.../file_name, but here the file_path is the relative path after the ag_data directory.")

@tool("ADMA_get_meta_data", args_schema=ADMA_get_meta_data_input_schema)
def ADMA_get_meta_data(file_path):
  """ Always call this tool when the user want to get the meta data of a file or directory on the ADMA server."""
  api_url = f'{root_url}/api/meta_data/?target_path={file_path}'

  # Sending the GET request to the meta data of the file
  response = requests.get(api_url)

  # Checking the response from the server
  if response.status_code == 200:
      #print(response.json())
      return response.json()

  else:
      return {}
      #print("Failed to download the meta data:", response.text)


class ADMA_list_directory_contents_input_schema(BaseModel):
    dir_path: str = Field(description="The path or name of the directory in the ADMA system. The full path is like /username/ag_data/.../file_name, but here the dir_path is the relative path after the ag_data directory.")

@tool("ADMA_list_directory_contents", args_schema=ADMA_list_directory_contents_input_schema)
def ADMA_list_directory_contents(dir_path):
    """Always call this tool when the user want to list a directory on the ADMA server."""
    list_url = f"{root_url}/api/list/?target_path={dir_path}"
    response = requests.get(list_url)
    if response.status_code == 200:
        return response.json()  # Assuming the API returns a JSON list of paths
    else:
        print(f"Failed to list directory: {dir_path}, Status code: {response.status_code}, {response.text}")
        return []
    

class ADMA_get_running_instance_input_schema(BaseModel):
    dir_path: str = Field(description="The path or name of the directory in the ADMA system. The full path is like /username/ag_data/.../file_name, but here the dir_path is the relative path after the ag_data directory.")

@tool("ADMA_get_running_instance", args_schema=ADMA_get_running_instance_input_schema)
def ADMA_get_running_instance(dir_path):
    """Always call this tool when the user want to check if there is any running instance for dir_path on the ADMA server."""
    instance_url = f"{root_url}/api/get_running_instance/?target_path=ypan12/ag_data/{dir_path}"
    response = requests.get(instance_url)
    if response.status_code == 200:
        return response.json()  # Assuming the API returns a JSON list of paths
    else:
        return f"Failed to get running instance: {dir_path}, Status code: {response.status_code}, {response.text}"
        
    

class ADMA_check_file_input_schema(BaseModel):
    dir_path: str = Field(description="The path or name of the directory in the ADMA system. The full path is like /username/ag_data/.../file_name, but here the dir_path is the relative path after the ag_data directory.")

@tool("ADMA_check_file", args_schema=ADMA_check_file_input_schema)
def ADMA_check_file(dir_path):
    """Always call this tool when the user want to check the content of dir_path on the ADMA server."""
    download_url = f"{root_url}/api/download/?target_path={dir_path}"
    response = requests.get(download_url)

    if response.status_code == 200:
        rd = uuid.uuid4()
        with open(f"tmp/{rd}_{os.path.basename(dir_path)}", "wb") as f:
            f.write(response.content)
        result = {"type": "file", "path": f"tmp/{rd}_{os.path.basename(dir_path)}"}
        return result   
    else:
        return f"Failed to download file: {dir_path}, Status code: {response.status_code}, {response.text}"
         