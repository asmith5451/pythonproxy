"""
This module contains my modified "hipchatter.py" aka hipbarker.py. This is to
change the modules used from hiplogger which used python-simple-hipchat (which
is a version 1 token system from hipchat API's point of view) to hypchat which
is a stand-alone module that works with Hipchat API's version 2 token system
(which is the token that I was given from hipchat.

HypChat was built to ONLY work with "administrator" tokens or 'global' tokens.
Which is why I import HypChat's requests, restobject, bearerauth and linker. I
do that because i need to MANUALLY add the room number to the variable "rooms"
aka:

self.rooms = Linker('{0}/v2/room/1821618'.format(endpoint),
                    _requests=self._requests)

The number '1821618' is the ROOM NUMBER. If you want to use a NON-administrator
token you'll need to ADD this room number to that line. Otherwise you'll need to
comment out _new_match_rooms and surrounding variables to use administrator
tokens. It's all based on WHO you want to post as and HOW. I wanted to post as
"Lorde Barkington" and not as Adam Smith. That requires that I DON'T use a
administrator token to post from. Because an administrator token = "YOU". You'll
want a "ROOM" token to post as an alternate "Person" or character.
"""
import hypchat
from hypchat import _requests
from hypchat import requests
from hypchat.requests import BearerAuth
from hypchat.restobject import Linker
import os
# import pdb

# Lorde Barkington's TOKEN
THE_TOKEN = os.getenv("HIPBARKER_TOKEN")
if THE_TOKEN is None:
    THE_TOKEN = os.getenv("PYCHARM_TOKEN")
    # print(THE_TOKEN)

DEFAULT_ROOM_ID = 1821618
print(THE_TOKEN)


def non_admin_token(room_id):
    # Don't change or move this variable
    _old_match_rooms = hypchat.HypChat.__init__

    # Required to post to a single room as a non-administrator!
    def _new_match_rooms(self, token=THE_TOKEN,
                         endpoint='https://api.hipchat.com', verify=True):
        """
        The purpose of this snippit of code is to force the "rooms" variable
        in HypChat to post to a SINGLE room. If you don't do this it will
        attempt to post as an administrator which will result in a
        http error:

        403 Forbidden
        Annoying, yes, but not something that can't be overcome.
        """
        # _requests and endpoint are only here to satisfy the entire
        # 'self.rooms' statement.
        self._requests = _requests(auth=BearerAuth(token), verify=verify)
        self.rooms = Linker('{0}/v2/room/' + str(room_id).format(endpoint),
                            _requests=self._requests)
        self.endpoint = endpoint

    # Don't change or move this variable
    hypchat.HypChat.__init__ = _new_match_rooms
# End of non_admin_token():


class Hipbarker:
    """
    This class uses HypChat as a foundation for posting notifications to
    HipChat. HypChat requires a token. Tokens can be made here:

    https://kickback.hipchat.com/rooms/tokens/<ROOM NUMBER>

    After you have a token and room number figured out. You need only to plug
    them into the "bare minimum variables" then your done! You can now post
    messages(notifications) to the room provided! AS the LABEL found in:

    https://kickback.hipchat.com/rooms/tokens/<ROOM NUMBER>

    For example the name of my Barker for DAM-Barker is 'Lorde Barkington'. :D
    """

    # Assign token from env import or pycharm import.
    hipchat_token = THE_TOKEN

    def __init__(self, room_id=DEFAULT_ROOM_ID):
        # Change room_id if it was passed from external module
        self.room_id = room_id
        non_admin_token(self.room_id)

        # Assign HypChat specific variables
        self.barker_token = hypchat.HypChat(self.hipchat_token)
        errorcount = 0
        while errorcount < 3:
            try:
                self.barker_room = self.barker_token.get_room(id_or_name=self.room_id)
                break
            except:
                print("Failed to get room from hipchat. %s errors so far. Max 3 errors" % str(errorcount))
                errorcount += 1
        if errorcount == 3:
            quit()

    def post_message(self, message, color='yellow', notify=False):
        self.barker_room.notification(message, color=color, format='html',
                                      notify=notify)
# End of class Hipbarker:
__author__ = "Adam Smith"