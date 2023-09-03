import requests


try:
    # Get request to the REST API to stop and close it
    requests.get('http://127.0.0.1:5000/stop_server')

    # Get request to the WEB API to stop and close it
    requests.get('http://127.0.0.1:5001/stop_server')

except Exception as e:

    # Catch any general exception when trying to stop the servers
    print(f'Error stopping server: {e}')
