import datetime


class Node:
    def __init__(self, loc, id):
        self.chain = []  # The Proof of Origin chain on the node
        self.loc = loc  # The 1D location of the node
        self.id = id  # The ID of the node (parallel of XYO address)
        self.radius = 2  # The max radius of Bluetooth connections
        self.choosyNodeScores = {}  # A dict of how "choosy" each node is

    # Connects to all nodes within radius
    def connect_with_nearby_nodes(self, nodes):
        for node in nodes:
            if abs(node.loc - self.loc) <= self.radius:
                self.hs1(node)

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

    @staticmethod
    def packet_equals(packet1, packet2):
        return packet1[0] == packet2[0] \
               and ((packet1[1] == packet2[1] and packet1[2] == packet2[2] and packet1[3] == packet2[3])
                    or (packet1[1] == packet2[2] and packet1[2] == packet2[1] and packet1[3] == -packet2[3]))

    @staticmethod
    def packet_conflicts(packet1, packet2):
        return packet1[0] == packet2[0] \
               and ((packet1[1] == packet2[1] and packet1[2] == packet2[2] and packet1[3] != packet2[3])
                    or (packet1[1] == packet2[2] and packet1[2] == packet2[1] and packet1[3] != -packet2[3]))

    def overlap_with_network(self, nodes):
        overlap = 1e-10
        for node in nodes:
            for packet1 in node.chain:
                for packet2 in self.chain:
                    if self.packet_equals(packet1, packet2):
                        overlap += 1
        return overlap

    def conflicts_with_network(self, nodes):
        conflicts = 0
        for node in nodes:
            for packet1 in node.chain:
                for packet2 in self.chain:
                    if self.packet_conflicts(packet1, packet2):
                        conflicts += 1
        return conflicts

    def pseudo_chain_score(self, nodes):
        return len(self.chain) * len(nodes) \
               / self.overlap_with_network(nodes) \
               - sum(map(lambda x: x.choosyNodeScores.get(self.id, 0), nodes)) \
               - self.conflicts_with_network(nodes)


class CartelNode(Node):
    def __init__(self, loc, id, buddyIDs):
        super().__init__(loc, id)
        self.buddyIDs = buddyIDs

    # Only connects with nodes in the same cartel as itself
    def hs3(self, node):
        if node.id not in self.buddyIDs:
            return None
        return super().hs3(node)


class CartelDeceptionNode(Node):
    def __init__(self, loc, id, buddyIDs):
        super().__init__(loc, id)
        self.buddyIDs = buddyIDs

    # Only connects with nodes not in the same cartel as itself
    def hs3(self, node):
        if node.id in self.buddyIDs:
            return None
        return super().hs3(node)


class LyingNode(Node):
    # Handshake step 3
    def hs3(self, node):
        packet = (datetime.datetime.now(), self.id, node.id, node.loc - self.loc + 20)
        self.chain.append(packet)  # Add new packet
        return packet
