import config
import functions
import telebot
from telebot import types
import os
import time

bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=['photo'])
def photo(message):
   # print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
   # print('fileID =', fileID)
    file_info = bot.get_file(fileID)
   # print('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)

    chat_ID = message.chat.id
    #print(chat_ID)
    # image_name - переменная, в которой хранится имя для изображения, включая id чата
    image_name = (str(chat_ID) + ".jpg") 
    #print(image_name)

    with open(image_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    markup = types.ReplyKeyboardMarkup()
    buttons = functions.btnList.keys()
    markup.row(*buttons)
    bot.send_message(message.chat.id, "Выберите, что сделать с фото", reply_markup=markup)

@bot.message_handler(content_types=["text"])
def editImage(message): 
    chat_ID = message.chat.id
    image_name = (str(chat_ID) + ".jpg")
     
    functionName = functions.btnList.get(message.text, "")
    fileName = getattr(functions, functionName)(image_name, chat_ID)
    rtrn_image = open(fileName, 'rb')
    bot.send_photo(message.chat.id, rtrn_image)
    # bot.send_message(message.chat.id, functionName)

    #time.sleep(5)
    # Блок закрытия всех открытых ранее изображений
    rtrn_image.close()

    # Блок удаления изображений, исходника и обработанного
    os.remove(image_name)
    os.remove(fileName)

if __name__ == '__main__':
	bot.polling(none_stop=True)


# file_id = 'AAAaaaZZZzzz'
# tb.send_photo(chat_id, file_id)