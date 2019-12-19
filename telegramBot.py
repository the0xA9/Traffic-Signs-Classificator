from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from predict import makePrediction
from tensorflow.keras.models import load_model

BOT_TOKEN = "1017748021:AAEbcprwYlWcabv-4jN4LKMYqvtZb-oX_Uo"

# load the traffic sign recognizer model
model = load_model("trafficsignnet.model")

class TelegramBot:
    def __init__(self):
        self.updater = Updater(token=BOT_TOKEN)

        self.bot_url = 'https://t.me/trafficSignRecognitionBot'
        self.updater.dispatcher.add_handler(CommandHandler('start', self.new_chat_user))
        self.updater.dispatcher.add_handler(CommandHandler('help', self.help_message))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.photo, self.photo_handler))

    @staticmethod
    def get_bot_commands():
        return {'/start': 'Begin your chat', '/help': 'List of bot commands'}

    def start_bot(self):
        self.updater.start_polling()

    def help_message(self, bot, update):
        chat_id = update.message.chat_id
        command = self.get_bot_commands()
        message = ''
        for key in command.keys():
            message += "{0} - {1}\n".format(key, command[key])
        bot.sendMessage(chat_id=chat_id, text=message)

    def new_chat_user(self, bot, update):
        chat_id = update.message.chat_id
        message = update.message.text.split('/start ', 1)
        bot.sendMessage(chat_id=chat_id, text="Please, try again later")

    def photo_handler(self, bot, update):
        file = bot.getFile(update.message.photo[-1].file_id)
        print ("file_id: " + str(update.message.photo[-1].file_id))
        file.download('image/image.jpg')
        detectedSign = makePrediction(model).split(",")
        chat_id = update.message.chat_id
        retMsg = "Sign \"" + detectedSign[1] + "\" detected\nSignID: " + detectedSign[2]
        bot.sendMessage(chat_id=chat_id, text=retMsg)

if __name__ == '__main__':
    bot = TelegramBot()
    bot.start_bot()


