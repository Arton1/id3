from tree_node import TreeNode

class AttributeNode(TreeNode):
    def __init__(self, attribute_number, attribute_value_with_node_pairs):
        self._attribute_index = attribute_number-1
        self._edges = attribute_value_with_node_pairs
    
    def classify(self, object_to_classify):
        object_attribute_value = object_to_classify[self._attribute_index]
        for attribute_value, node in self._edges:
            if attribute_value == object_attribute_value:
                return node.classify(object_to_classify)

    def __len__(self):
        size = 1
        for attribute_value, node in self._edges:
            size += len(node)
        return size

    def _get_node_name(self):
        return self._attribute_index+1

    def __str__(self):
        subtree_description = ""
        node_description = f"{self._get_node_name()} -> "
        for attribute_index, node in self._edges:
            if type(node) is AttributeNode:
                subtree_description += "\n" + str(node)
            node_description += f"{attribute_index}: {node._get_node_name()}, "
        return node_description[:-2] + subtree_description
