import webview
import requests
from server import server
import base64
class Api:
    def __init__(self):
        print("Welcome")
    def save_dialog(self, url):
        print(url.split(",")[1])
        path = window.create_file_dialog(webview.SAVE_DIALOG, directory='./', save_filename='')[0]
        with open(path, "wb") as fh:
            fh.write(base64.decodebytes("b'"+url.split(",")[1]+"='"))
        return "success"
if __name__ == '__main__':
    api = Api()
    window = webview.create_window("App", server, width=1200, height=900, resizable=False,js_api=api)
    webview.start(debug=True)
