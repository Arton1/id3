from id3_tree_builder import Id3TreeBuilder
import re

if __name__ == "__main__":
    data = None
    with open("training_data") as file:
        text = file.readlines()
    data = [re.findall(r"\w+", line) for line in text]
    id3_tree_builder = Id3TreeBuilder(data)
    tree_root = id3_tree_builder.get_tree()
    print(len(tree_root))