import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll
import config
from vk_api.utils import get_random_id


class VKBot:
    """
    Creates a class to work with chatbot VK
    """

    def __init__(self):
        self.token = config.token_vkinder
        self.vk_session = vk_api.VkApi(token=self.token)
        self.longpoll = VkLongPoll(self.vk_session)
        self.keyboard = self.current_keyboard()

    def send_msg(self, user_id, message, attachment=None):
        """
        Sends a new message to the user in the chat.
        :param user_id: int
        :param message: string
        :param attachment: string
        """
        self.vk_session.method('messages.send',
                               {'user_id': user_id,
                                'message': message,
                                'random_id': get_random_id(),
                                'keyboard': self.keyboard,
                                'attachment': attachment})

    @staticmethod
    def current_keyboard():
        """
        Creates a keyboard to interact with the chatbot.
        :return Keyboard JSON-object
        """
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Показать', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button('Добавить в избранное', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Не нравится', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_line()
        keyboard.add_button('Список избранных', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Черный список', color=VkKeyboardColor.SECONDARY)
        return keyboard.get_keyboard()
