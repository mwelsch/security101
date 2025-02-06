import asyncio
import base64
from flask import render_template
from flask_socketio import emit


class ServerHandler:
    def __init__(self):
        self.database = PseudoDatabase()
    def screenshot_received(self, request):
        if request.method == 'POST':
            file = request.files['file']
            file = base64.b64encode(file.read())
            file = file.decode()
            self.database.update_last_screenshot(file)
            return f'Uploaded'
        return render_template('index.html')

    def control_view(self):

        #return send_file(BytesIO(self.database.get_last_screenshot()),
        #         download_name="Renamed.jpg", as_attachment=True)

        return render_template('control.html', user_image = self.database.get_last_screenshot())

    def stream_newest_image(self):
            emit('newest_image_returned', {'data': self.database.get_last_screenshot()})


class PseudoDatabase:
    last_screenshot = None
    def __init__(self):
        self.last_screenshot = None

    def update_last_screenshot(self, file):
        self.last_screenshot = file

    def get_last_screenshot(self):
        return self.last_screenshot