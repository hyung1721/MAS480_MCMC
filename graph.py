# -*- coding: utf-8 -*-
"""

MAS480 Mathematics and AI
Homework 3 - Graph class definition code
20180127 Woojin Kim

"""

class Graph:
    class State:
        __slots__ = '_state'
        
        def __init__(self, x):
            self._state = x
        
        def state(self):
            return self._state
        
    class Edge:
        __slots__ = '_origin', '_destination', '_prob'
        
        def __init__(self, x, y, p):
            self._origin = x
            self._destination = y
            self._prob = p
        
        def opposite(self, x):
            return self._destination if x is self._origin else self._origin
        
        def endpoints(self):
            return (self._origin, self._destination)
        
        def get_prob(self):
            return self._prob
    
        def update_edge(self, p):
            self._prob = p
    
    def __init__(self):
        self._outgoing = {}
        self._target_dist = {}
    
    def states(self):
        return self._outgoing
    
    def edges(self):
        result = set()
        for item in self._outgoing.values():
            result.update(item.values())
        return result
    
    def target_distribution(self):
        return self._target_dist
    
    def get_state(self, coordinate):
        for state in self.states().keys():
            if state.state() == coordinate:
                return state
    
    def get_incident_edges(self, x):
        result = list(self._outgoing[x].values())
        return result
    
    def get_edge(self, x, y):
        return self._outgoing[x].get(y)
    
    def incident_edges(self, x):
        adj = self._outgoing
        for edge in adj[x].values():
            yield edge
    
    def insert_state(self, x = None):
        s = self.State(x)
        self._outgoing[s] = {}
        return s
    
    def insert_edge(self, x, y, p = None):
        e = self.Edge(x, y, p)
        self._outgoing[x][y] = e
        self._outgoing[y][x] = e
        return e
    
    def insert_target_dist(self, x, p):
        self._target_dist[x] = p
        
    def get_target_dist(self, x):
        return self._target_dist[x]
    
def check_possible_edge(state1, state2):
    result = False
    count = 0
    
    if state1[0] == state2[0]:
        count += 1
    
    if state1[1] == state2[1]:
        count += 1
    
    if state1[2] == state2[2]:
        count += 1
    
    if count >= 2:
        result = True
    
    return result
    
def generate_Graph(state_list):
    g = Graph()
    num_states = len(state_list)
    
    # Insert all possible states into graph g
    for i in range(num_states):
        for j in range(num_states):
            for k in range(num_states):
                x1 = state_list[i]
                y1 = state_list[j]
                z1 = state_list[k]
                g.insert_state((x1, y1, z1))
    
    # Insert all possible edges into graph g
    states = list(g.states().keys())
    
    for state_index in range(len(states)):
        for compare_state_index in range(state_index, len(states)):
            
            state_coordinate = states[state_index].state()
            compare_coordinate = states[compare_state_index].state()
            
            if check_possible_edge(state_coordinate, compare_coordinate):
                g.insert_edge(states[state_index], states[compare_state_index], 0)
    
    return g

def init_target_stationary_distribution(g):
    states = g.states().keys()
    
    total_prob_unnormalized = 0
    
    for i in range(1, 5):
        for j in range(1, 5):
            for k in range(1, 5):
                total_prob_unnormalized += 1/(i + j + k)
    
    normal_constant = 1 / total_prob_unnormalized
    
    for state in states:
        state_coordinate = state.state()
        
        i = state_coordinate[0]
        j = state_coordinate[1]
        k = state_coordinate[2]
        
        p = normal_constant / (i + j + k)
        g.insert_target_dist(state_coordinate, p)

if __name__ == "__main__":
    state_list = [1, 2, 3, 4]
    graph = generate_Graph(state_list)
    init_target_stationary_distribution(graph)
    
    
    
    
    
    
