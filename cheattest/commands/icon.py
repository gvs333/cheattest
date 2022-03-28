import os
import psutil
import re
import sys
import _thread

import pystray
from PIL import Image, ImageDraw, ImageFont

from cheattest.commands.base import BaseCommand
from cheattest.constants import ICON_COMMANDS_SOCK_PATH, PACKET_LENGTH, IconProtocolValue
from cheattest.utils import Utils


class StartIconCommand(BaseCommand):
    """Draws icon and listens for incomming commands."""

    def __init__(self,
                 answers_local_filepath: str,
                 icon_image_props: dict,
                 icon_dropdown_names: dict,
                 **kwargs):
        self.answers_path = Utils.resolve_path(answers_local_filepath)

        self.font = ImageFont.truetype(Utils.resolve_path(icon_image_props['font_path']),
                                       icon_image_props['font_size'])
        self.icon_dropdown_names = icon_dropdown_names
        self.chars_per_screen = icon_image_props['chars_per_screen']
        self.image_sizes = icon_image_props['sizes']
        self.text_coords = icon_image_props['text_coords']

        self.offset = 0
        self.data = ''
        self.is_hidden = False

    def do(self):
        self.sync_answers()

        self.menu = [
            pystray.MenuItem(self.icon_dropdown_names['left'], self.left),
            pystray.MenuItem(self.icon_dropdown_names['right'], self.right),
            pystray.MenuItem(self.icon_dropdown_names['sync_answers'], self.sync_answers),
            pystray.MenuItem(self.icon_dropdown_names['toggle_visibility'], self.toggle_visibility),
            pystray.MenuItem(self.icon_dropdown_names['exit'], self.exit)
        ]

        image = self.create_filled_icon_image()
        self.icon = pystray.Icon("name", image, "title", self.menu)
        _thread.start_new_thread(self.listen_for_commands, tuple())
        self.icon.run()

    def listen_for_commands(self):
        sock = Utils.create_unix_udp_socket_server(ICON_COMMANDS_SOCK_PATH)

        while 1:
            data, _ = sock.recvfrom(PACKET_LENGTH)
            if data:
                data = data.decode()
                if data == IconProtocolValue.LEFT:
                    self.left()
                elif data == IconProtocolValue.RIGHT:
                    self.right()
                elif data == IconProtocolValue.SYNC_ANSWERS:
                    self.sync_answers()
                elif data == IconProtocolValue.TOGGLE_VISIBILITY:
                    self.toggle_visibility()
                elif data == IconProtocolValue.EXIT:
                    sock.close()
                    break

    def sync_answers(self):
        """Syncs answers with local machine."""

        with open(self.answers_path) as f:
            # remove white spaces
            self.data = re.sub('\\s', '', f.read())

        self.end_part_length = len(self.data) % self.chars_per_screen
        if not self.end_part_length:
            self.end_part_length = self.chars_per_screen

    def left(self):
        """Icon shows previous chars."""

        self.offset -= self.chars_per_screen
        if self.offset < 0:
            self.offset = max(0, len(self.data) - self.end_part_length)
        self.redraw()

    def right(self):
        """Icon shows next chars."""

        self.offset += self.chars_per_screen
        if self.offset >= len(self.data):
            self.offset = 0
        self.redraw()

    def toggle_visibility(self):
        """Hides/shows icon image."""

        if self.is_hidden:
            self.redraw()
        else:
            self.icon.icon = self.create_icon_image()
        self.is_hidden ^= True

    def exit(self):
        sys.exit(0)

    def redraw(self):
        """Redraws icon."""

        self.icon.icon = self.create_filled_icon_image()

    def create_filled_icon_image(self) -> Image:
        """Creates icon image filled with file's part's text."""

        image = self.create_icon_image()
        draw = ImageDraw.Draw(image)
        draw.text(self.text_coords,
                  self.data[self.offset:self.offset+self.chars_per_screen],
                  font=self.font)

        return image

    def create_icon_image(self) -> Image:
        """Creates empty icon image."""

        return Image.new("RGBA",
                         self.image_sizes,
                         (255, 255, 255, 0))


class KillIconCommand(BaseCommand):
    """Kills all the icon processes(that are listening on the socket)."""

    def do(self):
        for conn in psutil.net_connections("unix"):
            if conn.laddr == ICON_COMMANDS_SOCK_PATH and conn.pid != os.getpid():
                psutil.Process(conn.pid).terminate()


RestartIconCommand = Utils.create_multi_command(KillIconCommand, StartIconCommand)
