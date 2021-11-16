from igraph import *
import numpy



def draw(x,g):
    """Draw the graph with vertices and edges labeled"""
    ## Retrieve vertex labels from ac_solver output
    labels = [y for _,y in sorted([(int(a[1:]),b) for a,b in x.items() if a[0] == 'v'],key=lambda z:z[0])]
    print(labels)
    g.vs["label"] = labels #= [x[i] for i in range(g.vcount())]
    g.vs['color'] = ['dark sea green']
    edges = g.get_edgelist()
    g.es['label'] = [str(abs(labels[edges[i][0]] - labels[edges[i][1]])) for i in range(g.ecount())]
    plot(g)


def load_graph(fd):
    g = Graph.Read(fd)
    g.to_undirected()
    return g

