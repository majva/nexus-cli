
from requests import get

from json import loads as json_loads
from os import environ
import base64


class Components:
    
    def __init__(self):
        super(Components, self).__init__()

        pass_phrase: bytes = bytes(f"{str(environ.get('USERNAME'))}:{str(environ.get('PASSWORD'))}", 'utf-8')

        self.base_url: str = str(environ.get('BASE_URL'))
        self.encoded: str = str(base64.b64encode(pass_phrase)).replace('b', '')

        # get latest packages exist in nexus
        self.latest_package: list = list()
        
    def get_components(self, repository_name: str, continuation_token: str = ''):
        
        if continuation_token != '':
            api = f"/service/rest/v1/components?repository={repository_name}&continuationToken={continuation_token}"
        else:
            api = f"/service/rest/v1/components?repository={repository_name}"
        
        response = get(
            self.base_url + api,
            headers={
                "accept": "application/json", 
                "Authorization": f"Basic {self.encoded}"
            }
        )
        
        components = json_loads(response.content)
        if (components["continuationToken"] != None):
            for item in components["items"]:
                self.latest_package.append({
                    "name": item["name"],
                    "sha256": item["assets"][0]["checksum"]["sha256"],
                    "asset_id": item["assets"][0]["id"],
                    "fslayers": self.get_all_manifest(component_path=item["name"])
                })
            self.get_components(repository_name=repository_name, continuation_token=components["continuationToken"])
        else:
            for item in components["items"]:
                self.latest_package.append({
                    "name": item["name"],
                    "sha256": item["assets"][0]["checksum"]["sha256"],
                    "asset_id": item["assets"][0]["id"],
                    "fslayers": self.get_all_manifest(component_path=item["name"])
                })

    def get_components_count(self, repository_name: str) -> int:
        self.get_components(repository_name=repository_name)
        print(self.latest_package)
        return len(self.latest_package)

    def get_all_manifest(self, component_path: str):
        
        fslayers: set = set()

        response = get(
            self.base_url + f"/repository/docker-hosted/v2/{component_path}/manifests/latest",
            headers={
                "accept": "application/json", 
                "Authorization": f"Basic {self.encoded}"
            }
        )
        fs_layers = json_loads(response.content)

        for item in fs_layers["fsLayers"]:
            fslayers.add(item["blobSum"])
        print("fslayers: " + str(len(fslayers)))
        return fslayers
