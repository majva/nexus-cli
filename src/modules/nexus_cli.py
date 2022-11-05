
from .apis.components import Components
from .apis.assets import Assets


class NexusCli:
    
    def __init__(self):
        super(NexusCli, self).__init__()
        
    def start(self):
        # components = Components()
        # components.get_latest_components(repository_name="docker-hosted")
        
        assets = Assets()
        assets.get_all_assets(repository_name="docker-hosted")
        # assets.delete_old_assets(
        #     latest_assets=components.latest_package
        # )
