"""
    - created at 10/20/2021 by mehrad ghasempour
    - email: topcodermc@gmail.com
    - this package is gateways packages handler in IOC
"""

from dependency_injector.containers import DeclarativeContainer 
from dependency_injector.providers import Singleton

from .services.cli.cli_manager import CLIManager


class CoreCollection(DeclarativeContainer):
    """ IoC container of business service providers """
    
    cli_manager: Singleton = Singleton(
        CLIManager
    )