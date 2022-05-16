<img  src="https://cdn.glitch.global/5045ed4d-89cd-4f64-80ba-25a2c76b94b7/bot.png?v=1651674003202"  alt="logo">

# [VKinder](https://vk.com/public213024441 "Сообщество VKinder") chat-bot for Vkontakte App

It is a team project, built as a class project.

### Goal

Goal is to write a script for a chat-bot which will be interacting with databease of social media network Vkontakte. 
Bot will offer different choices od random matches built as a dialoge with the user.

### Instruction

You need to write the program with following conditions:
1. Using the information about the user of the bot (gender, age and city) find matching people for that user.
2. For those matches you need to get three most popular pictures, which you can determine by the amount of likes.
3. Return the information about the matching use in following format:

```
 First_name Last_name
 profile URL
 three pictures as an attachments (https://dev.vk.com/method/messages.send)
```

4. Should be a possibility to go to the next person, with the button or with a command.
5. Save favorite matches to favorites list.
6. Return favorites list.

 ### How To:

1. Install requirements from file `requirements.txt`. with the folloeing command `pip install -r requirements.txt`.
2. Go to main.py and run the file.
3. In modules.py you need to change your password, instead of YOURPASSWORD should be your unique password to create a database. 
For this bot we used PosеgreSQL и PgAdmin. After that run the script module.py, database will be created.
5. To chat with the bot, folloe the link [VKinder](https://vk.com/im?media=&sel=-213024441&v=)
6. To activate the bot write the message "привет".
7. When you press button "Показать" the results chosen according to algorythm from the initial task will be shown. Bot will choose profiles of the people opposite geneder, from the same city and the same age as a bot user. In case city information is missing, Moscow is used by default.
7. When user press button "Добавить в избранное" profile is added to database table favorites list. User have an option to review favorites list by pressing button "Список избранных".
8.  When user press button "Не нравится" profile is added to database table black list. User have an option to review favorites list by pressing button "Черный список".

