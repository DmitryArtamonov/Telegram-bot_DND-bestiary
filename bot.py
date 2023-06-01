

from log import log
from bestiary import bestiary
import re

class Bestiary_bot:

    def __init__(self):
        self.message_start = "Hiiii....! I'm <b>Dungeons & Dragons</b> Bestiary bot. Just write a part of the monster's name and I'll find it for you!"
        self.message_short_name = 'Too short! Give me at least 3 characters.'
        self.message_no_monster = "Sorry I didn't find any monster. Try again."


    def print_monster(self, monster_id): # create an answer with monster's pic and card
        monster_id = int(monster_id)
        monster = bestiary.monsters[monster_id]
        hp_pattern = r'\((.*?)\)'
        hp_button = re.search(hp_pattern, monster['Hit Points']).group(1)
        reply = {}
        monster = bestiary.monsters[monster_id]
        if 'img_url' in monster:
            reply['pic'] = monster['img_url']
        reply['buttons'] = [bestiary.create_card(monster_id),
                            ('HP_'+str(monster_id), 'HP❤ ' + hp_button)]
        return reply

    def print_roll_hp(self, monster_id):
        hp = bestiary.roll_hp(monster_id)
        text = f'🎲 HP: {hp[0]}\n{hp[1]}'
        reply = {'text': text}
        return reply

    def text_replier(self, user_message):
        '''
        Create a reply on a text message.
        Keys = 'text', 'buttons', 'pic'
        Buttons are in a list, first index is the message, that should be shown upon buttons
        '''

        if len(user_message) < 3 :
            return {'text': self.message_short_name}

        else:
            names = bestiary.get_monster_names(user_message)

            if not names:
                return {'text': self.message_no_monster}

            elif len(names) == 1:  # if only one monster founded, return its card
                reply = self.print_monster(names[0][0])
                return reply

            else:
                reply = {'buttons': ['Choose:']}
                for monster in names:
                    reply['buttons'].append(monster)
                return reply

    def button_replier(self, button_id):
        '''
        Create a reply on a button pushed.
        Keys = 'text', 'buttons', 'pic'
        Buttons are in a list, first index is the message, that should be shown upon buttons
        '''
        if 'HP' in button_id:
            monster_id = int(button_id[3:])
            reply = self.print_roll_hp(monster_id)
        else:
            reply = self.print_monster(button_id)
        return reply


bestiary_bot = Bestiary_bot()