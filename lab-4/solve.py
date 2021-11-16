#!/usr/bin/python3
import sys
from CSP import *
from Graph import *

def main(graphfile):
    g = load_graph(graphfile)
    m = g.ecount()
    n = g.vcount()
    
    edges = g.es

    ## XD is a variable:domain dictionary
    XD = {}

    ## C is a list of constraints
    C = []

    ## Set the domains for the vertex variables [0,m]
    for v in range(n):
        XD["v"+str(v)] = set(range(m+1))

    ## Set the domains for the edge variables [1,m]        
    for e in range(m):
        XD["e"+str(e)] = set(range(1,m+1))
        edge = edges[e]
        source = edges[e].source
        target = edges[e].target
        C.append(Constraint(("v"+str(source),"v"+str(target),"e"+str(e)), edge_label_constraint))

    ## All-diff constraint
    C.append(Constraint(tuple(map(lambda x: "v"+str(x),range(n))),all_diff_constraint))
    C.append(Constraint(tuple(map(lambda x: "e"+str(x),range(m))),all_diff_constraint))
    
    ## Symmetry breaking constraint 
    C.append(Constraint(("v0",),is_zero))

    print(f"Graph has {m} edges and {n} vertices")

    csp = CSP(XD,C)
    x = ac_solver(csp)
    draw(x,g)

    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit(f"usage: {sys.argv[0]} <graph_file>")
    try:
        with open(sys.argv[1],'r') as file:
            main(file)
            file.close()
    except IOError as e:
        exit(f"failed to open file '{sys.argv[1]}': {str(e)}")

    
