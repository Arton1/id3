from abc import ABC, abstractmethod

class TreeNode(ABC):

    @abstractmethod
    def classify(self, object):
        pass

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def _get_node_name(self):
        pass