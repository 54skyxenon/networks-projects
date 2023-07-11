#include "network.h"

extern int TRACE;
extern int YES;
extern int NO;

const int connectcosts3[4] = {7, INFINITY, 2, 0};

distance_table dt3;

/* students to write the following two routines, and maybe some others */

void rtinit3() {
  rtinit(3, &dt3, connectcosts3);
}

void rtupdate3(rtpkt *rcvdpkt) {
  printf("rtupdate3 called!\n");

  if (dtupdate(rcvdpkt, &dt3)) {
    propagate(3, dt3.costs[3]);
  }
  printdt3(&dt3);
}

void printdt3(distance_table *dtptr) {
  printf("             via     \n");
  printf("   D3 |    0     2 \n");
  printf("  ----|-----------\n");
  printf("     0|  %3d   %3d\n", dtptr->costs[0][0], dtptr->costs[0][2]);
  printf("dest 1|  %3d   %3d\n", dtptr->costs[1][0], dtptr->costs[1][2]);
  printf("     2|  %3d   %3d\n", dtptr->costs[2][0], dtptr->costs[2][2]);
}