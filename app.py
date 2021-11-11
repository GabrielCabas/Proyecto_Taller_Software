import webview
import requests
from server import server
import base64
import os
class Api:
    def __init__(self):
        print("Welcome")

    def save_dialog(self, value):
        directory = os.path.realpath(".").split("/")
        directory = directory[0] + "/" + directory[1] + "/" + directory[2] + "/"
        path = window.create_file_dialog(webview.SAVE_DIALOG, directory=directory, save_filename='data{}'.format(value))[0]
        return path

if __name__ == '__main__':
    api = Api()
    window = webview.create_window("App", server, width=1200, height=900, resizable=False,js_api=api)
    webview.start(debug=True)