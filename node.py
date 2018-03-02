import datetime


class Node:
    def __init__(self, loc, id):
        self.chain = []  # The Proof of Origin chain on the node
        self.loc = loc  # The 1D location of the node
        self.id = id  # The ID of the node (parallel of XYO address)
        self.radius = 1  # The max radius of Bluetooth connections
        self.choosyNodeScores = {}  # A dict of how "choosy" each node is

    # Connects to all nodes within radius
    def connect_with_nearby_nodes(self, nodes):
        for node in nodes:
            if abs(node.loc - self.loc) <= self.radius and node.id != self.id:
                node.hs1(node)

    # Handshake step 1
    def hs1(self, node):
        node.hs2(self, node.loc - self.loc)

    # Handshake step 2
    def hs2(self, node, dist):
        if dist == self.loc - node.loc:
            packet = node.hs3(self)
            if packet is not None:
                # Got new packet
                self.chain.append(packet)
            else:
                # Choosy node, penalize
                if node.id not in self.choosyNodeScores.keys():
                    self.choosyNodeScores[node.id] = 0
                self.choosyNodeScores[node.id] += 1

    # Handshake step 3
    def hs3(self, node):
        packet = (datetime.datetime.now(), self.id, node.id, node.loc - self.loc)
        self.chain.append(packet)  # Add new packet
        return packet

    # Returns the perceived credibility of another node
    def subjective_credibility(self, node):
        cScore = 0 if node.id not in self.choosyNodeScores.keys() else self.choosyNodeScores[node.id]
        return len(node.chain) - cScore


class CartelNode(Node):
    def __init__(self, loc, id, buddyIDs):
        super().__init__(loc, id)
        self.buddyIDs = buddyIDs

    # Only connects with nodes in the same cartel as itself
    def hs3(self, node):
        if node.id not in self.buddyIDs:
            return None
        return super().hs3(node)


class CartelDeceptionNode(CartelNode):
    # Only connects with nodes not in the same cartel as itself
    def hs3(self, node):
        if node.id in self.buddyIDs:
            return None
        return super().hs3(node)
