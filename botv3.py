# Imports Bot
from multiprocessing.connection import wait
from ntpath import join
import telebot
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import threading
from datetime import datetime


# Datos
token_bot = '5553840811:AAEarEj-qTKDftl96Dn3AXBEeDwAOOueKwA'
chat_id_mzarzu = 820291613
usuario = "zarzuelomario@gmail.com"
contrasenia = "150599"
delay_notif_auto = 3*3600
delay_notif_auto_overdue = 12*3600
delay_notif_auto_weekly = 24*3600
flag_daily = 1
flag_overdue = 1
flag_weekly = 1
funcion_hoy = "function getHoy(){let task_hoy = [];for (let x of document.querySelector('#app > div.v-application--wrap > main > div > div > div.layout.pt-3.justify-space-around > div.dashboard-column.mt-12 > div.day.js-day.dashboard-item').getElementsByClassName('title-input js-title-input')) {task_hoy.push(x._value)}return JSON.stringify(task_hoy);} return getHoy()"
funcion_overdue = "function getOverdue(){let task_overdue = [];for (let x of document.querySelector('#app > div.v-application--wrap > main > div > div > div.layout.pt-3.justify-space-around > div.dashboard-column.mt-12 > div.day.dashboard-item.mb-5').getElementsByClassName('title-input js-title-input')) {task_overdue.push(x._value)}return JSON.stringify(task_overdue);} return getOverdue()"
funcion_week = "function getWeek(){let task_week = [];for (let x of document.querySelector('#app > div.v-application--wrap > main > div > div > div.layout.pt-3.justify-space-around > div:nth-child(1) > div > div.week.js-week > div.mt-2.mb-6').getElementsByClassName('title-input js-title-input')) {task_week.push(x._value)}return JSON.stringify(task_week);} return getWeek()"


# Inicia el bot
bot = telebot.TeleBot(token_bot)


########## FUNCIONES INTERNAS ##########################################################################################################
# Bucle infinito que comprueba si hay mensajes nuevos
def recibir_mensajes():
    bot.infinity_polling()


########## SCRAP #######################################################################################################################
# Funcion que hace el scrap
def ObtenerDatos(funcion):
    # Abrimos navegador
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://journal.bulletjournal.app/dashboard')
    time.sleep(1)

    # Iniciamos sesion
    mBox = driver.find_element("xpath", '//*[@id="input-22"]')
    mBox.send_keys(usuario)  # pone usuario

    mBox = driver.find_element("xpath", '//*[@id="input-25"]')
    mBox.send_keys(contrasenia)  # pone contraseña

    driver.find_element(
        "xpath", '/html/body/div/div/main/div/div/div/div[2]/form/button').click()  # click al login
    time.sleep(5)

    # Obtenemos elementos
    elementos_raw = driver.execute_script(funcion)
    elementos_json = json.loads(elementos_raw)
    return elementos_json


########## COMANDOS DEL BOT ############################################################################################################

# Comando de inicio del bot
@bot.message_handler(commands=['start'])
def cmd_start(message):
    if message.from_user.id == chat_id_mzarzu:
        mensaje = "Bot de recordatorios iniciado"
        bot.reply_to(message, mensaje)
    else:
        print(message.from_user.id, message.from_user.username,
              message.from_user.first_name, message.from_user.last_name)


# Comando de ayuda del bot
@bot.message_handler(commands=['ayuda', 'help'])
def cmd_start(message):
    if message.from_user.id == chat_id_mzarzu:
        mensaje = "Bot de recordatorios de tareas de Bullet time.\nEn el menu tienes disponibles los comandos con sus descripciones"
        bot.reply_to(message, mensaje)
    else:
        print(message.from_user.id, message.from_user.username,
              message.from_user.first_name, message.from_user.last_name)


# Comando para mostrar tareas pendientes de hoy
@bot.message_handler(commands=['to_do'])
def cmd_getToDo(message):
    if message.from_user.id == chat_id_mzarzu:
        bot.send_chat_action(message.chat.id, "typing")
        tareas = ObtenerDatos(funcion_hoy)
        print(tareas)
        # Si hay elementos en la lista de tareas, los formatea
        if tareas != []:
            tareas_str = ''
            for x in tareas:
                tareas_str += '\t'
                tareas_str += x
                tareas_str += '\n'

            bot.send_message(message.chat.id, 'DAILY LOG\n' + tareas_str)
        else:
            bot.send_message(
                message.chat.id, "No hay más tareas que hacer por hoy.\nComprueba la App para ver las tareas atrasadas :)")
    else:
        print(message.from_user.id, message.from_user.username,
              message.from_user.first_name, message.from_user.last_name)


