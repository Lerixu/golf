"""
Introduction to Web Science
Assignment 9
Team : golf

"""
import pandas as pd

store = pd.HDFStore('store2.h5')
df2=store['df2']
# we transform the list of outlinks into a set
df2['out_links_unique']=df2.out_links.apply(lambda x:set(x))
graph=df2.set_index("name")["out_links_unique"].to_dict()

# Using breath first search algorithm to get all paths
def bfs_paths( start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        try:
            for next in graph[vertex] - set(path):
                if next == goal:
                    yield path + [next]
                else:
                    queue.append((next, path + [next]))
        except KeyError:
            pass
# the shortest path is the first element returned by bfs_path
def shortest_path_len( start, goal):
    try:
        return len(next(bfs_paths( start, goal)))
    except StopIteration:
        return None
               
def find_diameter():
    # we get the verticies
    v = list(graph.keys())
    smallest_path_lens = []
    # looping on all possible pairs
    for i in range(len(v)-1) :
        for j in range(i+1, len(v)):
            # we store the lenghts
            len_shortest_path =shortest_path_len(v[i],v[j])
            smallest_path_lens.append(len_shortest_path)
    # the maximum lenght of all shortest paths between every possible pair
    # of vertices is the diameter
    diameter =max(smallest_path_lens)
    return diameter
    
# We still have some memory issues, this is working on smaller graphs
# but we run into memory erros on the store.h5 df2 graph
print(find_diameter())

