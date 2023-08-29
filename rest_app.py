import datetime
import pymysql
from flask import Flask, jsonify, request
from db_connector import ConnectDB

app = Flask(__name__)


@app.route('/users/<user_id>', methods=["GET", "POST", "PUT", "DELETE"])
def resta_app(user_id):
    try:
        db = ConnectDB()
        db_conn = db.connect_db()

    except pymysql.Error as e:
        response = {"Status": "ERROR", "reason": f'{e}'}
        return jsonify(response), 500

    if request.method == "POST":
        try:
            with db_conn.cursor() as cursor:
                select_query = "SELECT user_id FROM users WHERE user_id = %s"
                cursor.execute(select_query, (user_id,))
                user = cursor.fetchone()

            if user:
                raise UserAlreadyExists("Id already exists")
            else:
                data = request.get_json()
                user_name = data.get('user_name')

                with db_conn.cursor() as cursor:
                    insert_query = "INSERT INTO users (user_id, user_name, creation_date) VALUES (%s, %s, %s)"
                    cursor.execute(insert_query, (user_id, user_name, datetime.datetime.now()))
                    db_conn.commit()

                response = {"Status": "OK", "User_added": f"{user_name}"}
                return jsonify(response), 200

        except pymysql.Error as e:
            response = {"Status": "ERROR", "reason": f'{e}'}
            return jsonify(response), 500

        except UserAlreadyExists as e:
            response = {"Status": "ERROR", "reason": f'{e}'}
            return jsonify(response), 500

        except Exception as e:
            response = {"Status": "ERROR", "reason": f'{e}'}
            return jsonify(response), 500

    elif request.method == "GET":
        try:
            with db_conn.cursor() as cursor:
                query_data = (user_id,)
                retrieve_query = "SELECT user_id, user_name FROM users WHERE user_id = %s"
                cursor.execute(retrieve_query, query_data)
                user = cursor.fetchone()

            if user:
                id_user, user_name = user
                response = {"Status": "OK", "User_name": f"{user_name}"}
                return jsonify(response), 200
            else:
                raise UserDoesNotExist("No such ID")

        except pymysql.Error as e:
            response = {"Status": "ERROR", "reason": f'{e}'}
            return jsonify(response), 500

        except UserDoesNotExist as e:
            response = {"Status": "ERROR", "reason": f'{e}'}
            return jsonify(response), 500

        except Exception as e:
            return f"General error - {e}"

    elif request.method == "PUT":
        try:
            with db_conn.cursor() as cursor:
                query_data = (user_id,)
                retrieve_query = "SELECT user_id, user_name FROM users WHERE user_id = %s"
                cursor.execute(retrieve_query, query_data)
                user = cursor.fetchone()

            data = request.get_json()
            new_value = data.get('user_name')

            if user:
                with db_conn.cursor() as cursor:
                    update_query = "UPDATE users SET user_name = %s WHERE user_id = %s"
                    cursor.execute(update_query, (new_value, user_id))
                    db_conn.commit()

                response = {"Status": "OK", "User_updated": f"{new_value}"}
                return jsonify(response), 200
            else:
                raise UserDoesNotExist("No such ID")

        except pymysql.Error as e:
            response = {"Status": "ERROR", "reason": f'{e}'}
            return jsonify(response), 500

        except UserDoesNotExist as e:
            response = {"Status": "ERROR", "reason": f'{e}'}
            return jsonify(response), 500

        except Exception as e:
            return f"General error - {e}"

    elif request.method == "DELETE":
        try:
            with db_conn.cursor() as cursor:
                query_data = (user_id,)
                retrieve_query = "SELECT user_id, user_name FROM users WHERE user_id = %s"
                cursor.execute(retrieve_query, query_data)
                user = cursor.fetchone()

            if user:
                with db_conn.cursor() as cursor:
                    delete_query = "DELETE FROM users WHERE user_id = %s"
                    cursor.execute(delete_query, (user_id,))
                    db_conn.commit()

                response = {"Status": "OK", "User_deleted": f"{user_id}"}
                return jsonify(response), 200
            else:
                raise UserDoesNotExist("No such ID")

        except pymysql.Error as e:
            response = {"Status": "ERROR", "reason": f'{e}'}
            return jsonify(response), 500

        except UserDoesNotExist as e:
            response = {"Status": "ERROR", "reason": f'{e}'}
            return jsonify(response), 500

        except Exception as e:
            return f"General error - {e}"


class UserAlreadyExists(Exception):
    def __init__(self, message):
        super().__init__(message)


class UserDoesNotExist(Exception):
    def __init__(self, message):
        super().__init__(message)


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
