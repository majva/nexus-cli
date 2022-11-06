

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Callable

from app_nexuscli_core.service_collection import CoreCollection


class NexusCli:
    
    def __init__(self):
        super(NexusCli, self).__init__()
        
    def __run_app__(self, cli_manager):
        cli_manager.check_argumants()

        # # components = Components()
        # # components.get_latest_components(repository_name="docker-hosted")
        
        # assets = Assets()
        # assets.get_all_assets(repository_name="docker-hosted")
        # # assets.delete_old_assets(
        # #     latest_assets=components.latest_package
        # # )

    main: Callable = Callable(
        __run_app__, self=None,
        cli_manager=CoreCollection.cli_manager
    )
