#include "network.h"

extern int TRACE;

const int connectcosts1[4] = {1, 0, 1, INFINITY};

distance_table dt1;

/* students to write the following two routines, and maybe some others */

void rtinit1() {
  rtinit(1, &dt1, connectcosts1);
}

void rtupdate1(rtpkt *rcvdpkt) {
  printf("rtupdate1 called!\n");

  if (dtupdate(rcvdpkt, &dt1)) {
    propagate(1, dt1.costs[1]);
  }
  printdt1(&dt1);
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