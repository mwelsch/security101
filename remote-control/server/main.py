from io import BytesIO
from flask import Flask, render_template, request, send_file

from server.handle_server_requests import ServerHandler

app = Flask(__name__)
handler = ServerHandler()
@app.route('/', methods=['GET', 'POST'])
def receive_screenshot():
    return handler.screenshot_received(request)




@app.route('/control', methods=['GET', 'POST'])
def show_screen():
    return handler.control_view()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True, port=5000)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
