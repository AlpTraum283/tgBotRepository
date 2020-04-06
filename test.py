import config
import functions
import telebot
from telebot import types

bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=['photo'])
def photo(message):
   # print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
   # print('fileID =', fileID)
    file_info = bot.get_file(fileID)
   # print('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    
    markup = types.ReplyKeyboardMarkup()
    buttons = functions.btnList.keys()
    markup.row(*buttons)
    bot.send_message(message.chat.id, "Выберите, что сделать с фото", reply_markup=markup)

@bot.message_handler(content_types=["text"])
def editImage(message): 
    functionName = functions.btnList.get(message.text, "")
    fileName = getattr(functions, functionName)()
    rtrn_image = open(fileName, 'rb')
    bot.send_photo(message.chat.id, rtrn_image)
    # bot.send_message(message.chat.id, functionName)

if __name__ == '__main__':
	bot.polling(none_stop=True)


# file_id = 'AAAaaaZZZzzz'
# tb.send_photo(chat_id, file_id)