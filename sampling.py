# -*- coding: utf-8 -*-
"""

MAS480 Mathematics and AI
Homework 3 - Module for Sampling and Comparing result
20180127 Woojin Kim

"""
import numpy as np
import pandas as pd

def sampling(g, initial_point, length, num, printable = True):
    all_samples = []
    
    while num > 0:
        current_state = g.get_state(initial_point)
        sample_result = []
        iter_length = length
        
        while iter_length > 0:
            sample_result.append(current_state.state())
            #print("current state: ", current_state.state())
            edges = g.get_incident_edges(current_state)
            
            transition_state = []
            transition_prob  = []
            
            for edge in edges:
                transition_state.append(edge.opposite(current_state))
                transition_prob.append(edge.get_prob())
            
            #print("incident states: ", [state.state() for state in transition_state])
            #print("transition prob: ", transition_prob)
            current_state = np.random.choice(transition_state, 1, replace = True, p = transition_prob)[0]
            iter_length -= 1
        
        all_samples.append(tuple(sample_result))
        num -= 1
    
    if printable:
        for sample in all_samples:
            print(sample)
    
    return all_samples

def generate_distribution():
    state_list = [1, 2, 3, 4]
    num_states = len(state_list)
    distribution = {}
    
    for i in range(1, num_states + 1):
        for j in range(1, num_states + 1):
            for k in range(1, num_states + 1):
                distribution[(i, j, k)] = 0
    
    return distribution

def empirical_distribution(dist, samples, t, total_num):
    for sample in samples:
        count = 0
        
        for state in sample:
            dist[state] = dist.get(state, 0) + (1 / total_num)
            
            if count == t:
                break
            
            count += 1
    
    return dist

def long_term_average(t, samples):
    result_dist = generate_distribution()
    
    for current_t in range(t):
        
        dist = generate_distribution()
        total_num = len(samples) * (current_t + 1)
        empirical_dist_with_t = empirical_distribution(dist, samples, current_t, total_num)
        
        for state in result_dist.keys():
            result_dist[state] += empirical_dist_with_t[state] / t
    
    return result_dist

def calculate_long_term_averages(list_t, samples, sample_size):
    result = []
    
    for t in list_t:
        
        if t > sample_size:
            raise ValueError("t must not be greater than sample size")
        
        average_prob_dist = long_term_average(t, samples)
        result.append(average_prob_dist)
    
    return result

def compare_average_and_target(average_dist, target_dist, t):
    plot1 = pd.DataFrame([average_dist]).T.plot.line(color = 'blue', legend = False)
    plot2 = pd.DataFrame([target_dist]).T.plot.line(ax = plot1, color = 'red', legend = False)

    plot2.set_xlabel('State')
    plot2.set_ylabel('Probability')
    
    plot2.set_title('Comparing empirical long-term(blue) a(' + str(t) + ') with target(red)')
    plot2.set_ylim((0, 0.1))
    
    print('The L1 loss of empirical long-term distribution a(' + str(t) + ') is:')
    
    error = 0
    for state in average_dist.keys():
        error += abs(average_dist[state] - target_dist[state])
    print(error)
