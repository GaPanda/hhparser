# hhparser

Разработан с целью получения данных с сайта [hh.ru](http://hh.ru).

***

Необходимые программы:

1) [Python 3.x](https://www.python.org/downloads/)

2) [MSSQL Server 2016 Express](https://www.microsoft.com/ru-ru/sql-server/sql-server-editions-express).

3) Библиотеки python установленные с помощью пакетного менеджера pip
   - lxml-3.7.3 и выше
   - beautifulsoup4 4.5.3 и выше
   - pyodbc 4.0.15 и выше

***

Установка:

1) Скопировать репозиторий к себе на компьютер или скачать zip архив с файлами проекта hhparser. Распаковать с помощью архиватора, например [WinRar](http://www.win-rar.ru/download/), в любую удобную для вас директорию. 
2) Установить необходимые программы(Python и MSSQL Server) и библиотеки python. Установку библиотек можно осуществить с помощью команды в командной строке Windows:

```
pip install lxml bs4 pyodbc
```
3) Создать базу данных с помощью сгенерированного файла MSSQL\crebas.sql (Изображение физической модели также находиться в папке MSSQL).

4) Если Python не добавлен в переменную PATH(в Windows) или возникает ошибка с запуском файла script_run.bat. Нужно добавить в файл script_run.bat полный путь до python.exe.
##### Стандартный:
```
@echo off
cmd /k "python main.py"
```
##### Измененный:
```
@echo off
cmd /k "Путь до файла\python.exe main.py"
```
5) Запускать скрипт с помощью файла script_run.bat.
