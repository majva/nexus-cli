
from sys import argv


class CLIManager:

    def __init__(self):
        super(CLIManager, self).__init__()
    
    def check_argumants(self):

        if (len(argv) <= 1):
            print ("For showing helps command please type python app.py -h")
            return

        if argv[1] == "-h" or argv[1] == "--help":
            from .components.help import HelpComponent
            HelpComponent.print()

        elif argv[1] == "-sc": # count of components
            from ...apis.components import Components
            components = Components()
            print(f"count of components: {components.get_components_count(argv[2])}")

        elif argv[1] == "-sa": # count of assets
            from ...apis.assets import Assets
            assets = Assets()
            print(f"count of assets: {components.get_components_count(argv[2])}")

        elif argv[1] == "-ad": # delete oldest assets
            from ...apis.assets import Assets
            from ...apis.components import Components
            components = Components()
            components.get_components(repository_name=argv[2])
            assets = Assets()
            assets.get_all_assets(repository_name=argv[2])
            assets.delete_old_assets(components.latest_package)

        elif argv[1] == "-jad": # activing the cron job for delete the oldest assets
            pass

            