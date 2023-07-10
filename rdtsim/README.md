# Reliable Transport Protocol

### Purpose

Simulation of a custom TCP-like protocol - one that can retransmit corrupted or dropped packets. Two implementations exist: the simple Alternating-Bit (AB) protocol along with the more complex and efficient Go-Back-N (GBN) protocol.

### Usage
The simulator can be run with several options:
```bash
$ python3 rdtsim-gbn.py -n 100 -d 10 -z 20 -l 0.2 -c 0.2 -v 2
```

Here is a breakdown of the above command, every option I used is optional:
- `-n 100`: 100 messages should be transmitted
- `-d 10`: mean time of arrival is 10 time units
- `-z 20`: window size (applies to GBN only) fits 20 packets
- `-l 0.2`: 20% chance of a packet getting dropped
- `-c 0.2`: 20% chance of a packet getting corrupted
- `-v 2`: output verbosity level at 2 (higher = more verbose)

You can also specify a random seed with `-s <seed>` and test out the `rdtsim-ab.py` implementation in a similar way.

### Specification
- `datastructures.py` contains message and packet APIs used by both implementations
- `rdtsim-ab.py` is the AB implementation
- `rdtsim-gbn.py` is the GBN implementation

Within the scripts, `EntityA` is the sender and `EntityB` is the receiver.

You can find finite-state machine diagrams for both implementations in section 3.4 of the [textbook](https://gaia.cs.umass.edu/kurose_ross).

_NOTE: Bidirectional transmission isn't supported by the Python simulator, but is supported in the [C template](http://gaia.cs.umass.edu/kurose/transport/prog2.c) the authors provide._
