
from requests import post, get, delete

from json import loads as json_loads
from os import environ
import base64


class Assets:
    
    def __init__(self):
        super(Assets, self).__init__()
        
        pass_phrase: bytes = bytes(f"{str(environ.get('USERNAME'))}:{str(environ.get('PASSWORD'))}", 'utf-8')

        self.base_url: str = str(environ.get('BASE_URL'))
        self.encoded: str = str(base64.b64encode(pass_phrase)).replace('b', '')

        self.all_assets: list = list()
        
    def get_all_assets(self, repository_name: str, continuation_token: str = ''):
        
        if continuation_token != '':
            api = f"/service/rest/v1/assets?repository={repository_name}&continuationToken={continuation_token}"
        else:
            api = f"/service/rest/v1/assets?repository={repository_name}"
        
        response = get(
            self.base_url + api,
            headers={
                "accept": "application/json", 
                "Authorization": f"Basic {self.encoded}"
            }
        )
        
        assets = json_loads(response.content)
        
        if assets["items"] != None:
            for item in assets["items"]:
                self.all_assets.append({
                    "asset_id": item["id"],
                    "sha256": item["checksum"]["sha256"]
                })
            
        if (assets["continuationToken"] != None):
            self.get_all_assets(repository_name="docker-hosted", continuation_token=assets["continuationToken"])
        else:
            print(len(self.all_assets))
            
    def delete_old_assets(self, latest_assets: list):
        for item in self.all_assets:
            for latest_asset in latest_assets:
                if item["asset_id"] != latest_asset["asset_id"]:
                    response = delete(
                        self.base_url + f"/service/rest/v1/assets/{item['asset_id']}",
                        headers={
                            "accept": "application/json", 
                            "Authorization": f"Basic {self.encoded}"
                        }
                    )