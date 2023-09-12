import os
import signal
from flask import Flask
import requests

app = Flask(__name__)


@app.route('/users/get_user_data/<user_id>', methods=["GET"])
def get_user_data(user_id):
    """
    Description:
        This router retrieve any user from the database and render in the browser with HTML elements.

    Parameters:
        * user_id - Corresponds to the user ID in the database.

    Return:
        HTML elements in case of successful response or String containing exception message in case
        of failing response.
    """
    get_user_endpoint = f"http://rest_app:5000/users/{user_id}"

    try:
        # Make a GET request to the REST API to retrieve a user returning the HTML element
        response = requests.get(get_user_endpoint, stream=True)
        data = response.json()
        return f"<h1 id='user'>{data['User_name']}</h1>"

    except requests.RequestException as e:
        return f"Error: {e}", 500

    except Exception as e:
        return f"<h1 id='user'>No such user: {user_id}</h1>"


@app.route('/stop_server')
def stop_server():
    """
        Description:
            Stop the API server.

        Return:
            Sting response with status of the operation.
    """
    try:
        os.kill(os.getpid(), signal.CTRL_C_EVENT)
        return 'Server Stopped'
    except Exception as e:
        return f'Error stopping server: {e}'


@app.errorhandler(404)
def page_not_found(e):
    """
        Description:
            Friendly message when the status code is 404.

        Return:
            Sting response with status of the operation.
    """
    return f'Whoops! Looks like this page went on vacation!\n {e}', 404


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )
