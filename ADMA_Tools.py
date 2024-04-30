import requests as refresh_requests
import os

from langchain.tools import BaseTool, StructuredTool, tool
import json
from langchain_community.utilities import Requests
from langchain.pydantic_v1 import BaseModel, Field



token = '7353d23703a37d3a5554e63aa448bbc509b0cec0'
# Headers including the Authorization token (if needed)
headers = {'Authorization': f'Token {token}'}

requests = Requests(headers=headers)
root_url = 'http://unladma.hopto.org'

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