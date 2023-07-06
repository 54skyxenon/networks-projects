# Video Streaming with RTSP and RTP

### Purpose

A video streaming GUI application written in Python to support playing Motion JPEGs. Summarizing completed sessions, automatic connection setup, and getting video descriptions are also implemented.

### Usage
To start the server:
```bash
$ python3 Server.py 6789
```

Then, to start the client player:
```bash
$ python3 ClientLauncher.py 127.0.0.1 6789 3000 movie.Mjpeg
```

You can replace **6789** with whichever server port you prefer and **3000** with whatever RTP port you prefer. Currently, `movie.Mjpeg` is the only file available to test on.

The four buttons are self-explanatory, try clicking on them!

### Specification
- `ClientLauncher.py` starts up the GUI interaction
- `Client.py` sends commands from the user to the server, processes server responses, and renders video frames
- `RtpPacket.py` is responsible for building and decoding RTP packet header (see PDF for more details)
- `Server.py` sets up socket connections to clients
- `ServerWorker.py` processes received requests and sends back responses
- `VideoStream.py` is an abstraction for each frame of the video