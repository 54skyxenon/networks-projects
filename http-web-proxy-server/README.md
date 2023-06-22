# HTTP Web Proxy Server

### Purpose

Sits between the client and origin server when receiving requests, and also caches webpages for performance. This only supports ordinary GET and POST requests.

### Running

To start the server, assuming you want port 8888:
```bash
$ python3 ProxyServer.py 8888
```

The cache is built under the local `cached/` directory. You can put the included `favicon.ico` under the `cached/` for convenience.

### Examples

GET Request (visit URL in browser):
```txt
http://localhost:8888/www.google.com
```

POST Request (using CURL):
```bash
$ curl -d "param1=value1&param2=value2" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://localhost:8888/httpbin.org/post
```