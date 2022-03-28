from os.path import abspath, dirname, join


ROOT_DIR = abspath(join(dirname(__file__), ".."))
SOCKS_DIR = join(ROOT_DIR, "socks")
RESOURCES_DIR = join(ROOT_DIR, "resources")
IMAGES_DIR = join(RESOURCES_DIR, "images")
YAML_CONF_PATH = join(ROOT_DIR, "conf.yaml")

ICON_COMMANDS_SOCK_PATH = join(RESOURCES_DIR, "listen_icon_commands.sock")
PACKET_LENGTH = 256
COMMAND_SEPARATOR = " "


class IconProtocolValue:
    LEFT = '0'
    RIGHT = '1'
    SYNC_ANSWERS = '2'
    TOGGLE_VISIBILITY = '3'
    EXIT = '4'
