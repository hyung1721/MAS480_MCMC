# -*- coding: utf-8 -*-
"""

MAS480 Mathematics and AI
Homework 3 - Problem (1) Metropolis-Hasting Algorithm
20180127 Woojin Kim

"""

import graph
import sampling as sp

def construct_markov_chain_MH(g):
    edges = g.edges()
    
    r = 10 # max number of edges in G
    
    for edge in edges:
        (i, j) = edge.endpoints()
        if i == j:
            continue
        else:
            pi_i = g.get_target_dist(i.state())
            pi_j = g.get_target_dist(j.state())
            
            # Update transition probability
            edge.update_edge(min(1, pi_j / pi_i) / r)
    
    for edge in edges:
        (i, j) = edge.endpoints()
        if i == j:
            sum_pi = 0
            for incident_edge in g.incident_edges(i):
                sum_pi += incident_edge.get_prob()
            edge.update_edge(1-sum_pi)

if __name__ == "__main__":
    state_list = [1, 2, 3, 4]
    G = graph.generate_Graph(state_list)
    graph.init_target_stationary_distribution(G)
    construct_markov_chain_MH(G)
    
    # Problem a
    # With the initial point (1, 1, 1), do the sampling with
    # length 10.
    print("### Metropolis-Hasting Algorithm ####")
    print('########## Problem (1) - a ##########')
    print('')
    sp.sampling(G, (1, 1, 1), 10, 1, printable = True)
    print('')
    
    # Problem b
    # With the initial point (1, 1, 1), do the sampling 100 times 
    # with length 500.
    samples = sp.sampling(G, (1, 1, 1), 500, 100, printable = False)
    
    # Problem c
    # Compare the target probability mass function with empirical long-term
    # average probability distribution.
    list_t = [2, 10, 50, 100, 200, 300, 400, 500]
    long_term_averages = sp.calculate_long_term_averages(list_t, samples, 500)
    target_dist = G.target_distribution()
    
    print('########## Problem (1) - c ##########\n')
    for index in range(len(long_term_averages)):
        sp.compare_average_and_target(long_term_averages[index], target_dist, list_t[index])
    