# Comando para mostrar tareas pasadas
@bot.message_handler(commands=['overdue'])
def cmd_getOverdue(message):
    if message.from_user.id == chat_id_mzarzu:
        bot.send_chat_action(message.chat.id, "typing")
        tareas = ObtenerDatos(funcion_overdue)
        print(tareas)
        # Si hay elementos en la lista de tareas, los formatea
        if tareas != []:
            tareas_str = ''
            for x in tareas:
                tareas_str += '\t'
                tareas_str += x
                tareas_str += '\n'

            bot.send_message(message.chat.id, 'OVERDUE TASKS\n' + tareas_str)
        else:
            bot.send_message(
                message.chat.id, "No hay más tareas que hacer por hoy.\nComprueba la App para ver las tareas atrasadas :)")
    else:
        print(message.from_user.id, message.from_user.username,
              message.from_user.first_name, message.from_user.last_name)


# Comando para mostrar tareas semanales
@bot.message_handler(commands=['week'])
def cmd_getWeek(message):
    if message.from_user.id == chat_id_mzarzu:
        bot.send_chat_action(message.chat.id, "typing")
        tareas = ObtenerDatos(funcion_week)
        print(tareas)
        # Si hay elementos en la lista de tareas, los formatea
        if tareas != []:
            tareas_str = ''
            for x in tareas:
                tareas_str += '\t'
                tareas_str += x
                tareas_str += '\n'

            bot.send_message(message.chat.id, 'WEEKLY TASKS\n' + tareas_str)
        else:
            bot.send_message(
                message.chat.id, "No hay más tareas que hacer por hoy.\nComprueba la App para ver las tareas atrasadas :)")
    else:
        print(message.from_user.id, message.from_user.username,
              message.from_user.first_name, message.from_user.last_name)


# Funcion del hilo del bucle de notificaciones automaticas diarias
def notif_auto(mensaje):
    global delay_notif_auto
    global flag_daily
    global fecha_auto_daily
    #now = datetime.now() 
    #if now + delay_notif_auto 
    while (True):
        if flag_daily == 0: 
            now = datetime.now()
            if  now.hour >= 8 and now.hour <= 23:
                cmd_getToDo(mensaje)
                time.sleep(delay_notif_auto)
            else:
                time.sleep((fecha_auto_daily.hour-now.hour)*3600 + (fecha_auto_daily.minute-now.minute)*60)                         
        else:
            break
    print("Hilo diario muerto.\n")

# Comando para mostrar tareas pendientes de hoy AUTOMATICAMENTE


@bot.message_handler(commands=['start_auto'])
def notif_auto_bot(message):
    # Hace que solo mzarzu pueda activar las notificaciones automaticas
    if message.from_user.id == chat_id_mzarzu:
        global flag_daily
        global fecha_auto_daily 
        fecha_auto_daily = datetime.fromtimestamp(message.date)
        if flag_daily != 0:
            flag_daily = 0
            hilo_notif_hoy = threading.Thread(
                name="hilo_notif_hoy", target=notif_auto, args=[message])
            hilo_notif_hoy.start()
            print("Notificaciones automaticas activadas")
            bot.send_message(
                message.chat.id, "Notificaciones automaticas de diarias activadas")
        else:
            print("Las notificaciones automáticas ya están activas.")
            bot.send_message(
                message.chat.id, "Las notificaciones automáticas ya están activas.")
    else:
        print(message.from_user.id, message.from_user.username,
              message.from_user.first_name, message.from_user.last_name)


# Funcion del hilo del bucle de notificaciones automaticas overdues
def notif_auto_overdue(mensaje):
    global delay_notif_auto_overdue
    global flag_overdue
    while (True):
        time.sleep(delay_notif_auto_overdue)
        if flag_overdue == 0:
            cmd_getOverdue(mensaje)
        else:
            break
    print("Hilo overdue muerto.\n")


# Comando para mostrar tareas pendientes overdues AUTOMATICAMENTE
@bot.message_handler(commands=['start_auto_overdue'])
def notif_auto__overdue_bot(message):
    # Hace que solo mzarzu pueda activar las notificaciones automaticas
    if message.from_user.id == chat_id_mzarzu:
        global flag_overdue
        if flag_overdue != 0:
            flag_overdue = 0
            hilo_notif_overdue = threading.Thread(
                name="hilo_notif_overdue", target=notif_auto_overdue, args=[message])
            hilo_notif_overdue.start()
            print("Notificaciones automaticas de vencidas activadas")
            bot.send_message(
                message.chat.id, "Notificaciones automaticas de vencidas activadas")
        else:
            print("Las notificaciones automáticas ya están activas.")
            bot.send_message(
                message.chat.id, "Las notificaciones automáticas de vencidas ya están activas.")
    else:
        print(message.from_user.id, message.from_user.username,
              message.from_user.first_name, message.from_user.last_name)


# Funcion del hilo del bucle de notificaciones automaticas semanales
def notif_auto_weekly(mensaje):
    global delay_notif_auto_weekly
    global flag_weekly
    while (True):
        time.sleep(delay_notif_auto_weekly)
        if flag_weekly == 0:
            cmd_getWeek(mensaje)
        else:
            break
    print("Hilo semanal muerto.\n")

# Comando para mostrar tareas pendientes semanales AUTOMATICAMENTE


