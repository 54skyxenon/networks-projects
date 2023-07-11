# UDP Pinger

### Purpose

An experiment in pinging UDP packets to an unreliable server.

### Usage

First, start the server:
```bash
$ python3 UDPPingerServer.py
```

And then send a few pings from the client:
```bash
$ python3 UDPPingerClient.py
```

### Heartbeats

Heartbeats check if an application is still running. The heartbeat client will stop transmitting after a few pings, which the heartbeat server can detect through timing out.

Running the heartbeat server/client is the same as before:
```bash
$ python3 UDPHeartbeatServer.py
[in another shell]
$ python3 UDPHeartbeatClient.py
```