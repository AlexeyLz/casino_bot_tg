from database.database_connection import connection
from aiogram import types


def register_user(message: types.Message):
    cursor = connection.cursor()
    cursor.execute('select * from users where id = ?', (message.from_user.id,))
    if len(cursor.fetchall()) < 1:
        cursor.execute('INSERT INTO users (id, username, balance) VALUES (?,?,?)',
                       (message.from_user.id, message.from_user.username, 0))
        connection.commit()
        print('reg', message.from_user.id, message.from_user.username)
        cursor.close()
    cursor.close()


def check_user_registered(user_id):
    cursor = connection.cursor()
    cursor.execute('select * from users where id = ?', (user_id,))
    if len(cursor.fetchall()) < 1:
        cursor.close()
        return False
    cursor.close()
    return True


def check_user_have_balance(user_id, balance):
    cursor = connection.cursor()
    cursor.execute('select * from users where id = ?', (user_id,))
    data = cursor.fetchone()
    cursor.close()
    if float(data[2]) >= float(balance):
        return True
    return False


def give_money(user_id, money):
    cursor = connection.cursor()
    cursor.execute('select * from users where id = ?', (user_id,))
    balance = float(cursor.fetchone()[2])
    balance += float(money)
    cursor.execute('UPDATE users SET balance = ? WHERE id = ?', (balance, user_id,))
    connection.commit()
    cursor.close()


def take_money(user_id, money):
    cursor = connection.cursor()
    cursor.execute('select * from users where id = ?', (user_id,))
    balance = float(cursor.fetchone()[2])
    balance -= float(money)
    cursor.execute('UPDATE users SET balance = ? WHERE id = ?', (balance, user_id,))
    connection.commit()
    cursor.close()


def get_balance(user_id):
    cursor = connection.cursor()
    cursor.execute('select * from users where id = ?', (user_id,))
    balance = float(cursor.fetchone()[2])
    cursor.close()
    return balance
