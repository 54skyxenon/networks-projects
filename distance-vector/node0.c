#include <stdio.h>
#include "network.h"

extern int TRACE;
extern int YES;
extern int NO;

distance_table dt0;

/* students to write the following two routines, and maybe some others */

void rtinit0()
{
  printf("rtinit0 called!\n");
}

void rtupdate0(rtpkt *rcvdpkt)
{
}

void printdt0(distance_table *dtptr)
{
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

void linkhandler0(int linkid, int newcost)
/* called when cost from 0 to linkid changes from current value to newcost*/
/* You can leave this routine empty if you're an undergrad. If you want */
/* to use this routine, you'll need to change the value of the LINKCHANGE */
/* constant definition in prog3.c from 0 to 1 */
{
}