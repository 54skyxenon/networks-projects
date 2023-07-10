#include <stdio.h>
#include "network.h"

extern int TRACE;
extern int YES;
extern int NO;

int connectcosts3[4] = {7, INFINITY, 2, 0};

distance_table dt3;

/* students to write the following two routines, and maybe some others */

void rtinit3() {
  printf("rtinit3 called!\n");

  for (int i = 0; i < 4; i++) {
    for (int j = 0; j < 4; j++) {
      dt3.costs[i][j] = INFINITY;
    }
  }

  for (int adj = 0; adj < 4; adj++) {
    dt3.costs[3][adj] = dt3.costs[adj][3] = connectcosts3[adj];
  }

  // Send its directly-connected neighbors the cost of it minimum cost paths
  for (int adj = 0; adj < 4; adj++) {
    if (adj != 3) {
      rtpkt *pkt = (rtpkt *)malloc(sizeof(rtpkt *));
      creatertpkt(pkt, 3, adj, connectcosts3);
      tolayer2(*pkt);
    }
  }
}

void rtupdate3(rtpkt *rcvdpkt) {
  printf("rtupdate3 called!\n");
}

void printdt3(distance_table *dtptr) {
  printf("             via     \n");
  printf("   D3 |    0     2 \n");
  printf("  ----|-----------\n");
  printf("     0|  %3d   %3d\n", dtptr->costs[0][0], dtptr->costs[0][2]);
  printf("dest 1|  %3d   %3d\n", dtptr->costs[1][0], dtptr->costs[1][2]);
  printf("     2|  %3d   %3d\n", dtptr->costs[2][0], dtptr->costs[2][2]);
}