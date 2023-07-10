#include <stdio.h>
#include "network.h"

extern int TRACE;
extern int YES;
extern int NO;

int connectcosts0[4] = {0, 1, 3, 7};

distance_table dt0;

/* students to write the following two routines, and maybe some others */

void rtinit0() {
  printf("rtinit0 called!\n");

  for (int i = 0; i < 4; i++) {
    for (int j = 0; j < 4; j++) {
      dt0.costs[i][j] = INFINITY;
    }
  }

  for (int adj = 0; adj < 4; adj++) {
    dt0.costs[0][adj] = dt0.costs[adj][0] = connectcosts0[adj];
  }

  // Send its directly-connected neighbors the cost of it minimum cost paths
  for (int adj = 0; adj < 4; adj++) {
    if (adj != 0) {
      rtpkt *pkt = (rtpkt *)malloc(sizeof(rtpkt *));
      creatertpkt(pkt, 0, adj, connectcosts0);
      tolayer2(*pkt);
    }
  }
}

void rtupdate0(rtpkt *rcvdpkt) {
  printf("rtupdate0 called!\n");
}

void printdt0(distance_table *dtptr) {
  printf("                via     \n");
  printf("   D0 |    1     2    3 \n");
  printf("  ----|-----------------\n");
  printf("     1|  %3d   %3d   %3d\n", dtptr->costs[1][1],
         dtptr->costs[1][2], dtptr->costs[1][3]);
  printf("dest 2|  %3d   %3d   %3d\n", dtptr->costs[2][1],
         dtptr->costs[2][2], dtptr->costs[2][3]);
  printf("     3|  %3d   %3d   %3d\n", dtptr->costs[3][1],
         dtptr->costs[3][2], dtptr->costs[3][3]);
}

void linkhandler0(int linkid, int newcost) {
/* called when cost from 0 to linkid changes from current value to newcost*/
/* You can leave this routine empty if you're an undergrad. If you want */
/* to use this routine, you'll need to change the value of the LINKCHANGE */
/* constant definition in prog3.c from 0 to 1 */
}