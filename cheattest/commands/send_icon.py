from cheattest.commands.base import BaseCommand
from cheattest.constants import ICON_COMMANDS_SOCK_PATH, IconProtocolValue
from cheattest.utils import Utils


class SignalIconCommand(BaseCommand):
    """Sends command to icon."""

    def __init__(self, message: str, **kwargs):
        self.message = message.encode()

    def do(self):
        sock = Utils.connect_to_unix_udp_socket(ICON_COMMANDS_SOCK_PATH)
        sock.sendall(self.message)
        sock.close()


SendLeftIconCommand = Utils.partialclass(SignalIconCommand, message=IconProtocolValue.LEFT)
SendRightIconCommand = Utils.partialclass(SignalIconCommand, message=IconProtocolValue.RIGHT)
SendSyncIconCommand = Utils.partialclass(SignalIconCommand, message=IconProtocolValue.SYNC_ANSWERS)
SendToggleIconCommand = Utils.partialclass(SignalIconCommand, message=IconProtocolValue.TOGGLE_VISIBILITY)
