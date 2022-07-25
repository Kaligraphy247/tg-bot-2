from telegram import *  # Update lives here
from telegram.ext import *  # CommandHandler, MessageHandler lives here
from requests import *
from dotenv import load_dotenv
from datetime import datetime

import database as db
import os, json

# Functions

def start_command(update: Update, context=CallbackContext):
    # authorized_users(context=context)
    buttons = [["Info"], ["List all movies 📽"], ["Search ATM's DB 🔎"], ["a"]]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Hello {update.effective_user.first_name}!\nWelcome to the bot!") #, Press a button to continue 👀",
    

    # reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True))
    print(f"(user) ~{update.message.from_user.username}~ pressed the start command at {time_now()}")  # debug

def time_now():
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    return timestamp

def buttons_list(update: Update, context=CallbackContext):
    update.message.reply_text(cmd_text)
    print(f"(user) ~{update.message.from_user.username}~ pressed the button list at {time_now()}")  # debug


def cancel(update: Update, context=CallbackContext):
    """Cancels and ends the conversation."""
    user = update.message.from_user
    print(f"{user.full_name} canceled the conversation")  # debug
    update.message.reply_text(
        "You canceled a conversation  🤷‍♂️"
    )  # , reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def help_command(update: Update, context=CallbackContext):
    update.message.reply_text(
        f"Hello @{update.effective_user.username}! This is the help command"
    )
    print("Pressed the help command")  # debug


def info(update: Update, context=CallbackContext):
    update.message.reply_text(
        f"Hello @{update.effective_user.username}! This is the info command"
    )
    print("Pressed the info command")  # debug


def hello(update: Update, context=CallbackContext):
    update.message.reply_text(
        f"Hello @{update.effective_user.username}! This is the hello"
    )
    print("Pressed the help command")  # debug


def hello2(update: Update, context=CallbackContext):
    update.message.reply_text(
        f"Hello @{update.effective_user.username}! This is the hello2 command"
    )
    print("Pressed the hello2 command")  # debug


def format_search_result(search_results: tuple) -> str:
    """formats the tuple to something else"""
    movie_title = [title[1] for title in search_results]
    movie_link = [link[2] for link in search_results]
    msg = ""
    for title, link in sorted(zip(movie_title, movie_link)):
        msg += f"{title}\n{link} 🖱\n\n"
    return msg


def list_all(update: Update, context=CallbackContext):
    conn = db.create_connection(database)
    results = db.show_all_movies(conn)
    msg = format_search_result(results)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"All Movies in DB 📽\nTotal: {len(results)}",
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    print(f"(user) ~{update.message.from_user.username}~ pressed the button list at {time_now()}")  # debug

SEARCH_QUERY = range(1)


def search_db(update: Update, context=CallbackContext):
    # context.bot.send_message(chat_id=update.effective_chat.id, text="Search DB")
    update.message.reply_text(
        "Search ATM's DB 🔎\n", reply_markup=ForceReply(selective=True)
    )
    print(f"(user) ~{update.message.from_user.username}~ pressed the button search {time_now()}")  # debug    return SEARCH_QUERY
    # print(user_data, text)


def search_query(update: Update, context: CallbackContext):
    """Stores the Search Query and sends the result to the user"""
    conn = db.create_connection(database)
    title = update.message.text
    print(title)
    results = db.show_movie_by_title(conn, (title))
    if len(results) >= 1:
        msg = format_search_result(results)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Result for "{title}" 🔎\nTotal: {len(results)}',
        )
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        return ConversationHandler.END

    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Sorry, I couldn't find that in my Database 😢,\nTry again? /search 🔎",
        )
        return ConversationHandler.END


