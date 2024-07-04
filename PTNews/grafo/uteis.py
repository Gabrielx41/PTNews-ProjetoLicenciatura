import networkx as nx
import matplotlib
matplotlib.use('Agg')

def build_graph_for_keyword(inverted_index, target_word, top_cooccurrences):
    G = nx.Graph()
    
    # Add the main keyword as a node
    G.add_node(target_word)
    
    # Add top co-occurring keywords and edges
    for co_word, count in top_cooccurrences:
        G.add_node(co_word)
        G.add_edge(target_word, co_word, weight=count)
        
    data = nx.readwrite.json_graph.node_link_data(G)
    
    return data