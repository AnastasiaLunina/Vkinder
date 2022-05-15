import logger
import vkapi
import vkbot
from vk_api.longpoll import VkEventType
import models
from models import Session, engine

# create a Session
session = Session()
connection = engine.connect()


def main():
    """
    Receives a message from the user and sends a response message.
    """
    vk_bot = vkbot.VKBot()
    vk_api = vkapi.VkApi()
    stack = []
    flag_favorite = False
    flag_black = False

    @logger.logger('log_file.txt')
    def get_user_for_bot(user_id):
        """
        Gets information about the user by his ID: city, sex, bdate.
        Checks if the user exists in the database, if not then adds.
        Gets vk user data by the specified parameters: city, gender, age.
        Returns information about user in following format:
        First name, Last name
        Profile link
        three photos as attachments, taken from method get_photos_from_profile()
        :param user_id: int
        :return: list
        """
        city, sex, bdate = vk_api.get_user_info(user_id)
        if models.check_if_bot_user_exists(user_id) is None:
            models.add_bot_user(user_id)
        return vk_api.search_user(city, sex, bdate)

    @logger.logger('log_file.txt')
    def add_user_to_db(bot_user_id, flag_list):
        """
        Adds user information to favorites or black list.
        flag_list True - adds user information to favorites list.
        flag_list False - adds user information to black list.
        :param bot_user_id: bot_user_id
        :param flag_list: Boolean
        :return: Boolean
        """
        nonlocal flag_favorite
        nonlocal flag_black
        if not stack or (flag_list and not flag_favorite):
            vk_bot.send_msg(event.user_id, "Добавлять некого")
            return False
        elif not stack or (not flag_list is None and not flag_black):
            vk_bot.send_msg(event.user_id, "Добавлять некого")
            return False
        first_name, last_name, url, user_attachment = stack.pop()
        vk_user_id = int(url.split('id')[1])
        if flag_list and models.check_if_match_exists(vk_user_id)[0] is None:
            print('1')
            flag_favorite = False
            models.add_new_match_to_favorites(vk_user_id, bot_user_id, first_name, last_name, url)
            models.add_photo_of_the_match(user_attachment, vk_user_id)
            return True
        elif not flag_list and models.check_if_match_exists(vk_user_id)[1] is None:
            print('2')
            flag_black = False
            models.add_new_match_to_black_list(vk_user_id, bot_user_id, first_name, last_name, url)
            models.add_photo_of_the_match(user_attachment, vk_user_id)
            return True
        return False

    for event in vk_bot.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                message = event.text.lower()
                if message == "привет":
                    vk_bot.send_msg(event.user_id, 'Привет, для начала работы нажми кнопку "Показать"')
                elif message == "список избранных":
                    for user in models.show_all_favorites(event.user_id):
                        msg = f'{user[0]} {user[1]}\n{user[2]}'
                        vk_bot.send_msg(event.user_id, message=msg, attachment=user[3])
                elif message == "черный список":
                    for user in models.show_all_blacklisted(event.user_id):
                        msg = f'{user[0]} {user[1]}\n{user[2]}'
                        vk_bot.send_msg(event.user_id, message=msg, attachment=user[3])
                elif message == "добавить в избранное":
                    add_user_to_db(event.user_id, True)
                elif message == "не нравится":
                    add_user_to_db(event.user_id, False)
                elif message == "показать":
                    data = get_user_for_bot(event.user_id)
                    msg = f'{data[0]} {data[1]}\n{data[2]}'
                    stack.append(data)
                    vk_bot.send_msg(event.user_id, message=msg, attachment=data[3])
                    flag_favorite, flag_black = True, True
                else:
                    vk_bot.send_msg(event.user_id, "К сожалению, такой команды я не знаю")

if __name__ == '__main__':
    main()