ADD_QUERY = range(1)
def add_movie_command(update: Update, context: CallbackContext):
    """Command for adding movies to DB"""
    if update.effective_chat.username not in allowed_usernames:
        update.message.reply_html(
            "I don't think you are allowed to use this function 🤔\nAsk <a href='t.me/lazy_jay'>Admin</a> for Permission 👀", disable_web_page_preview=True)
        print(f"Unauthorized: '{update.message.from_user.username}' tried to use me without permission")
    else:    
        update.message.reply_text(
            "Add new Movie to ATM's DB  ▶\nReply like the image shown below.\nType ➡ cancel; ⬅ to cancel",
            reply_markup=ForceReply(selective=True),
        )
        context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=open(add_movie_img, "rb")
        )
        print(f"(user) ~{update.message.from_user.username}~ pressed the add_movie command at {time_now()}")  # debug
        return ADD_QUERY


def add_movie_name(update: Update, context: CallbackContext):
    """Adds the movie to the database"""
    conn = db.create_connection(database)
    title = update.message.text

    if ";" not in title:
        print("wrong format")  # debug
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Wrong Format\nReply like the image shown below.",
        )
        context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=open(add_movie_img, "rb")
        )
        return ConversationHandler.END

    elif title.startswith(";"):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Wrong Format\nReply like the image shown below.",
        )
        context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=open(add_movie_img, "rb")
        )
        return ConversationHandler.END

    elif title.count(";") > 1:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Wrong Format\nReply like the image shown below.",
        )
        context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=open(add_movie_img, "rb")
        )
        return ConversationHandler.END

    else:
        if title == "cancel;":
            user = update.message.from_user
            print(f"{user.full_name} canceled Add movie command")  # debug
            update.message.reply_text("Canceled!", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        else:
            title = title.split(";")
            name = title[0].strip()
            link = title[1].strip()
            print(type(name), type(link))
            db.add_movie(conn, (name, link))
            # db.add_movie(conn, (str(name), str(title))) # db.add_movie(conn, (name, title))
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Success!\nUse /list_all to view all movies",
            )
            return ConversationHandler.END

UPDATE_QUERY_1, UPDATE_QUERY_2, UPDATE_QUERY_3 = range(3)
def update_movie_command(update: Update, context: CallbackContext):
    """Command for updating movies in db"""
    if update.effective_chat.username not in allowed_usernames:
        update.message.reply_html(
                "I don't think you are allowed to use this function 🤔\nAsk <a href='t.me/lazy_jay'>Admin</a> for Permission 👀", disable_web_page_preview=True)
        print(f"Unauthorized: '{update.message.from_user.username}' tried to use me without permission")
    
    else:
        update.message.reply_text("Update movie\nSearch  🔎  for the movie you want to update  👀", reply_markup=ForceReply(selective=True))
        print(f"(user) ~{update.message.from_user.username}~ pressed the update_movie command at {time_now()}")  # debug
        return UPDATE_QUERY_1


def update_query(update: Update, context: CallbackContext):
    """Updates existing movie from db"""
    conn = db.create_connection(database)
    search_update = update.message.text
    results, RESULTS = db.show_movie_by_title(conn, (search_update)), db.show_movie_by_title(conn, (search_update))
    update_query.for_id_in_stage_2 = RESULTS # funny way to export this variable to the next stage
    if len(results) >= 1:
        movie_id = [pk[0] for pk in results]
        movie_title = [title[1] for title in results]
        movie_link = [link[2] for link in results]
        msg = ""
        for id, title, link in sorted(zip(movie_id, movie_title, movie_link)):
            msg += f"{id}.   {title}      {link}\nEnter \"{id}\" to update\n\n"
        update.message.reply_text(text=msg, reply_markup=ForceReply(selective=True))
        return UPDATE_QUERY_2
    
    else:
        update.message.reply_text("Sorry, I couldn't find that in my Database 😢,\nTry again? /search 🔎")
        return ConversationHandler.END


