from private_library.adapters.cli import create_cli

from .private_library_api import MessageBus

cli = create_cli(MessageBus)
