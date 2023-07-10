#ifndef NETWORK_H
#define NETWORK_H

// distance_vector.c
typedef struct rtpkt rtpkt;
typedef struct event event;
void init();
void creatertpkt(rtpkt*, int, int, int[]);
void insertevent(event*);
void tolayer2(rtpkt);

// Across all nodes
typedef struct distance_table {
  int costs[4][4];
} distance_table;

// node0.c
void rtinit0();
void rtupdate0(rtpkt*);
void linkhandler0(int, int);

// node1.c
void rtinit1();
void rtupdate1(rtpkt*);
void linkhandler1(int, int);

// node2.c
void rtinit2();
void rtupdate2(rtpkt*);

// node3.c
void rtinit3();
void rtupdate3(rtpkt*);

#endif /* NETWORK_H */