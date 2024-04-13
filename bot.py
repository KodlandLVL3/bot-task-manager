from telebot import TeleBot
import telebot
from logic import TaskManager
bot = TeleBot("")

task_manager = TaskManager("database.db")
task_manager.create_table()

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, """Привет! Я бот-менеджер задач 
Помогу тебе сохранить твои задачи!) 

/add_task - используй для добавления новой задачи
/delete_task - используй для удаления задачи                                      
                     """)
    

@bot.message_handler(commands=['add_task'])
def addtask_command(message):
    bot.send_message(message.chat.id, "Введите название задачи:")
    bot.register_next_step_handler(message, save_task)

def save_task(message):
    name = message.text
    user_id = message.from_user.id 
    task_manager.add_task(user_id, name, '')
    bot.send_message(message.chat.id, "Задача добавлена")

@bot.message_handler(commands=['delete_task'])
def deletetask_command(message):
    bot.send_message(message.from_user.id, "Введите имя задачи, которую хотите удалить:")
    bot.register_next_step_handler(message, delete_task_by_id)

def delete_task_by_id(message):
    user_id = message.from_user.id  
    task_name = message.text
    task_manager.delete_task(task_name, user_id)
    bot.send_message(message.chat.id, "Задача удалена")

@bot.message_handler(commands=['show']) 
def show(message):
    user_id = message.from_user.id 
    arg = telebot.util.extract_arguments(message.text)
    try:
        arg = int(arg)
        tasks = task_manager.show_task_many(user_id, arg)
    except:
        tasks = task_manager.show_task_all(user_id)
    if tasks:
        tasks =  "\n".join([x[0] for x in tasks])
        bot.send_message(message.chat.id, tasks)
    else:
        bot.send_message(message.chat.id, "Задач нет")
        

bot.infinity_polling()
