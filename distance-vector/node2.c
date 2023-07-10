#include <stdio.h>
#include "network.h"

extern int TRACE;
extern int YES;
extern int NO;

int connectcosts2[4] = {3, 1, 0, 2};

distance_table dt2;

/* students to write the following two routines, and maybe some others */

void rtinit2() {
  printf("rtinit2 called!\n");

  for (int i = 0; i < 4; i++) {
    for (int j = 0; j < 4; j++) {
      dt2.costs[i][j] = INFINITY;
    }
  }

  for (int adj = 0; adj < 4; adj++) {
    dt2.costs[2][adj] = dt2.costs[adj][2] = connectcosts2[adj];
  }

  // Send its directly-connected neighbors the cost of it minimum cost paths
  for (int adj = 0; adj < 4; adj++) {
    if (adj != 2) {
      rtpkt *pkt = (rtpkt *)malloc(sizeof(rtpkt *));
      creatertpkt(pkt, 2, adj, connectcosts2);
      tolayer2(*pkt);
    }
  }
}

void rtupdate2(rtpkt *rcvdpkt) {
  printf("rtupdate2 called!\n");
}

void printdt2(distance_table *dtptr) {
  printf("                via     \n");
  printf("   D2 |    0     1    3 \n");
  printf("  ----|-----------------\n");
  printf("     0|  %3d   %3d   %3d\n", dtptr->costs[0][0],
         dtptr->costs[0][1], dtptr->costs[0][3]);
  printf("dest 1|  %3d   %3d   %3d\n", dtptr->costs[1][0],
         dtptr->costs[1][1], dtptr->costs[1][3]);
  printf("     3|  %3d   %3d   %3d\n", dtptr->costs[3][0],
         dtptr->costs[3][1], dtptr->costs[3][3]);
}