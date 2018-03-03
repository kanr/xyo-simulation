import node


def print_node_scores(nodes):
    for n in nodes:
        n.connect_with_nearby_nodes(list(filter(lambda x: x.id != n.id, nodes)))

    for n0 in nodes:
        print('ID:', n0.id, 'Score:', n0.pseudo_chain_score(list(filter(lambda x: x.id != n0.id, nodes))))

    print()

if __name__ == '__main__':
    cartelIDs1 = [1, 2, 4, 5]
    nodes1 = [
        node.Node(0, 0),
        node.CartelNode(1, 1, cartelIDs1),
        node.CartelDeceptionNode(2, 2, cartelIDs1),
        node.Node(3, 3),
        node.CartelDeceptionNode(4, 4, cartelIDs1),
        node.CartelNode(5, 5, cartelIDs1),
        node.Node(6, 6)
    ]

    cartelIDs2 = [1, 5]
    nodes2 = [
        node.Node(0, 0),
        node.CartelNode(1, 1, cartelIDs2),
        node.Node(2, 2),
        node.Node(3, 3),
        node.Node(4, 4),
        node.CartelNode(5, 5, cartelIDs2),
        node.Node(6, 6)
    ]

    nodes3 = [
        node.Node(0, 0),
        node.Node(1, 1),
        node.Node(2, 2),
        node.LyingNode(3, 3),
        node.Node(4, 4),
        node.Node(5, 5),
        node.Node(6, 6)
    ]

    print_node_scores(nodes1)
    print_node_scores(nodes2)
    print_node_scores(nodes3)

