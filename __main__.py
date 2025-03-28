import os
import logging
import time
import telebot
from telebot import types

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Получение токена из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    logger.error('Не задан BOT_TOKEN в переменных окружения!')
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

# База данных вопросов
questions = {
    "дошкольный и начальная школа": {
        "лёгкий": [
            {
                "question": "Где нельзя находиться в наушниках?",
                "options": ["В машине", "Вблизи ж/д путей", "На природе", "Дома"],
                "correct_answer": "Вблизи ж/д путей"
            },
            {
                "question": "Что нельзя делать в железнодорожном транспорте?",
                "options": ["Спать", "Играть в карты", "Высовываться из окна"],
                "correct_answer": "Высовываться из окна"
            },
            {
                "question": "Что делать, если вы потерялись на вокзале?",
                "options": ["Обратиться к прохожему за помощью", "Ждать, когда придёт помощь",
                            "Обратиться к работнику вокзала или полицейскому", "Самому искать родителей"],
                "correct_answer": "Обратиться к работнику вокзала или полицейскому"
            }
        ],
        "средний": [
            {
                "question": "Что из данных утверждений НЕЛЬЗЯ делать на ж/д путях или в железнодорожном транспорте?",
                "options": ["Есть на платформе в ожидании поезда", "Открывать окно в вагоне",
                            "Слушать музыку или смотреть в телефон вблизи железнодорожных путей",
                            "Ждать поезд за ограничительной линией, держась ближе к центру платформы"],
                "correct_answer": "Слушать музыку или смотреть в телефон вблизи железнодорожных путей"
            },
            {
                "question": "В какие игры можно играть возле поездов?",
                "options": ["Во все, это же весело", "В подвижные игры(футбол, прятки, догонялки)",
                            "Не играть в игры вообще", "В неподвижные игры(слова, города, ассоциации)"],
                "correct_answer": "В неподвижные игры(слова, города, ассоциации)"
            },
            {
                "question": "Где должен находиться пассажир, передвигаясь на железнодорожном транспорте?",
                "options": ["В вагоне", "На подножках в переходных площадках вагонов", "На крыше вагона",
                            "Цепляться за движущийся железнодорожный состав, маневренные тепловозы и другие подвижные составы"],
                "correct_answer": "В вагоне"
            }
        ],
        "сложный": [
            {
                "question": "Какая железная дорога считается первой?",
                "options": ["Московская", "Царскосельская", "Дальневосточная", "Забайкальская"],
                "correct_answer": "Царскосельская"
            }
        ]
    },
    "средняя школа": {
        "лёгкий": [
            {
                "question": "Какое напряжение в проводах контактной сети на железной дороге?",
                "options": ["10 тысяч вольт", "220 вольт", "600 вольт", "27 тысяч вольт"],
                "correct_answer": "27 тысяч вольт"
            },
            {
                "question": "Твои друзья решили развлечься, разрисовать вагоны поезда и положить камни на рельсы, что будешь делать?",
                "options": ["Пойду с ними и постою рядом", "Сделаю тоже, что и они, мы же друзья",
                            "Сделаю вид, что не слышал об этом", "Сделаю замечание и расскажу взрослым"],
                "correct_answer": "Сделаю замечание и расскажу взрослым"
            },
            {
                "question": "Что делать, если торопишься на важное мероприятие и нужно перейти ж/д пути?",
                "options": ["Перейду там, где считаю безопасным", "Посмотрю, что нет поездов и перейду по путям",
                            "Найду ближайший пешеходный настил, мост или виадук",
                            "Попрошу взрослого перевести меня через пути"],
                "correct_answer": "Попрошу взрослого перевести меня через пути"
            }
        ],
        "средний": [
            {
                "question": "Что делать, если вы оказались между двух движущихся поездов?",
                "options": ["Встать ровно, спиной к одному составу и лицом к другому, ждать, когда они проедут",
                            "Бежать в направлении большего поезда", "Лечь на землю на одинаковом расстоянии от поездов",
                            "Звать на помощь"],
                "correct_answer": "Лечь на землю на одинаковом расстоянии от поездов"
            },
            {
                "question": "Для чего нужен стоп-кран?",
                "options": ["Для экстренной остановки поезда", "Для управления поездом",
                            "Для того, чтобы остановить поезд на нужной остановке",
                            "Для того, чтобы вызвать проводника"],
                "correct_answer": "Для экстренной остановки поезда"
            },
            {
                "question": "Что делать, если вы увидели оголённый провод?",
                "options": ["Подойти, посмотреть и сообщить взрослым", "Потрогать и проверить есть ли электричество",
                            "Не подходить ближе, чем на 8 метров и сообщить взрослым", "Оставить его так"],
                "correct_answer": "Не подходить ближе, чем на 8 метров и сообщить взрослым"
            }
        ],
        "сложный": [
            {
                "question": "Что делать, если вы приехали на маленький остановочный пункт, где нет пешеходного настила, виадука и подземного перехода. Вам нужно пересечь железнодорожные пути. Как вы будете это делать?",
                "options": [
                    "Пройду по насыпи вдоль железнодорожных путей до удобного на мой взгляд места и там пересеку железную дорогу",
                    "Пересеку железнодорожные пути под прямым углом и отправлюсь дальше", "Выкопаю подземный переход",
                    "Не буду пересекать железнодорожные пути"],
                "correct_answer": "Пересеку железнодорожные пути под прямым углом и отправлюсь дальше"
            }
        ]
    }
}

