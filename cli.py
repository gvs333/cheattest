"""Accepts command aliases as cli arguments and executes corresponding
commands sequentually.
"""

import sys

from cheattest.constants import YAML_CONF_PATH
from cheattest.utils import Utils


if __name__ == '__main__':
    conf = Utils.load_yaml_config(YAML_CONF_PATH)
    commands = sys.argv[1:]

    Utils.execute_commands(commands, conf)
