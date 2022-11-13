
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

        self.is_sha_exist: list() = list()
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
        
        if (assets["continuationToken"] != None):
            for item in assets["items"]:
                # if str(item["path"]).find("-/blobs/") == -1:
                if item["checksum"]["sha256"] not in self.is_sha_exist:
                    self.all_assets.append({
                        "asset_id": item["id"],
                        "sha256": item["checksum"]["sha256"]
                    })
                    self.is_sha_exist.append(item["checksum"]["sha256"])
            self.get_all_assets(repository_name="docker-hosted", continuation_token=assets["continuationToken"])
        else:
            for item in assets["items"]:
                # if str(item["path"]).find("-/blobs/") == -1:
                if item["checksum"]["sha256"] not in self.is_sha_exist:
                    self.all_assets.append({
                        "asset_id": item["id"],
                        "sha256": item["checksum"]["sha256"]
                    })
                    self.is_sha_exist.append(item["checksum"]["sha256"])
            return
            
    def delete_old_assets(self, latest_assets: list):
        delete_item: set = set()
        print("all_assets: " + str(len(self.all_assets)))
        for item in self.all_assets:
                for latest_asset in latest_assets:
                    if (("sha256:" + item["sha256"]) not in latest_asset["fslayers"]) and (item["asset_id"] != latest_asset["asset_id"]):
                        delete_item.add(item["asset_id"])
        print("delete_item " + str(len(delete_item)))

        for item in delete_item:
            response = delete(
                self.base_url + f"/service/rest/v1/assets/{item}",
                headers={
                    "accept": "application/json", 
                    "Authorization": f"Basic {self.encoded}"
                }
            )

    def get_assets_count(self, repository_name: str): 
        self.get_all_assets(repository_name=repository_name)
        return len(self.all_assets)
