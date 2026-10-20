class SimulatedNetwork:
    def __init__(self):
        self.nodes = {}
        self.partitions = []

    def register_node(self, node_id, node):
        self.nodes[node_id] = node

    def partition(self, *groups):
        """
        Splits the network into isolated partitions.
        Messages between different groups are dropped.
        Example: network.partition([1, 2], [3, 4, 5])
        """
        self.partitions = [set(g) for g in groups]

    def heal(self):
        """Restores full network connectivity."""
        self.partitions = []

    def is_connected(self, src, dst):
        if not self.partitions:
            return True
        for group in self.partitions:
            if src in group and dst in group:
                return True
        return False

    def send_request_vote(self, src, dst, args):
        if not self.is_connected(src, dst):
            return None
        target = self.nodes.get(dst)
        if target is None:
            return None
        return target.handle_request_vote(args)

    def send_append_entries(self, src, dst, args):
        if not self.is_connected(src, dst):
            return None
        target = self.nodes.get(dst)
        if target is None:
            return None
        return target.handle_append_entries(args)
