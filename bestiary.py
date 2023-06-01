import json
import re
from random import randint

class Bestiary:

    def __init__(self):
        with open('monsters.json', mode='r', encoding='UTF-8') as monsters_file:
            self.monsters = json.load(monsters_file)  # contains a list of monsters
        self.format()


    def format(self):  # remove tags <..> from text
        for monster in self.monsters:
            for key,value in monster.items():
                if isinstance(value, str): # remove tags <..>
                    value = value.replace('<p>', '').replace('</p>', '')
                    value = value.replace('<div>', '').replace('</div>', '')
                    value = value.replace('<em>', '<i>').replace('</em>', '</i>')
                    value = value.replace('<strong>', '\n<u>').replace('</strong>', '</u>')
                    monster[key] = value


        return



    def get_monster_names(self, text):
        '''
        Find names of monsters in bestiary
        :param text: part of the name
        :return: list of tuples, tuple = (mocter_id(int), monster_name(str))
        '''
        monster_list = []
        for i in range (len(self.monsters)):
            if text.lower() in self.monsters[i]['name'].lower():
                monster_list.append((i, self.monsters[i]['name']))
        return monster_list

    def get_monster_by_name(self, text):
        '''
        Find a monster by name
        :param text: name (case insensitive)
        :return: index of the monster
        '''
        for i in range(len(self.monsters)):
            if text.lower() == self.monsters[i]['name'].lower():
                return i
        return None

    def create_card(self, id):
        '''
        Create a card with monster data
        :param id: monster id
        :return: monster data in a text format
        '''
        card = ''
        for k, v in self.monsters[id].items():
            if k == 'name':
                card += f'<b>{v.upper()}</b>\n'
            elif k == 'meta':
                card += f'<code>{v}</code>\n\n'
            elif k in ('STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'):
                card += f"<b>{k}</b>: {v} {self.monsters[id][k+'_mod']}\n"
            elif '_mod' in k or k == 'img_url':
                continue
            else:
                if 'Actions' in k or 'Traits' in k:
                    card += '\n'
                card += f'<b>{k}</b>: {v}\n'
        return card

    def roll_hp(self, monster_id):
        hp_rule = self.monsters[monster_id]['Hit Points']
        numbers = re.findall(r'\d+', hp_rule)
        numbers = [int(number) for number in numbers]
        dice_amount, dice = numbers[1:3]
        if len(numbers) == 4:
            add_hp = numbers[3]
        else:
            add_hp = 0

        hp = []
        for i in range(dice_amount):
            res = randint(1,dice)
            hp.append(res)

        if add_hp != 0:
            hp.append(add_hp)

        hp_num = sum(hp)
        hp_string = ' + '.join([str(dice) for dice in hp])
        hp_string = '<code>' + hp_string + '</code>'

        return hp_num, hp_string


bestiary = Bestiary()
