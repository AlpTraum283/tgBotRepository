import config
import telebot
from PIL import Image

bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): 
    bot.send_message(message.chat.id, message.text)


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
    
    image = Image.open('image.jpg')
    rotated_image = image.rotate(90, expand = True)
    rotated_image.save('rotated_image.jpg', quality = 100)
    rtrn_image = open('rotated_image.jpg', 'rb')
    bot.send_photo(message.chat.id, rtrn_image)

if __name__ == '__main__':
	bot.polling(none_stop=True)


file_id = 'AAAaaaZZZzzz'
tb.send_photo(chat_id, file_id)