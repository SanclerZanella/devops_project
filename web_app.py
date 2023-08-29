from flask import Flask
import requests

app = Flask(__name__)


@app.route('/users/get_user_data/<user_id>', methods=["GET"])
def get_user_data(user_id):
    get_user_endpoint = f"http://127.0.0.1:5000/users/{user_id}"

    try:
        response = requests.get(get_user_endpoint, stream=True)
        data = response.json()
        return f"<h1 id='user'>{data['User_name']}</h1>"

    except requests.RequestException as e:
        return f"Error: {e}", 500

    except Exception as e:
        return f"<h1 id='user'>No such user: {user_id}</h1>"


if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5001,
        debug=True
    )
