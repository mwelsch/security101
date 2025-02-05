from asyncio import Queue

import mss
import mss.tools

class ScreenCapture:
    def capture_screen(self):
        return None

    def grab(queue: Queue) -> None:
        rect = {"top": 0, "left": 0, "width": 600, "height": 800}

        with mss.mss() as sct:
            for _ in range(1_000):
                queue.put(sct.grab(rect))

        # Tell the other worker to stop
        queue.put(None)


    def save(queue: Queue) -> None:
        number = 0
        output = "screenshots/file_{}.png"
        to_png = mss.tools.to_png

        while "there are screenshots":
            img = queue.get()
            if img is None:
                break

            to_png(img.rgb, img.size, output=output.format(number))
            number += 1