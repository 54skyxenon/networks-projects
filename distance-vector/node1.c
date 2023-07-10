#include <stdio.h>
#include "network.h"

extern int TRACE;
extern int YES;
extern int NO;

int connectcosts1[4] = {1, 0, 1, INFINITY};

distance_table dt1;

/* students to write the following two routines, and maybe some others */

void rtinit1() {
  printf("rtinit1 called!\n");

  for (int i = 0; i < 4; i++) {
    for (int j = 0; j < 4; j++) {
      dt1.costs[i][j] = INFINITY;
    }
  }

  for (int adj = 0; adj < 4; adj++) {
    dt1.costs[1][adj] = dt1.costs[adj][1] = connectcosts1[adj];
  }

  // Send its directly-connected neighbors the cost of it minimum cost paths
  for (int adj = 0; adj < 4; adj++) {
    if (adj != 1) {
      rtpkt *pkt = (rtpkt *)malloc(sizeof(rtpkt *));
      creatertpkt(pkt, 1, adj, connectcosts1);
      tolayer2(*pkt);
    }
  }
}

void rtupdate1(rtpkt *rcvdpkt) {
  printf("rtupdate1 called!\n");
}

void printdt1(distance_table *dtptr) {
  printf("             via   \n");
  printf("   D1 |    0     2 \n");
  printf("  ----|-----------\n");
  printf("     0|  %3d   %3d\n", dtptr->costs[0][0], dtptr->costs[0][2]);
  printf("dest 2|  %3d   %3d\n", dtptr->costs[2][0], dtptr->costs[2][2]);
  printf("     3|  %3d   %3d\n", dtptr->costs[3][0], dtptr->costs[3][2]);
}

void linkhandler1(int linkid, int newcost) {
/* called when cost from 1 to linkid changes from current value to newcost*/
/* You can leave this routine empty if you're an undergrad. If you want */
/* to use this routine, you'll need to change the value of the LINKCHANGE */
/* constant definition in prog3.c from 0 to 1 */
}