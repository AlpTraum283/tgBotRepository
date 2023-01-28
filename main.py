import config 
import functions
import telebot
from telebot import types
import os
import sqlite3

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "Для начала работы со мной достаточно отправить мне изображение.")
    global handling
    handling = 0
    chat_ID = message.chat.id
    conn = sqlite3.connect("mydb") 
    cursor = conn.cursor()
    string = "INSERT INTO sub_list (chat_id, subscribe) VALUES ({}, 'yes')".format(chat_ID)
    try:
        cursor.execute(string)
    except:
        print('Во время вставки записи что-то пошло не так, пользователь с id {} уже существует'.format(chat_ID))
    conn.commit()
    conn.close()

@bot.message_handler(commands=['hello'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Привет, это ImageEditBot, который может помочь с обработкой твоих изображений!")


@bot.message_handler(commands=['subscribe'])
def send_about(message):
    subKb = types.InlineKeyboardMarkup(row_width=2)
    for i in range(0, len(functions.subButtonList)):
        subKb.add( types.InlineKeyboardButton( functions.subButtonList [i], callback_data=functions.subButtonList [i] ) )

    bot.send_message(message.chat.id, "После приобретения подписки вы сможете пользоваться дополнительными функциями. Стоимость подписки - 50 руб.", reply_markup=subKb)


@bot.message_handler(content_types=['photo'])
def photo(message):
    global handling
    handling = 0
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)

    chat_ID = message.chat.id
    image_name = (str(chat_ID) + ".jpg") 

    with open(image_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    inlineKb = types.InlineKeyboardMarkup(row_width=2)
    for i in range(0, len(functions.buttonNameList)):
        inlineKb.add( types.InlineKeyboardButton( functions.buttonNameList[i], callback_data=functions.buttonNameList[i] ) )

    bot.send_message(message.chat.id, "Выберите, что сделать с фото", reply_markup=inlineKb)

@bot.callback_query_handler(lambda query: query.data in functions.buttonNameList)
def process_callback_1(query):
    try:
        global handling
        chat_ID = query.message.chat.id
        image_name = (str(chat_ID) + ".jpg")
        changedImageName = ('changed_' + str(chat_ID) + '.jpg')
        inlineKb = types.InlineKeyboardMarkup(row_width=2)

        if query.data == 'Поворот':
                degreeKb = types.InlineKeyboardMarkup(row_width=2)
                for i in range(0, len(functions.buttonNameDegreeList)):
                    degreeKb.add( types.InlineKeyboardButton( functions.buttonNameDegreeList[i], callback_data=functions.buttonNameDegreeList[i] ) )
                bot.send_message(chat_ID, 'Выберите, на сколько градусов повернуть', reply_markup=degreeKb)

        elif query.data == 'Размытие':
            if handling == 0:
                changedImage = functions.imageBlurFilter(image_name, chat_ID)    
                rtrn_image = open(changedImage, 'rb')
                bot.send_photo(chat_ID, rtrn_image)
                for i in range(0, len(functions.buttonNameList)):
                    inlineKb.add( types.InlineKeyboardButton( functions.buttonNameList[i], callback_data=functions.buttonNameList[i] ) )

                bot.send_message(chat_ID, 'Выберите дальнейшее действие', reply_markup=inlineKb)
                rtrn_image.close()
                handling+=1

            else: 
                changedImage = functions.imageBlurFilter(changedImageName, chat_ID)    
                rtrn_image = open(changedImage, 'rb')
                bot.send_photo(chat_ID, rtrn_image)
                for i in range(0, len(functions.buttonNameList)):
                    inlineKb.add( types.InlineKeyboardButton( functions.buttonNameList[i], callback_data=functions.buttonNameList[i] ) )

                bot.send_message(chat_ID, 'Выберите дальнейшее действие', reply_markup=inlineKb)
                rtrn_image.close()

        elif query.data == 'Обвод по контуру':
            if handling == 0:
                changedImage = functions.imageContourFilter(image_name, chat_ID)    
                rtrn_image = open(changedImage, 'rb')
                bot.send_photo(chat_ID, rtrn_image)
                for i in range(0, len(functions.buttonNameList)):
                    inlineKb.add( types.InlineKeyboardButton( functions.buttonNameList[i], callback_data=functions.buttonNameList[i] ) )

                bot.send_message(chat_ID, 'Выберите дальнейшее действие', reply_markup=inlineKb)
                rtrn_image.close()
                handling+=1

            else:
                changedImage = functions.imageContourFilter(changedImageName, chat_ID)    
                rtrn_image = open(changedImage, 'rb')
                bot.send_photo(chat_ID, rtrn_image)
                for i in range(0, len(functions.buttonNameList)):
                    inlineKb.add( types.InlineKeyboardButton( functions.buttonNameList[i], callback_data=functions.buttonNameList[i] ) )

                bot.send_message(chat_ID, 'Выберите дальнейшее действие', reply_markup=inlineKb)
                rtrn_image.close()

        elif query.data == 'Применить маску':
            conn = sqlite3.connect("mydb") 
            cursor = conn.cursor()
            string = "Select subscribe from sub_list where chat_id = {}".format(chat_ID)
            try:
                cursor.execute(string)
            except:
                print('Во время выборки что-то пошло не так, пользователя с id {} не существует'.format(chat_ID))
                print('user with id {} does not exist'.format(chat_ID))
            conn.commit()
            rows = cursor.fetchall()
            for row in rows:
                print(row[0])
            if 'no' in row:
                bot.answer_callback_query(callback_query_id=query.id, text="Выбранная функция доступна только обладателям подписки.", show_alert=False)
            elif 'yes' in row:
                filterKb = types.InlineKeyboardMarkup(row_width=2)
                for i in range(0, len(functions.buttonFilterNameList)):
                    filterKb.add( types.InlineKeyboardButton( functions.buttonFilterNameList[i], callback_data=functions.buttonFilterNameList[i] ) )
                bot.send_message(chat_ID, 'Выберите маску', reply_markup=filterKb)   
        elif query.data == 'Чёрно-белое':
            if handling == 0:
                image_name = (str(chat_ID) + ".jpg")
                changedImage = functions.imageBWFilter(image_name, chat_ID)    
                rtrn_image = open(changedImage, 'rb')
                bot.send_photo(chat_ID, rtrn_image)
                for i in range(0, len(functions.buttonNameList)):
                    inlineKb.add( types.InlineKeyboardButton( functions.buttonNameList[i], callback_data=functions.buttonNameList[i] ) )

                bot.send_message(chat_ID, 'Выберите дальнейшее действие', reply_markup=inlineKb)
                rtrn_image.close()
                handling+=1

            else:
                image_name = (str(chat_ID) + ".jpg")
                changedImage = functions.imageBWFilter(changedImageName, chat_ID)    
                rtrn_image = open(changedImage, 'rb')
                bot.send_photo(chat_ID, rtrn_image)
                for i in range(0, len(functions.buttonNameList)):
                    inlineKb.add( types.InlineKeyboardButton( functions.buttonNameList[i], callback_data=functions.buttonNameList[i] ) )

                bot.send_message(chat_ID, 'Выберите дальнейшее действие', reply_markup=inlineKb)
                rtrn_image.close()

        elif query.data == 'Закончить обработку':
            os.remove(image_name)
            os.remove(changedImageName)
    except:
        print('Что-то пошло не так во время применения основных функций')

@bot.callback_query_handler(lambda degree: degree.data in functions.buttonNameDegreeList)
def rotateImage(degree):
    try:
        global handling
        chat_ID = degree.message.chat.id
        image_name = (str(chat_ID) + ".jpg")
        changedImageName = ('changed_' + str(chat_ID) + '.jpg')
        if degree.data == '90° влево':
            if handling == 0:
                changedImage = functions.imageRotateLeft(image_name, chat_ID, 90)
                rtrn_image = open(changedImage, 'rb')
                bot.send_photo(chat_ID, rtrn_image)
                inlineKb = types.InlineKeyboardMarkup(row_width=2)
                for i in range(0, len(functions.buttonNameList)):
                    inlineKb.add( types.InlineKeyboardButton( functions.buttonNameList[i], callback_data=functions.buttonNameList[i] ) )

                bot.send_message(chat_ID, 'Выберите дальнейшее действие', reply_markup=inlineKb)
                rtrn_image.close()
                handling+=1

            else:
                changedImage = functions.imageRotateLeft(changedImageName, chat_ID, 90)
                rtrn_image = open(changedImage, 'rb')
                bot.send_photo(chat_ID, rtrn_image)
                inlineKb = types.InlineKeyboardMarkup(row_width=2)
                for i in range(0, len(functions.buttonNameList)):
                    inlineKb.add( types.InlineKeyboardButton( functions.buttonNameList[i], callback_data=functions.buttonNameList[i] ) )

                bot.send_message(chat_ID, 'Выберите дальнейшее действие', reply_markup=inlineKb)
                rtrn_image.close()

        elif degree.data == '90° вправо':
            if handling == 0:
                changedImage = functions.imageRotateLeft(image_name, chat_ID, 270)
                rtrn_image = open(changedImage, 'rb')
                bot.send_photo(chat_ID, rtrn_image)
                inlineKb = types.InlineKeyboardMarkup(row_width=2)
                for i in range(0, len(functions.buttonNameList)):
                    inlineKb.add( types.InlineKeyboardButton( functions.buttonNameList[i], callback_data=functions.buttonNameList[i] ) )

                bot.send_message(chat_ID, 'Выберите дальнейшее действие', reply_markup=inlineKb)
                rtrn_image.close()
                handling+=1

            else:
                changedImage = functions.imageRotateLeft(changedImageName, chat_ID, 270)
                rtrn_image = open(changedImage, 'rb')
                bot.send_photo(chat_ID, rtrn_image)
                inlineKb = types.InlineKeyboardMarkup(row_width=2)
                for i in range(0, len(functions.buttonNameList)):
                    inlineKb.add( types.InlineKeyboardButton( functions.buttonNameList[i], callback_data=functions.buttonNameList[i] ) )

                bot.send_message(chat_ID, 'Выберите дальнейшее действие', reply_markup=inlineKb)
                rtrn_image.close()
    except:
        print('Что-то пошло не так во время поворота')

@bot.callback_query_handler(lambda sub: sub.data in functions.subButtonList)
def process_callback_1(sub):
    try:
        chat_ID = sub.message.chat.id
        if sub.data == 'Подписаться':

            conn = sqlite3.connect("mydb") # или :memory: чтобы сохранить в RAM
            cursor = conn.cursor()
            string = "Update sub_list set subscribe = 'yes' where chat_id = {}".format(chat_ID)
            try:
            # Вставляем данные в таблицу
                cursor.execute(string)
            except:
                print('Во время вставки записи что-то пошло не так, пользователь с id {} уже существует'.format(chat_ID))
                print('Something went wrong, user with id {} already exists'.format(chat_ID))
            # Сохраняем изменения
            conn.commit()
            bot.send_message(sub.message.chat.id, "Для получения подписки переведите 50 рублей на счет 410013478692822 Яндекс.Деньги с указанием вашего chat_id. Ваш chat_id - {}. Администратор добавит Вас в список подписчиков.".format(chat_ID))
        elif sub.data == 'Позже': 
            bot.send_message(sub.message.chat.id, "Для начала работы со мной достаточно отправить мне изображение.")
    except:
        print('Что-то пошло не так во применения подписки')

@bot.callback_query_handler(lambda Filter: Filter.data in functions.buttonFilterNameList)
def rotateImage(Filter):
    try:
        chat_ID = Filter.message.chat.id
        image_name = (str(chat_ID) + ".jpg")
        changedImageName = ('changed_' + str(chat_ID) + '.jpg')
        if Filter.data == 'Маска кошки':
            changedImage = functions.drawCatMask(image_name,chat_ID)
            if changedImage == 'Ошибка. На изображении не найдено лиц.':
                bot.send_message(chat_ID, changedImage)
            else:
                rtrn_image = open(changedImage, 'rb')
                bot.send_photo(chat_ID, rtrn_image)
                inlineKb = types.InlineKeyboardMarkup(row_width=2)
                for i in range(0, len(functions.buttonNameList)):
                    inlineKb.add( types.InlineKeyboardButton( functions.buttonNameList[i], callback_data=functions.buttonNameList[i] ) )

                bot.send_message(chat_ID, 'Выберите дальнейшее действие', reply_markup=inlineKb)
        elif Filter.data == 'Маска собаки':
            changedImage = functions.drawDogMask(image_name,chat_ID)
            if changedImage == 'Ошибка. На изображении не найдено лиц.':
                bot.send_message(chat_ID, changedImage)
            else:
                rtrn_image = open(changedImage, 'rb')
                bot.send_photo(chat_ID, rtrn_image)
                inlineKb = types.InlineKeyboardMarkup(row_width=2)
                for i in range(0, len(functions.buttonNameList)):
                    inlineKb.add( types.InlineKeyboardButton( functions.buttonNameList[i], callback_data=functions.buttonNameList[i] ) )

                bot.send_message(chat_ID, 'Выберите дальнейшее действие', reply_markup=inlineKb)
        elif Filter.data == 'Маска лисы':
            changedImage = functions.drawFoxMask(image_name,chat_ID)
            if changedImage == 'Ошибка. На изображении не найдено лиц.':
                bot.send_message(chat_ID, changedImage)
            else:
                rtrn_image = open(changedImage, 'rb')
                bot.send_photo(chat_ID, rtrn_image)
                inlineKb = types.InlineKeyboardMarkup(row_width=2)
                for i in range(0, len(functions.buttonNameList)):
                    inlineKb.add( types.InlineKeyboardButton( functions.buttonNameList[i], callback_data=functions.buttonNameList[i] ) )

                bot.send_message(chat_ID, 'Выберите дальнейшее действие', reply_markup=inlineKb)
    except:
        print('Что-то пошло не так во время применения маски')

if __name__ == '__main__':
    global handling 
    handling = 0
    bot.polling(none_stop=True)
