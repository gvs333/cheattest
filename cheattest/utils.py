import functools
import importlib
import os
import socket
from inspect import isclass
from typing import Any, Dict, Sequence, Type

import yaml

from cheattest.commands.base import BaseCommand
from cheattest.constants import ROOT_DIR


class Utils:

    @staticmethod
    def create_unix_udp_socket_server(path: str) -> socket.socket:
        """Creates UDP Unix socket binding it to `path`."""

        if os.path.exists(path):
            os.remove(path)

        os.makedirs(os.path.dirname(path), exist_ok=True)
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        sock.bind(path)

        return sock

    @staticmethod
    def connect_to_unix_udp_socket(path: str) -> socket.socket:
        """Connects to UDP Unix socket."""

        sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        sock.connect(path)

        return sock

    @staticmethod
    def execute_commands(commands: Sequence[str], conf: Dict[str, Any]):
        """Executes commands sequentially.

        Args:
        commands: list of command aliases
        conf: dict with all conf
        """

        for command in commands:
            klass = Utils.load_command_class(conf, command)
            instance = klass(**conf)
            instance.do()

    @staticmethod
    def load_command_class(conf: Dict[str, Any], command_alias: str) -> Type[BaseCommand]:
        klass = Utils.load_module_object(conf['commands_mapping'][command_alias])
        assert isclass(klass) and issubclass(klass, BaseCommand)

        return klass

    @staticmethod
    def load_module_object(path: str) -> Any:
        """Loads module object via importlib.

        Args:
            path: dotted path to the object.
            Last part is an object name within module."""

        last_dot = path.rindex(".")
        module_name = path[:last_dot]
        module = importlib.import_module(module_name)
        class_name = path[last_dot+1:]

        return getattr(module, class_name)

    @staticmethod
    def create_multi_command(*command_classes: type) -> Type[BaseCommand]:
        """Create a wrapper class for multiple commands."""

        for klass in command_classes:
            if not issubclass(klass, BaseCommand):
                raise Exception("{klass} shoud be a subclass of BaseCommand.")

        class MultiCommand(BaseCommand):
            """Wrapper class for multple commands."""

            def __init__(self, *args, **kwargs):
                for klass in command_classes:
                    klass.__init__(self, *args, **kwargs)

            def do(self):
                for klass in command_classes:
                    klass.do(self)

        MultiCommand.__bases__ = command_classes

        return MultiCommand

    @staticmethod
    def partialclass(cls: type, *args, **kwargs) -> type:

        class NewCls(cls):
            __init__ = functools.partialmethod(cls.__init__, *args, **kwargs)

        return NewCls

    @staticmethod
    def load_yaml_config(path: str) -> Any:
        with open(path) as f:
            return yaml.load(f, yaml.Loader)

    @staticmethod
    def resolve_path(path: str) -> str:
        """Returns an absolute path if it's relative according to the project's
        root directory.
        """

        if not os.path.isabs(path):
            path = os.path.join(ROOT_DIR, path)

        return path
