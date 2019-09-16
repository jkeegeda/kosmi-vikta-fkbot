from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
# Вместо костылей использование встроенной функции vk_api
from vk_api.utils import get_random_id 
from bs4 import BeautifulSoup
import requests, time, os, re

mytokenvk = os.environ.get('BOT_TOKEN_VK')
vk_session = vk_api.VkApi(token="mytokenvk")
longpull = VkLongPoll(vk_session)
vk = vk_session.get_api()
base_url = "http://loopy.ru/?word="

while True:
    # try позволит исключить ошибку timeout , которая иногда может пролезать
    try:
        for event in longpull.listen():  # для каждого эвента прослушивания
            if event.type == VkEventType.MESSAGE_NEW:  # если событие новое сообщение то
                # print(str(event.text))                                                #написать текст этого сообщения
                if event.to_me:
                    q = str(event.text).lower() # Приведение к единому регистру даст больше свободы для написания команды
                    # q присваиваем текст из события , а именно из сообщения
                    # print(q)
                    # print("---" * 10)

                    # в случае если викторина прервана из-за того что не найдено ответов на 3 вопроса подряд:
                    # можно так
                        #step = q.split("остановлена ", 1)[-1]
                        #if step == "за отсутствие к ней интереса.":
                    #быстрый вариант:
                    if re.search(r'(стоп|осанов|stop)',q) != None: # Регулярка позволит больше вариаций команд
                    # if 'остановлена!' in q:
                        vk.messages.send(
                            # chat_id= event.chat_id,
                            chat_id=48,
                            message="старт",
                            random_id=get_random_id(),
                        )
                    else:
                        pass

                    mask = q.split("Подсказка:", 1)[-1]  # выделяем слово из подсказки для составления маски
                    mask = mask.replace(' ', '')  # убираем пробелы
                    mask_num = len(mask)  # узнаем количество букв ответа из подсказки
                    # print(mask_num)
                    listmask = list(mask)
                    # print(listmask[0])
                    maska = str(listmask[0]) + str('*'*int(len(mask)-1))
                    # print(maska)

                    q = q.replace('&quot;', "")  # убираем ковычки ибо не читаемая кодировка символа
                    q = q.split(": ", 1)[0]  # делим предложение на 2 части (разделитель,что в скобках). Оставляем 1 часть(то что до разделителя)
                    # print(q)
                    # print(len(q))                                                          #вывести сколько элементов в списке(сколько букв в том , что мы сотавили)
                    if len(q) < 10:  # если осталось одно слово"подсказка" из 9букв, значит давалась только подсазка без вопроса
                        pass  # значит мы ничего не ищем по подсказке
                    else:
                        try:
                            q = q.split(" (", 1)[0]  # делим предложение на 2 части (разделитель,что в скобках). Оставляем 1 часть(то что до разделителя)
                            # раскомментить #print(q)
                            # print(len(q))
                            q = str(q)  # преобразовываем list в строку
                            q = q.replace(" ", "+")  # заменяем пробелы в строке на плюсы
                            # print(q)
                            zapros = base_url + maska + '&d' + 'ef=' + str(q)  # создаем url запроса состоящего из маски и определения слова
                            # print(zapros)
                            r = requests.get(zapros)  # делаем запрос в виде url + наш вопрос

                            soap = BeautifulSoup(r.text, "html.parser")  # парсим сайт который нам выдался по запросу

                            msgs = soap.h3.text  # выводим текст из первого блока с тегом h3, это и есть наш ответ
                            # print(msgs)


                            vk.messages.send(
                                # chat_id= event.chat_id,
                                chat_id=48,
                                message=msgs.lower(),
                                random_id=get_random_id(),
                            )
                            time.sleep(2)

                        except Exception:   #AttributeError
                            pass
                            #print("не найдено")

                else:
                    pass
    except Exception as e:
        print(str(e))