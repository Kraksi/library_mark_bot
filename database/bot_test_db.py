# import pymysql
# def check_db():
#     # Параметры подключения
#     db_config = {
#         'host': '192.168.9.33',      # IP-адрес сервера MariaDB
#         'user': 'bot_user',      # Имя пользователя
#         'password': 'tOOT00A!',   # Пароль пользователя
#         'database': 'bot_db',        # Название базы данных
#         'port': 3306                 # Порт (по умолчанию 3306)
#     }

#     try:
#         # Попытка подключения к базе данных
#         connection = pymysql.connect(**db_config)
#         print("Успешно подключено к базе данных!")
        
#         # Пример выполнения простого запроса
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT DATABASE();")  # Проверяем, к какой БД подключены
#             current_db = cursor.fetchone()
#             print(f"Подключены к базе данных: {current_db[0]}")

#     except pymysql.MySQLError as e:
#         print(f"Ошибка подключения к базе данных: {e}")
#     finally:
#         # Закрываем соединение, если оно было установлено
#         if 'connection' in locals() and connection.open:
#             connection.close()
#             print("Соединение закрыто.")
#             return 1

# check_db()