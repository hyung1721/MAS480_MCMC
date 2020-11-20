# -*- coding: utf-8 -*-
"""

MAS480 Mathematics and AI
Homework 3 - Problem (2) Gibbs Sampling
20180127 Woojin Kim

"""
import graph
import sampling as sp

def get_diff_coordinate(coord1, coord2):
    for i in range(3):
        if coord1[i] != coord2[i]:
            return i

def construct_markov_chain_GS(g):
    edges = g.edges()

    d = 3 # dimension of state
    
    for edge in edges:
        (i, j) = edge.endpoints()
        if i == j:
            continue
        else:
            coordinate_i = i.state() # origin
            coordinate_j = j.state() # destination
            
            pi_j = g.get_target_dist(coordinate_j)
            
            # Find different coordinate's index
            diff_coordinate = get_diff_coordinate(coordinate_i, coordinate_j)
            
            # Compute marginal distribution
            temp_coordinate = list(coordinate_i)
            denominator = 0
            for new_coord in [1, 2, 3, 4]:
                temp_coordinate[diff_coordinate] = new_coord
                denominator += g.get_target_dist(tuple(temp_coordinate))
            
            # Update transition probability
            edge.update_edge(pi_j / denominator / d)
    
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
    construct_markov_chain_GS(G)
    
    # Problem a
    # With the initial point (1, 1, 1), do the sampling with
    # length 10.
    print('########## Gibbs Sampling  ##########')
    print('########## Problem (2) - a ##########')
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
    
    print('########## Problem (2) - c ##########\n')
    for index in range(len(long_term_averages)):
        sp.compare_average_and_target(long_term_averages[index], target_dist, list_t[index])
    