@bot.message_handler(commands=['start_auto_weekly'])
def notif_auto_week_bot(message):
    # Hace que solo mzarzu pueda activar las notificaciones automaticas
    if message.from_user.id == chat_id_mzarzu:
        global flag_weekly
        if flag_weekly != 0:
            flag_weekly = 0
            hilo_notif_weekly = threading.Thread(
                name="hilo_notif_weekly", target=notif_auto_weekly, args=[message])
            hilo_notif_weekly.start()
            print("Notificaciones automaticas de semanales activadas")
            bot.send_message(
                message.chat.id, "Notificaciones automaticas de semanales activadas")
        else:
            print("Las notificaciones automáticas de semanales ya están activas.")
            bot.send_message(
                message.chat.id, "Las notificaciones automáticas de semanales ya están activas.")
    else:
        print(message.from_user.id, message.from_user.username,
              message.from_user.first_name, message.from_user.last_name)


# Comando para parar los recordatorios de tareas diarias pendientes AUTOMATICAMENTE
@bot.message_handler(commands=['stop_auto'])
def stop_notif_auto_bot(message):
    # Hace que solo mzarzu pueda parar las notificaciones automaticas
    if message.from_user.id == chat_id_mzarzu:
        global flag_daily
        flag_daily = 1
        print("Notificaciones automaticas de diarias desactivadas")
        bot.send_message(
            message.chat.id, "Notificaciones automaticas de diarias desactivadas")
    else:
        print(message.from_user.id, message.from_user.username,
              message.from_user.first_name, message.from_user.last_name)

# Comando para parar los recordatorios de tareas overdues pendientes AUTOMATICAMENTE


@bot.message_handler(commands=['stop_auto_overdue'])
def stop_notif_auto_bot(message):
    # Hace que solo mzarzu pueda parar las notificaciones automaticas
    if message.from_user.id == chat_id_mzarzu:
        global flag_overdue
        flag_overdue = 1
        print("Notificaciones automaticas de overdues desactivadas")
        bot.send_message(
            message.chat.id, "Notificaciones automaticas de overdues desactivadas")
    else:
        print(message.from_user.id, message.from_user.username,
              message.from_user.first_name, message.from_user.last_name)

# Comando para parar los recordatorios de tareas semanales pendientes AUTOMATICAMENTE


@bot.message_handler(commands=['stop_auto_weekly'])
def stop_notif_auto_bot(message):
    # Hace que solo mzarzu pueda parar las notificaciones automaticas
    if message.from_user.id == chat_id_mzarzu:
        global flag_weekly
        flag_weekly = 1
        print("Notificaciones automaticas de semanales desactivadas")
        bot.send_message(
            message.chat.id, "Notificaciones automaticas de semanales desactivadas")
    else:
        print(message.from_user.id, message.from_user.username,
              message.from_user.first_name, message.from_user.last_name)


# Comando para modificar el delay de tareas diarias
@bot.message_handler(commands=['delay'])
def delay_notif_auto_bot(message):
    if message.from_user.id == chat_id_mzarzu:
        global delay_notif_auto
        global flag_daily
        if flag_daily == 0:
            texto_mensaje = message.text.split(" ")
            num_texto_mensaje = int(texto_mensaje[1])
            print(texto_mensaje, type(num_texto_mensaje))
            if type(num_texto_mensaje) == int or type(num_texto_mensaje) == float:
                new_delay_notif_auto = num_texto_mensaje*3600
                delay_notif_auto = new_delay_notif_auto
                print("Se ha establecio el delay de notificaciones diarias en " +
                      str(num_texto_mensaje) + " horas.")
                print(new_delay_notif_auto)
                bot.send_message(
                    message.chat.id, "Se ha establecio el delay de notificaciones diarias en " + str(num_texto_mensaje) + " horas.")
        else:
            print("No se han activado las notificaciones diarias automaticas.")
            bot.send_message(
                message.chat.id, "No se han activado las notificaciones diarias automaticas.")
    else:
        print(message.from_user.id, message.from_user.username,
              message.from_user.first_name, message.from_user.last_name)


# Comando para que responda si se mandan mensajes no soportados
@bot.message_handler(content_types=["text"])
def bot_mensajes_texto(message):
    if message.from_user.id == chat_id_mzarzu:
        if message.text.startswith("/"):
            bot.send_message(message.chat.id, 'Comando no disponible')
        else:
            bot.send_message(message.chat.id, "texto")
            print(message.text)
    else:
        print(message.from_user.id, message.from_user.username,
              message.from_user.first_name, message.from_user.last_name)


########## MAIN ########################################################################################################################
if __name__ == '__main__':
    print('Iniciando el bot...')
    hilo_bot = threading.Thread(name="hilo_bot", target=recibir_mensajes)
    hilo_bot.start()
    print('Hilo polling infinito iniciado')


##########################################
'''Para arreglar el problema de 
versiones telebot no tiene el argumento 
imput handler, ejecutar en orden:

pip3 uninstall telebot
pip3 uninstall PyTelegramBotAPI
pip3 install pyTelegramBotAPI
pip3 install --upgrade pyTelegramBotAPI


source: https://stackoverflow.com/questions/64951712/telebot-object-has-no-attribute-message-handler
'''
#########################################
