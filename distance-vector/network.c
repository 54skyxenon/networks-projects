#include "network.h"

// Generalized routing table initialization (DRY) 
void rtinit(int target, distance_table *dt, const int connectcosts[]) {
  printf("rtinit%d called!\n", target);

  for (int i = 0; i < 4; i++) {
    for (int j = 0; j < 4; j++) {
      dt->costs[i][j] = INFINITY;
    }
  }

  for (int adj = 0; adj < 4; adj++) {
    dt->costs[target][adj] = dt->costs[adj][target] = connectcosts[adj];
  }

  propagate(target, connectcosts);
}

// Send its directly-connected neighbors the cost of its minimum cost paths
void propagate(int from, const int costs[]) {
  for (int adj = 0; adj < 4; adj++) {
    rtpkt *pkt = (rtpkt *)malloc(sizeof(rtpkt));
    creatertpkt(pkt, from, adj, costs);
    tolayer2(*pkt);
    free(pkt);
  }
}

// Update the distance vectors with Bellman-Ford
// Returns 1 if routing table was changed, 0 otherwise
int dtupdate(rtpkt *rcvdpkt, distance_table *dt) {
  int changed = NO;
  int src = rcvdpkt->sourceid;

  for (int dest = 0; dest < 4; dest++) {
    int new_cost = rcvdpkt->mincost[dest];
    if (new_cost < dt->costs[src][dest]) {
      dt->costs[src][dest] = dt->costs[dest][src] = new_cost;
      changed = YES;
    }
  }
  
  for (int i = 0; i < 4; i++) {
    for (int j = 0; j < 4; j++) {
      int new_cost = dt->costs[i][src] + dt->costs[src][j];
      if (new_cost < dt->costs[i][j]) {
        dt->costs[i][j] = dt->costs[j][i] = new_cost;
        changed = YES;
      }
    }
  }

  return changed;
}

// Send a message to all of the nodes asking for reinitialization
void resetall() {
  rtinit0();
  rtinit1();
  rtinit2();
  rtinit3();
}