from datetime import datetime

class Log():

    def add(self, *texts, mode=''):  # mode = 'c' for console only, 'f' - for file only
        text = []
        for string in texts:
            string = str(string).replace('\n', ' ')
            if len(string) > 100:
                string = string [:95] + '...'
            text.append(string)
        text = ' | '.join([str(string) for string in text])
        if mode != 'c':
            with open ('log.txt', mode='a', encoding='UTF-8') as log_file:
                print(f"[{datetime.now().strftime('%d.%m.%y %H:%M:%S')}] {text}", file=log_file)
        if mode != 'f':
            print(f'[log] {text}')

    def user_activity(self, *texts, user, mode =''):
        self.add(*texts, user.id, user.first_name, user.last_name, user.username, mode=mode)

    def bot_activity(self, *texts, mode =''):
        self.add('bot wrote:', *texts, mode=mode)


    def br(self):
        self.add('')

    def clear(self):
        with open ('log.txt', mode='w', encoding='UTF-8') as log_file:
            print('', end='', file=log_file)


log = Log()
