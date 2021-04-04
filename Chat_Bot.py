# -*- coding: utf-8 -*-
import vk_api, vk
from vk_api.longpoll import VkLongPoll, VkEventType
import string
import wikipedia
import json
import random
import os

wikipedia.set_lang('RU')

main_token = ''

vk_session = vk_api.VkApi(token=main_token)
longpool = VkLongPoll(vk_session)

def get_name(id):
    user_get = vk_session.get_api().users.get(user_ids=(id))
    user_get = user_get[0]
    first_name = user_get['first_name']
    last_name = user_get['last_name']
    full_name = first_name + " " + last_name
    return full_name

def load_bd():
    file = open('data.txt', 'r')
    datas = file.read()
    datas = datas.splitlines()
    file.close()
    data = {}
    for i in datas:
        i = i.split(', ')
        data[str(i[0])] = {}
        data[str(i[0])]['Name'] = i[1]
    return data

data = load_bd()

def check_id(id):
    file = open('data.txt', 'r')
    if str(id) in file.read():
        return 1
    else:
        return 0
    file.close()

def save_bd(id):
    with open('data.txt', 'a') as file:
        p = str(id) + ', ' + str(get_name(id))
        file.write(p + '\n')

def get_keyboard(buts):
    nb = []
    color = ''
    for i in range(len(buts)):
        nb.append([])
        for k in range(len(buts[i])):
            nb[i].append(None)
    for i in range(len(buts)):
        for k in range(len(buts[i])):
            text = buts[i][k][0]
            if buts[i][k][1] == 'p':
                color = 'positive'
            elif buts[i][k][1] == 'n':
                color = 'negative'
            nb[i][k] = {
                'action': {
                    'type': 'text',
                    'payload': "{\"button\": \"" + "i" + "\"}",
                    'label': f'{text}'
                },
                'color': f'{color}'
            }
    first_keyboard = {
        'one_time': False,
        'buttons': nb
    }
    first_keyboard = json.dumps(first_keyboard, ensure_ascii=False).encode('utf-8')
    first_keyboard = str(first_keyboard.decode('utf-8'))
    return first_keyboard

keyboard_1 = get_keyboard(
    [
        [('Помощь', 'p')],
        [('Википедия', 'p')],
        [('Мем', 'p')],
        [('Шутка', 'p')]
    ]
)

def send_photo(id, photo):
    vk_session.method('messages.send', {'chat_id': id, 'attachment': photo, 'random_id': 0})

def random_meme():
    meme_list = []
    meme = random.randint(0, len(meme_list)-1)
    url = meme_list[meme]
    return url

def send_stick(id, number):
    vk_session.method('messages.send', {'chat_id': id, 'sticker_id': number, 'random_id': 0})

def random_joke():
    file = open('jokes.txt', 'r', encoding='utf-8')
    jokes = file.read()
    jokes = jokes.splitlines()
    file.close()
    num_j = []
    for joke in jokes:
        joke = joke.split(') ')
        num_j.append(joke[1])
    j = random.choice(num_j)
    return j

def joke(id, random_joke):
    vk_session.method('messages.send', {'chat_id': id, 'message': random_joke, 'random_id': 0})

def sender(id, text):
    vk_session.method('messages.send', {'chat_id': id, 'message': text, 'random_id': 0, 'keyboard': keyboard_1})

def main(data):
    for event in longpool.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            if check_id(event.user_id) == 0:
                save_bd(event.user_id)
            data = load_bd()
            msg = event.text.lower()
            id = event.chat_id
            msg_appeal = 'адам,'
            msg_club_appeal = '[club201709453|@club201709453]'
            if msg.split()[0] == msg_club_appeal:
                msg = msg.split()
                if 'помощь' in msg:
                    sender(id, f'Мое имя Адам. На данный момент, я являюсь тестовым вк-ботом (надеюсь не на долго...). Вы можете как общаться со мной в чате беседы (Написав: Адам, [ваше сообщение]) или же воспользоваться клавиатурой чата (Там присутсвуют не все мои функции). По имеющимся вопросам обращаться к @id{234371454}.')
                elif 'мем' in msg:
                    send_photo(id, random_meme())
                elif 'шутка' in msg:
                    joke(id, random_joke())
                elif 'википедия' in msg:
                    sender(id, 'Информацию о ком или о чем вы хотите найти?')
                    send_id = event.user_id
                    for event in longpool.listen():
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                            if send_id == event.user_id:
                                try:
                                    message_wiki = 'Вот что я нашёл: ' + str(wikipedia.summary(event.text))
                                    sender(id, message_wiki)
                                except:
                                    sender(id, 'Я не смог найти полезной информации в википедии, по данному запросу')
                            else:
                                continue
                            break
                else:
                    sender(id, 'Я не могу на это ответить')
            elif msg.split()[0] == msg_appeal:
                msg = msg.translate(str.maketrans('', '', string.punctuation))
                msg = msg.split()
                if 'привет' in msg:
                    sender(id, 'Приветсвую, ' + data[f'{event.user_id}']['Name'].split()[0] + '!')
                elif 'пока' in msg:
                    sender(id, 'До скорой встречи!')
                elif 'спасибо' in msg:
                    sender(id, 'Рад стараться!')
                elif 'мем' in msg:
                    send_photo(id, random_meme())
                elif 'википедия' in msg:
                    sender(id, 'Информацию о ком или о чем вы хотите найти?')
                    send_id = event.user_id
                    for event in longpool.listen():
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                            if send_id == event.user_id:
                                try:
                                    message_wiki = 'Вот что я нашёл: ' + str(wikipedia.summary(event.text))
                                    sender(id, message_wiki)
                                except:
                                    sender(id, 'Я не смог найти полезной информации в википедии, по данному запросу')
                            else:
                                continue
                            break
                else:
                    sender(id, 'Я не могу на это ответить')
main(data)