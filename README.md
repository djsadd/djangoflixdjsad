
<h1 align="center"><a href="https://daniilshat.ru/" target="_blank">Netflix analogue written in Django</a> 
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>

<!--- Images --->
<img src="https://github.com/djsadd/djangoflixdjsad/blob/main/media/Снимок%20экрана%202023-09-13%20152814.png">
<img src="https://github.com/djsadd/djangoflixdjsad/blob/main/media/Снимок%20экрана%202023-09-13%20155052.png">
<img src="https://github.com/djsadd/djangoflixdjsad/blob/main/media/Снимок%20экрана%202023-09-13%20155804.png">
<img src="https://github.com/djsadd/djangoflixdjsad/blob/main/media/Снимок%20экрана%202023-09-13%20161217.png">


[![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=How+to+run+this+project)](https://git.io/typing-svg)

# First step: install env and install requirements.txt 
  > - ```python3 -m venv {myenvname}```
  > - ```source {myenvname}/Scripts/activate```
  > - ```pip install requierements.txt```

# Second step: Edit setting.py
  > - delete in settings: dabatases.

Use settings:
```
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': BASE_DIR / 'db.sqlite3',
   }
}
```

# Third step: Migrate database.
  > - wrie in command line: py manage.py migrate

# Fourth step: Run Server
  > - go to root folder in porject and runserver
  > - ```py manage.py runserver```
