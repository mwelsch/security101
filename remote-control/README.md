# A little offensive test app
If I gain access to a PC this app might be deployed to gain remote access. In the future persistancy and maybe privelage escalation should be added

Initially I thought I would hide the whole thing as a HTTP(S) app with no other traffic, to minimize detection.
~~But WebSockets seem to be mainstream now anyway, so I will use those for now. For better anti-detection a HTTP proxy can be used~~

I will do most communication through the HTTP(S) webserver. In case I want to live stream the screen I have multiple options:
- WebRTC
- Websockets
- Socket.IO (built on top of Websockets, but seems easier to handle)
- plain socket

I do want to take an easy and reliable approach: I tried using WebRTC with [this project](https://medium.com/@supersjgk/building-a-live-streaming-app-using-flask-opencv-and-webrtc-8cc8b521fa44#d598)
but honestly:
- I click on the link and the livestream takes forever to load.
- I cannot view it in multiple browser simultaniously (maybe that was because of the webcam api tho).
- It looks like a single stream and kind of difficult to built any other functionallity into the same site

The next thing I am going to try is Socket.IO from the Flask addon. Plain sockets would need some kind of NodeJS stuff to be viewed in the webrowser and lack a lot of comfort when programming, like automatic reconnecting.
Socket.IO just seems to be an improved version from Websockets so why not try it?


## Server
Handles multiple clients, should be able to
- receive & store/display
  - images (screenshots)
  - keyboard inputs
- send
  - keystrokes
  - maybe: commands to a powershell or something like that
- update the client script (for bugfixes, new functionality, etc.)

## Client
A payload, that:
- is a keylogger
- sends screenshots along with keylogs
  - ToDo find some kind of indicator of how often or when it is necessary to grab a screenshot
- can self-update
- can receive remote commands
  - keystrokes
  - maybe powershell commands
- if executed as admin: gain persistancy
- future: gain admin access or persistancy as normal user