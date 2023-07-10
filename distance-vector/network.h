#ifndef NETWORK_H
#define NETWORK_H

// distance_vector.c
struct rtpkt;
struct event;
void init();
void creatertpkt(struct rtpkt*, int, int, int[]);
void insertevent(struct event*);
void tolayer2(struct rtpkt);

// Across all nodes
struct distance_table {
  int costs[4][4];
};

// node0.c
void rtinit0();
void rtupdate0(struct rtpkt*);
void linkhandler0(int, int);

// node1.c
void rtinit1();
void rtupdate1(struct rtpkt*);
void linkhandler1(int, int);

// node2.c
void rtinit2();
void rtupdate2(struct rtpkt*);

// node3.c
void rtinit3();
void rtupdate3(struct rtpkt*);

#endif /* NETWORK_H */