user_states = {}


def create_keyboard(options):
    """Создает Reply клавиатуру с указанными вариантами"""
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
    for option in options:
        keyboard.add(option)
    return keyboard


@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    """Обработчик команд /start и /help"""
    try:
        user_id = message.chat.id
        user_states[user_id] = {}
        markup = create_keyboard(["дошкольный и начальная школа", "средняя школа"])
        bot.send_message(user_id, "Добро пожаловать! Выберите возрастную категорию:", reply_markup=markup)
        bot.register_next_step_handler(message, process_age)
        logger.info(f"Новый пользователь {user_id} начал опрос")
    except Exception as e:
        logger.error(f"Ошибка в handle_start: {e}")
        bot.reply_to(message, "⚠️ Произошла ошибка. Пожалуйста, попробуйте снова командой /start")


def process_age(message):
    """Обработка выбора возрастной категории"""
    try:
        user_id = message.chat.id
        age = message.text

        if age not in questions:
            bot.send_message(user_id, "Пожалуйста, выберите вариант из предложенных:")
            return handle_start(message)

        user_states[user_id]['age'] = age
        markup = create_keyboard(["лёгкий", "средний", "сложный"])
        bot.send_message(user_id, "Выберите уровень сложности:", reply_markup=markup)
        bot.register_next_step_handler(message, process_level)
        logger.info(f"Пользователь {user_id} выбрал возраст: {age}")
    except Exception as e:
        logger.error(f"Ошибка в process_age: {e}")
        bot.reply_to(message, "⚠️ Ошибка выбора возраста. Попробуйте снова /start")


def process_level(message):
    """Обработка выбора уровня сложности"""
    try:
        user_id = message.chat.id
        level = message.text

        if level not in ["лёгкий", "средний", "сложный"]:
            bot.send_message(user_id, "Пожалуйста, выберите вариант из предложенных:")
            return process_age(message)

        user_states[user_id]['level'] = level
        user_states[user_id]['question_index'] = 0
        ask_question(message)
        logger.info(f"Пользователь {user_id} выбрал уровень: {level}")
    except Exception as e:
        logger.error(f"Ошибка в process_level: {e}")
        bot.reply_to(message, "⚠️ Ошибка выбора уровня. Попробуйте снова /start")


def ask_question(message):
    """Задает следующий вопрос пользователю"""
    try:
        user_id = message.chat.id
        age = user_states[user_id]['age']
        level = user_states[user_id]['level']
        question_index = user_states[user_id]['question_index']

        if question_index < len(questions[age][level]):
            question_data = questions[age][level][question_index]
            question_text = question_data["question"]
            options = question_data["options"]

            markup = create_keyboard(options)
            bot.send_message(user_id, question_text, reply_markup=markup)
            bot.register_next_step_handler(message, process_answer)
            logger.info(f"Пользователю {user_id} задан вопрос {question_index + 1}/{len(questions[age][level])}")
        else:
            bot.send_message(
                user_id,
                "🎉 Вы ответили на все вопросы этого уровня!",
                reply_markup=types.ReplyKeyboardRemove()
            )
            logger.info(f"Пользователь {user_id} завершил опрос уровня {level}")
    except Exception as e:
        logger.error(f"Ошибка в ask_question: {e}")
        bot.reply_to(message, "⚠️ Ошибка при получении вопроса. Попробуйте снова /start")


def process_answer(message):
    """Обрабатывает ответ пользователя"""
    try:
        user_id = message.chat.id
        user_answer = message.text
        age = user_states[user_id]['age']
        level = user_states[user_id]['level']
        question_index = user_states[user_id]['question_index']

        question_data = questions[age][level][question_index]
        correct_answer = question_data["correct_answer"]

        if user_answer == correct_answer:
            reply_text = "✅ Правильно! " + correct_answer
        else:
            reply_text = f"❌ Неверно. Правильный ответ: {correct_answer}"

        bot.send_message(
            user_id,
            reply_text,
            reply_markup=types.ReplyKeyboardRemove()
        )

        user_states[user_id]['question_index'] += 1
        time.sleep(1)  # Пауза перед следующим вопросом
        ask_question(message)
        logger.info(
            f"Пользователь {user_id} ответил на вопрос {question_index + 1}: {'верно' if user_answer == correct_answer else 'неверно'}")
    except Exception as e:
        logger.error(f"Ошибка в process_answer: {e}")
        bot.reply_to(message, "⚠️ Ошибка обработки ответа. Попробуйте снова /start")


def run_bot():
    """Запускает бота с обработкой ошибок и автоматическим перезапуском"""
    logger.info("Запуск Telegram бота...")
    while True:
        try:
            bot.infinity_polling()
        except telebot.apihelper.ApiTelegramException as e:
            if "Conflict" in str(e):
                logger.error("Обнаружен конфликт: другой экземпляр бота уже запущен")
            else:
                logger.error(f"Ошибка API Telegram: {e}")
            time.sleep(10)
        except Exception as e:
            logger.error(f"Критическая ошибка: {e}\nПерезапуск через 5 секунд...")
            time.sleep(5)
        finally:
            logger.info("Перезапуск бота...")


if __name__ == '__main__':
    try:
        logger.info("Инициализация бота...")
        run_bot()
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.critical(f"Фатальная ошибка: {e}")