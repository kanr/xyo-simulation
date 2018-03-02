import node

if __name__ == '__main__':
    cartelIDs = [1, 3]
    nodes = [
        node.Node(0, 0),
        node.CartelNode(1, 1, cartelIDs),
        node.Node(2, 2),
        node.CartelDeceptionNode(3, 3, cartelIDs),
        node.Node(4, 4)
    ]

    for n in nodes:
        n.connect_with_nearby_nodes(nodes)

    for n0 in nodes:
        for n1 in nodes:
            if n0.id != n1.id:
                print(n0.id, n1.id, n0.subjective_credibility(n1))

