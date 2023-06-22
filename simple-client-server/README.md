# Basic Socket Programming

### Purpose

Demonstrates a basic client/server socket interaction.

### Usage

Start the server like so:
```bash
$ python3 server.py
```

Then start the client:
```bash
$ python3 client.py
```

### Interaction

1. The client asks for a number from 1 to 100 to transmit to the server.

2. The server reciprocates with a number from 1 to 100.
   
3. Both hosts display the sum of the two numbers.

Once a number out of range is received by the client, both host processes exit.