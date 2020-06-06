from tree_node import TreeNode

class LeafNode(TreeNode):
    def __init__(self, classification):
        self._classification = classification

    def classify(self, object):
        return self._classification

    def __len__(self):
        return 1

    def __str__(self):
        return ""

    def _get_node_name(self):
        return self._classification