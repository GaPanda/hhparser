# hhparser

Разработан с целью получения данных с сайта [hh.ru](http://hh.ru).

Разработка производилась в операционной среде Windows. Работоспособность программы на UNIX-подобных ОС не проверялась. На данный момент программа умеет работать только с базами данных MSSQL Server, в дальнейшем список будет пополняться.

***

## Необходимые программы:

Для добавление и просмотра обработанных программой запросов необходимы:

1) [MSSQL Server 2016 Express](https://www.microsoft.com/ru-ru/sql-server/sql-server-editions-express).
   
   [SQL Server Management Studio](https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms)

Если вы скачиваете архив скомпилированной программы, то установка Python и библиотек не обязательно.

2) [Python 3.x](https://www.python.org/downloads/)

3) Библиотеки python установленные с помощью пакетного менеджера pip.
   - lxml-3.7.3 и выше
   - beautifulsoup4 4.5.3 и выше
   - pyodbc 4.0.15 и выше

   Установку библиотек можно осуществить с помощью команды в командной строке Windows:
   ```
   pip install lxml bs4 pyodbc
   ```
***

## Установка скомпилированной программы:

1) Скачать архив по данной [ссылке](https://yadi.sk/d/3nPADzE13GkaBz). Распаковать с помощью архиватора, например [WinRar](http://www.win-rar.ru/download/), в любую удобную для вас директорию.

2) Создать базу данных на сервере MSSQL с помощью сгенерированного файла mssql\crebas.sql (Изображение физической модели также находиться в папке MSSQL).

3) Отредактировать конфигурационный файл config\config.ini под свои нужды (Необходимо использовать синтаксис Python). Указать имена своих MSSQL сервера и базы данных.Указать задержку между запросами в переменной timeout, значение по умолчанию 0. Так же, если необходимо отредактировать, добавить или удалить ключевые слова по которым происходит поиск информации о вакансии.

4) Запускать программу с помощью исполняемого файла hh_parser.exe, который находится в корне папки с программой.

***

## Установка из исходников:

1) Скопировать репозиторий к себе на компьютер или скачать zip архив с файлами проекта hhparser. Распаковать с помощью архиватора, например [WinRar](http://www.win-rar.ru/download/), в любую удобную для вас директорию. 

2) Установить необходимые программы(Python и MSSQL Server) и библиотеки python.

3) Создать базу данных с помощью сгенерированного файла mssql\crebas.sql (Изображение физической модели также находиться в папке MSSQL).

4) Отредактировать конфигурационный файл config\config.ini под свои нужды (Необходимо использовать синтаксис Python). Указать имена своих MSSQL сервера и базы данных.Указать задержку между запросами в переменной timeout, значение по умолчанию 0. Так же, если необходимо отредактировать, добавить или удалить ключевые слова по которым происходит поиск информации о вакансии.

5) Запускать скрипта 
   
   С помощью команды в консоле.
   ```
   Путь до файла\python.exe Путь до файла\hhparser.py
   ```
   
   С помощью файла script_run.bat.
   
   Если возникает ошибка с запуском файла script_run.bat. Нужно добавить в файл script_run.bat полный путь до python.exe и до файла hhparser.py.
   ##### Стандартный:
   ```
   @echo off
   cmd /k "python hhparser.py"
   ```
   ##### Измененный:
   ```
   @echo off
   cmd /k "Путь до файла\python.exe Путь до файла\hhparser.py"
   ```
***

## Работа с программой

После запуска программы, для выполнения запроса введите команду 1. Далее введите ваш поисковый запрос.

![alt text](http://i.piccy.info/i9/b4120ae76ab65f97539317ece29010fa/1491589138/9706/1135829/1.png)

После успешного выполнения запроса появится информация о времени обработки запроса, так же программа предложит добавить запрос в базу данных.

![alt text](http://i.piccy.info/i9/77a067c042a86b7ae08f9dfec284dfae/1491589221/14490/1135829/2.png)

При успешном добавлении появится сообщение, о времени добавления в базу данных.
![alt text](http://i.piccy.info/i9/1c523dbea21d781a960d707386756f1e/1491589225/18335/1135829/3.png)

Для просмотра информации из файла config.ini, введите команду 2.
![alt text](http://i.piccy.info/i9/0c1e44b7b203371cebe7703490d28689/1491589228/18438/1135829/4.png)

Для выхода из программы, введите команду 3.
