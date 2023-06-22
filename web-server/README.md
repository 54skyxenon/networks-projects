# Web Server

### Purpose

A multithreaded, vanilla HTTP Web Server. This parses an HTTP request for a local file and sends back a HTTP response.

### Usage

First, start the server:
```bash
$ python3 http-server.py
```

The server listens on port 6789, so fire up a web browser and visit `http://localhost:6789/HelloWorld.html`

A 404 page is displayed if a requested file isn't found. Feel free to test by adding your own HTML files!


### Custom Client

Also included is a custom HTTP client you can try:

```bash
$ python3 http-client.py localhost 6789 /HelloWorld.html
```

Spawning multiple instances of the client is useful for testing high concurrency.