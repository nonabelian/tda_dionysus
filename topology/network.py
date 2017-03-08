''' Author: Dylan Albrecht
    Date: March 6, 2017

    Functions for producing a dimensional reduction, or topological network.
    So far this only includes 'circle_network' which yields a networkx graph
    with labels colored by given binary classification.

    TODO:
        * Work on having better layout.
        * Add more label schemes.
        * Think of how to best represent persistence.

'''

import networkx as nx


def circle_network(dynamic_persistence, smap, evaluator, labels=None):
    ''' Creates a topological netowrk, based on the persistent features found
        in the data.
        INPUT: 
        OUTPUT: nx.Graph, list (colors of nodes)

        Example:
            >>> g, c = circle_network(dp, smap, rips.eval, labels=y)
            >>> pos = nx.spring_layout(graphs)
            >>> nx.draw_networkx(graphs, node_color=colors, pos=pos)

        TODO: Fix to better represent the 'bubbling'
    '''
    graph = nx.Graph()
    colors_dict = dict()

    label_colors = {0: 'b', 1: 'r'}

    for sigma in dynamic_persistence:
        if not sigma.sign():
            bd = evaluator(smap[sigma]) - evaluator(smap[sigma.pair()])

            if bd < 0.001: continue

            cycle = [smap[ii] for ii in sigma.cycle]
            chain = [smap[ii] for ii in sigma.chain]
            if not cycle or not chain: continue

            dim = chain[0].dimension()

            for s in cycle:
                pair_vertices = [v for v in s.vertices]

                if len(pair_vertices) > 1:
                    v1 = pair_vertices[0]
                    v2 = pair_vertices[1]
                    graph.add_edge(v1, v2, weight=1/(evaluator(s) + 0.1))

                    if labels is not None:
                        colors_dict[v1] = label_colors[labels[v1]]
                        colors_dict[v2] = label_colors[labels[v2]]
                    else:
                        colors_dict[v1] = 'b' if dim == 1 else 'r'
                        colors_dict[v2] = 'b' if dim == 1 else 'r'
                elif len(pair_vertices) == 1:
                    v = pair_vertices[0]
                    graph.add_node(v)

                    if labels is not None:
                        colors_dict[v] = label_colors[labels[v]]
                    else:
                        colors_dict[v] = 'b' if dim == 1 else 'r'

    disconnected_indices = [i for i,n in enumerate(graph.adjacency_list())
                              if not n]
    connected_indices = [i for i,n in enumerate(graph.adjacency_list())
                           if n]

    start_connector = disconnected_indices[0]
    for idx in disconnected_indices[1:]:
        graph.add_edge(start_connector, idx, weight=10)

    graph.add_edge(connected_indices[0], idx, weight=0.1)

    colors = [colors_dict[n] for n in graph.nodes()]

    return graph, colors