def update_query_2(update: Update, context: CallbackContext):
    """Next step to updating movie in db"""
    search_query = update.message.text
    update_query_2.for_id_in_stage_3 = search_query # like it says, for id to be used in stage 3
    movie_ids = []
    print(f"search_query in stage 2: {search_query}") # debug
    for result in update_query.for_id_in_stage_2:
        movie_ids.append(str(result[0]))
        # print(f"result @ index 0: {result[0]}") # debug
    if search_query in movie_ids:
        conn = db.create_connection(database)
        update.message.reply_text("Enter the update in the format shown below\nType ➡ cancel; ⬅ to cancel")
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(add_movie_img, "rb"))
        # break
        return UPDATE_QUERY_3
    else:
        update.message.reply_text("Looks like you entered a wrong id number  ☠\nTry again /update_movie")
        return ConversationHandler.END


def update_query_3(update: Update, context: CallbackContext):
    """Next step to updating the movie in the db.\n
    This step takes the input (reply) and updates the database
    with the corresponding id"""
    print("Stage 3") # debug
    new_update: str = update.message.text # redundant because `update` is already taken in this scope too 
    if ";" not in new_update:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Wrong Format\nReply like the image shown below.")
        context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=open(add_movie_img, "rb"))
        return ConversationHandler.END

    elif new_update.startswith(";"):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Wrong Format\nReply like the image shown below.")
        context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=open(add_movie_img, "rb"))
        return ConversationHandler.END

    elif new_update.count(";") > 1:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Wrong Format\nReply like the image shown below.")
        context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=open(add_movie_img, "rb"))
        return ConversationHandler.END

    else:
        if new_update == "cancel;":
            user = update.message.from_user
            print(f"(user) ~{update.message.from_user.username}~ canceled the update_movie command at {time_now()}")  # debug
            update.message.reply_text("Canceled!", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        else:
            conn = db.create_connection(database)
            new_update: list = new_update.split(sep=";")
            print(new_update) # debug
            new_movie_title = new_update[0].strip()
            new_movie_link = new_update[1].strip()
            db.update_movie(conn, (new_movie_title, new_movie_link, int(update_query_2.for_id_in_stage_3)))
            context.bot.send_message(chat_id=update.effective_chat.id, text="📽  Movie updated!   🔃")
            return ConversationHandler.END

DELETE_QUERY_1, DELETE_QUERY_2, DELETE_QUERY_3 = range(3)
def delete_movie_command(update: Update, context: CallbackContext):
    """Delete movie command"""
    if update.effective_chat.username not in allowed_usernames:
        update.message.reply_html(
            "I don't think you are allowed to use this function 🤔\nAsk <a href='t.me/lazy_jay'>Admin</a> for Permission 👀", disable_web_page_preview=True)
        print(f"Unauthorized: '{update.message.from_user.username}' tried to use me without permission")
    
    else:
        update.message.reply_text("Delete Movie\nSearch  🔎  for the movie you want to delete  👀", reply_markup=ForceReply(selective=True))
        print(f"(user) ~{update.message.from_user.username}~ pressed the delete movie command at {time_now()}")  # debug
        return DELETE_QUERY_1


def delete_query(update: Update, context: CallbackContext):
    """Delete Query 1"""
    conn = db.create_connection(database)
    search_update = update.message.text
    results = db.show_movie_by_title(conn, (search_update))
    # delete_query.search_text = results 
    delete_query.movie_id = [pk[0] for pk in results]# funny way to export this variable to the next stage
    if len(results) >= 1:
        movie_id = [pk[0] for pk in results]
        movie_title = [title[1] for title in results]
        movie_link = [link[2] for link in results]
        msg = ""
        for id, title, link in sorted(zip(movie_id, movie_title, movie_link)):
            msg += f"{id}.   {title}      {link}\nEnter \"{id}\" to delete\n\n"
        update.message.reply_text(text=msg, reply_markup=ForceReply(selective=True))
        return DELETE_QUERY_2
    else:
        update.message.reply_text("Sorry, I couldn't find that in my Database 😢,\nTry again? /delete_movie 🔎")
        return ConversationHandler.END

def delete_query_2(update: Update, context: CallbackContext):
    """Delete Query 2"""
    search_query = update.message.text # expecting the movie_id at the point
    movie_id = [str(ids) for ids in delete_query.movie_id]
    if search_query in movie_id:
        conn = db.create_connection(database)
        db.delete_movie(conn, int(search_query))
        context.bot.send_message(chat_id=update.effective_chat.id, text="Deleted!")
        return ConversationHandler.END

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, that didn't work\nTry again /delete_movie")
        return ConversationHandler.END


# program
if __name__ == "__main__":
    load_dotenv(dotenv_path=".")

    TOKEN = os.environ.get("TOKEN")
    PORT = int(os.environ.get('PORT', 5000)) # FOR PRODUCTION 
    add_movie_img = r"images\add_movie_example.png"
    # allowed_usernames = ["lazy_jay", "Artemokrloov", "Jayminai", "Kaligraph_Jay"]#os.environ.get('allowed') 
    allowed_usernames = json.loads(os.environ['allowed_usernames']) 
    

    database = "./movies.db"  # path to db
    # # if not os.path.exists(database): # only creates a db if path does not exist
    # conn = db.create_connection(database)


    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher


    search_convo_handler = ConversationHandler(
        entry_points=[CommandHandler("search", search_db)],
        states={SEARCH_QUERY: [MessageHandler(Filters.text, search_query)]},
        fallbacks=[CommandHandler("cancel", cancel)],
        conversation_timeout=600,
    )

    add_movie_convo_handler = ConversationHandler(
        entry_points=[CommandHandler("add_movie", add_movie_command)],
        states={
            ADD_QUERY: [MessageHandler(Filters.text, add_movie_name)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        conversation_timeout=600,
    )

    update_movie_convo_handler = ConversationHandler(
        entry_points=[CommandHandler("update_movie", update_movie_command)],
        states={
            UPDATE_QUERY_1: [MessageHandler(Filters.text, update_query)],
            UPDATE_QUERY_2: [MessageHandler(Filters.text, update_query_2)],
            UPDATE_QUERY_3: [MessageHandler(Filters.text, update_query_3)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        conversation_timeout=600,
    )

    delete_movie_convo_handler = ConversationHandler(
        entry_points=[CommandHandler("delete_movie", delete_movie_command)],
        states={
            DELETE_QUERY_1: [MessageHandler(Filters.text, delete_query)],
            DELETE_QUERY_2: [MessageHandler(Filters.text, delete_query_2)],
            DELETE_QUERY_3: []
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        conversation_timeout=600,
    )


    cmd_text = """
        1. /start\n
2. /info\n
3. /help\n
4. /hello\n
5. /hello2\n
6. /cmd\n
7. /list_all\n
8. /search\n
9 /cancel\n
10. /add_movie\n
11. /update_movie\n
12. /delete_movie\n
This command is for development purpose only. It will be removed in production.
        """

    # dipatcher
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("list_all", list_all))
    dispatcher.add_handler(CommandHandler("cancel", cancel))

    dispatcher.add_handler(search_convo_handler)  # convo handler for searching for movies
    dispatcher.add_handler(add_movie_convo_handler)  # convo handler for adding movie
    dispatcher.add_handler(update_movie_convo_handler) # convo handler for updating existing movie
    dispatcher.add_handler(delete_movie_convo_handler) # convo handler for deleting existing movie

    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("info", info))

    dispatcher.add_handler(CommandHandler("hello", hello))
    dispatcher.add_handler(CommandHandler("hello2", hello2))
    dispatcher.add_handler(CommandHandler("cmd", buttons_list))


   

    print("Running...")

    # For development only
    # updater.start_polling()  # bot is running
    # updater.idle()

    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN, webhook_url="https://tg-bot-2-prod.herokuapp.com/" + TOKEN)

    # updater.bot.setWebhook("https://tg-bot-2-prod.herokuapp.com/" + TOKEN)
    # updater.idle()
                            
