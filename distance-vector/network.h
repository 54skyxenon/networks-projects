#ifndef NETWORK_H
#define NETWORK_H

#include <stdlib.h>
#include <string.h>

#define INFINITY 999

// distance_vector.c
/* a rtpkt is the packet sent from one routing update process to
   another via the call tolayer3() */
typedef struct rtpkt
{
  int sourceid;   /* id of sending router sending this pkt */
  int destid;     /* id of router to which pkt being sent (must be an immediate neighbor) */
  int mincost[4]; /* min cost to node 0 ... 3 */
} rtpkt;

typedef struct event event;
void init();
void creatertpkt(rtpkt *, int, int, int[]);
void insertevent(event *);
void tolayer2(rtpkt);

// Across all nodes
typedef struct distance_table
{
  int costs[4][4];
} distance_table;

// node0.c
void rtinit0();
void rtupdate0(rtpkt *);
void printdt0(distance_table *);
void linkhandler0(int, int);

// node1.c
void rtinit1();
void rtupdate1(rtpkt *);
void printdt1(distance_table *);
void linkhandler1(int, int);

// node2.c
void rtinit2();
void rtupdate2(rtpkt *);
void printdt2(distance_table *);

// node3.c
void rtinit3();
void rtupdate3(rtpkt *);
void printdt3(distance_table *);

#endif /* NETWORK_H */