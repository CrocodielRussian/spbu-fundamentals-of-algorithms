from typing import Any

import networkx as nx
import queue
import matplotlib.pyplot as plt
from src.plotting import plot_graph

def dfs(G: nx.Graph, node: Any, visited: dict[Any], c: int, t: Any) -> int:
    if node == t:
        return c
    
    delta = 0
    visited[node] = True      
    for neigh in G.neighbors(node):
        if not visited[neigh] and G[node][neigh]['weight'] > 0:
            delta = dfs(G, neigh, visited, min(c, G[node][neigh]['weight']), t) 
            if delta > 0:
                visited[neigh] = False
                G[node][neigh]['weight'] -= delta
                G[neigh][node]['weight'] += delta
                return delta
    return delta

def max_flow(G: nx.Graph, s: Any, t: Any) -> int:
    value: int = 0
    
    c = 34 # Some threshold value for weight of edge 

    edges = []
    for u, v in G.edges():
        edges.append((v, u, 0))
    G.add_weighted_edges_from(edges)

    stack = [s]
    path = []
    min_edge = 1000
    while len(stack) > 0 and c > 0:
        node = stack.pop()
        if node == t:
            print(path)
            for i in range(1, len(path)):
                u = path[i-1]
                v = path[i]
            
            G[u][v]["weight"] -= min_edge
            G[v][u]["weight"] += min_edge
            
            value += min_edge
            
            stack.clear()
            path.clear()
            min_edge = 1000

            stack.append(s)
            node = s
        flag = True
        path.append(node)
        while flag and c > 0: 
            for neigh in G.neighbors(node):
                if not neigh in path and G[node][neigh]['weight'] > c:
                    min_edge = min(min_edge, G[node][neigh]['weight'])
                    stack.append(neigh)
                    flag = False
                    break
            if flag:
                c //= 2

    return value


if __name__ == "__main__":
    # Load the graph
    G = nx.read_edgelist("practicum_3/homework/advanced/graph_2.edgelist", create_using=nx.DiGraph)
    
    
    edges = []
    for u, v in G.edges():
        edges.append((v, u, 0))
    G.add_weighted_edges_from(edges)

    for u, v in G.edges():
        print(f"{u} {v} {G[u][v]['weight']}")

    print()

    ans = 0
    val = 100
    visited = {n: 0 for n in G}
    
    val = dfs(G, node = '1', visited = visited, c = 30, t = '6')
    
    for u, v in G.edges():
        print(f"{u} {v} {G[u][v]['weight']}")

    plot_graph(G)
    ans += val

    print(f"Maximum flow is {ans}. Should be 23")