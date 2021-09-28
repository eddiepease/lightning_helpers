import json
from collections import defaultdict
import pandas as pd


def read_file(file_path):
    """Code which reads the lightning network graph file"""
    with open(file_path, 'r') as j:
        graph_dict = json.loads(j.read())
    return graph_dict

# TODO: add further attributes to
def create_node_db():

    """ Create database of nodes with public key as dictionary key """

    node_db = {}
    graph_dict = read_file('describegraph.json')

    # gather data from the nodes
    for n in graph_dict['nodes']:
        pub_key = n['pub_key']
        if pub_key not in node_db:
            node_db[pub_key] = defaultdict(int)
            node_db[pub_key]['alias'] = n['alias']

    # gather data from the edges
    for e in graph_dict['edges']:
        node_db[e['node1_pub']]['num_channels'] += 1
        node_db[e['node1_pub']]['capacity'] += int(e['capacity'])
        node_db[e['node2_pub']]['num_channels'] += 1
        node_db[e['node2_pub']]['capacity'] += int(e['capacity'])

    # convert to dataframe and save to CSV
    df = pd.DataFrame.from_dict(node_db, orient='index')
    df.to_csv('nodes.csv')

if __name__ == '__main__':
    create_node_db()
