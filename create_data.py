import sys
import networkx as nx
import random

def greedy_spanner(G, r):
  G_S = nx.Graph()
  for a, b, data in sorted(G.edges(data=True), key=lambda x: x[2]['weight']):
    #print('{a} {b} {w}'.format(a=a, b=b, w=data['weight']))
    if not (a in G_S.nodes() and b in G_S.nodes() and nx.has_path(G_S, a, b)):
      G_S.add_weighted_edges_from([(a, b, G.get_edge_data(a, b)['weight'])])
    else:
      sp = nx.shortest_path_length(G_S, a, b, 'weight')
      if r*data['weight'] < sp:
        G_S.add_weighted_edges_from([(a, b, G.get_edge_data(a, b)['weight'])])
  return G_S

def verify_spanner_with_checker(G_S, G, all_pairs, check_stretch, param):
        for i in range(len(all_pairs)):
                if not (all_pairs[i][0] in G_S.nodes() and all_pairs[i][1] in G_S.nodes()):
                        return False
                if not nx.has_path(G_S, all_pairs[i][0], all_pairs[i][1]):
                        return False
                sp = nx.shortest_path_length(G, all_pairs[i][0], all_pairs[i][1], 'weight')
                #if not check_stretch(nx.dijkstra_path_length(G_S, all_pairs[i][0], all_pairs[i][1]), sp, param):
                if not check_stretch(nx.shortest_path_length(G_S, all_pairs[i][0], all_pairs[i][1], 'weight'), sp, param):
                        return False
        return True

def all_pairs_from_subset(s):
        all_pairs = []
        for i in range(len(s)):
                for j in range(i+1, len(s)):
                        p = []
                        p.append(s[i])
                        p.append(s[j])
                        all_pairs.append(p)
        return all_pairs

def multiplicative_check(subgraph_distance, actual_distance, multiplicative_stretch):
        if subgraph_distance <= multiplicative_stretch*actual_distance:
                return True
        return False


file_name = sys.argv[1]
data_size = int(sys.argv[2])

f = open(file_name, 'w')
# Generate graphs
for i in range(data_size):
  #n = 4
  n = 10
  # for now we have kept the graphs pretty dense, because the graphs are small
  param1 = .5
  G = nx.generators.random_graphs.erdos_renyi_graph(n,param1)
  G_W = nx.Graph()
  for (u, v) in G.edges():
    G_W.add_weighted_edges_from([(u, v, 1)])
  G = G_W
  #print(G.nodes())
  #print(G.edges())
  dt = []
  for j in range(n):
    for k in range(j+1, n):
      dt.append(1 if ((j, k) in G.edges() or (k, j) in G.edges()) else 0)
  #print(" ".join([str(x) for x in dt]))
  # compute greedy spanner, remove some edges so that its not a spanner any more, add two entries, one with the spanner and the other that is not spanner
  param = 2
  G_S = greedy_spanner(G, param)
  #print(G_S.edges())
  dtg = []
  for j in range(n):
    for k in range(j+1, n):
      dtg.append(1 if ((j, k) in G_S.edges() or (k, j) in G_S.edges()) else 0)
  ver_arr = [v for v in G.nodes()]
  while verify_spanner_with_checker(G_S, G, all_pairs_from_subset(ver_arr), multiplicative_check, param):
    # randomly remove an edge
    r = random.randint(0, len(G_S.edges())-1)
    edgs = [(u, v) for (u, v) in G_S.edges()]
    (u, v) = edgs[r]
    #print(edgs, r)
    G_S.remove_edge(u, v)
  dtng = []
  for j in range(n):
    for k in range(j+1, n):
      dtng.append(1 if ((j, k) in G_S.edges() or (k, j) in G_S.edges()) else 0)
  f.write("".join([str(x) for x in dt]) + "".join([str(x) for x in dtg]) + '1' + '\n')
  f.write("".join([str(x) for x in dt]) + "".join([str(x) for x in dtng]) + '0' + '\n')
f.close()
