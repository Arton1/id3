import math
import enum
import random
from attribute_node import AttributeNode
from leaf_node import LeafNode


class Id3TreeBuilder:
    class TestType(enum.Enum):
        CLASSIC = 0
        TOURNAMENT = 1

    def __init__(self, data_set, test_type):
        self._test_type = test_type
        self._root = self._create_subtree(data_set, list(range(1, len(data_set[0])-1)))

    def get_tree(self):
        return self._root

    def _create_subtree(self, data_list, avaliable_attributes):
        if len(avaliable_attributes) == 0:
            class_frequencies = self._calculate_class_frequencies(data_list)
            class_name, frequency = max(class_frequencies, key=lambda class_frequency_tuple: class_frequency_tuple[1])
            return LeafNode(class_name)
        if self._is_pure(data_list):
            return LeafNode(self._get_first_object_class_name(data_list))
        attribute_number = self._get_attribute_to_split_on(data_list, avaliable_attributes)
        attribute_values_with_subsets = self._split_set(data_list, attribute_number)
        avaliable_attributes.remove(attribute_number)
        attribute_value_with_node_pairs = list()
        for attribute_value, subset in attribute_values_with_subsets:
            node = self._create_subtree(subset, avaliable_attributes.copy())
            attribute_value_with_node_pairs.append((attribute_value, node))
        return AttributeNode(attribute_number, attribute_value_with_node_pairs)

    def _get_attribute_to_split_on_classic(self, data_list, avaliable_attributes):
        best_attribute_number = None
        best_attribute_information_gain = 0
        for attribute_number in avaliable_attributes:
            attribute_information_gain = self._calculate_information_gain(data_list, attribute_number)
            if attribute_information_gain >= best_attribute_information_gain:
                best_attribute_information_gain = attribute_information_gain
                best_attribute_number = attribute_number
        return best_attribute_number

    def _get_attribute_to_split_on_tournament(self, data_list, avaliable_attributes):
        if len(avaliable_attributes) > 1:
            attributes = random.sample(avaliable_attributes, 2)
            return self._get_attribute_to_split_on_classic(data_list, attributes)
        else:
            return avaliable_attributes[0]

    def _get_attribute_to_split_on(self, data_list, avaliable_attributes):
        if self._test_type == self.TestType.CLASSIC:
            return self._get_attribute_to_split_on_classic(data_list, avaliable_attributes)
        elif self._test_type == self.TestType.TOURNAMENT:
            return self._get_attribute_to_split_on_tournament(data_list, avaliable_attributes)
        else:
            raise RuntimeError("Bad test type")


    def _calculate_information_gain(self, data_list, attribute_number):
        set_entrophy = self._calculate_entrophy(data_list)
        subsets_mean_entrophy = self._calculate_subsets_mean_entrophy(data_list, attribute_number)
        return round(set_entrophy - subsets_mean_entrophy, 6)  # Round to ignore floating-point calculation errors

    def _calculate_entrophy(self, data_list):
        classes_frequencies = self._calculate_class_frequencies(data_list)
        entrophy = 0
        for class_value, class_frequency in classes_frequencies:
            entrophy += class_frequency * math.log2(class_frequency)
        return -entrophy

    def _calculate_subsets_mean_entrophy(self, data_list, division_attribute_number):
        data_subsets = self._split_set(data_list, division_attribute_number)
        mean_entrophy = 0
        for attribute_value, data_subset in data_subsets:
            mean_entrophy += len(data_subset) * self._calculate_entrophy(data_subset)
        return mean_entrophy/len(data_list)

    def _calculate_class_frequencies(self, data_list):
        class TreeClass:
            def __init__(self, class_value):
                self.class_value = class_value
                self.class_counter = 1

        classes = list()
        for data_object in data_list:
            object_class = data_object[0]
            for tree_class in classes:
                if tree_class.class_value == object_class:
                    tree_class.class_counter += 1
                    break
            else:
                classes.append(TreeClass(object_class))
        class_frequencies = list()
        for tree_class in classes:
            class_frequency = tree_class.class_counter/len(data_list)
            class_frequencies.append((tree_class.class_value, class_frequency))
        return class_frequencies

    def _split_set(self, data_list, division_attribute_number):
        data_subsets = list()
        for data_object in data_list:
            for attribute_value, attribute_data_set in data_subsets:
                if attribute_value == data_object[division_attribute_number]:
                    attribute_data_set.append(data_object)
                    break
            else:
                data_subsets.append((data_object[division_attribute_number], [data_object]))
        return data_subsets

    def _is_pure(self, data_list):
        class_frequencies = self._calculate_class_frequencies(data_list)
        for class_name, class_frequency in class_frequencies:
            if class_frequency == 1:
                return True
        return False

    def _get_first_object_class_name(self, data_list):
        return data_list[0][0]
