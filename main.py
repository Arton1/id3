from id3_tree_builder import Id3TreeBuilder
import re
from sys import argv

def print_usage_information():
    print("Arguments: test_type file_path")
    print("test_type: '-c' as classic, '-t' as tournament")
    quit()

if __name__ == "__main__":
    if len(argv) != 3:
        print_usage_information()
    try:
        file = open(argv[2])
    except IOError:
        print("File doesn't exist")
        quit()
    else:
        with file:
            text = file.readlines()
    data = [re.findall(r"\w+", line) for line in text]
    if argv[1] == '-t':
        id3_tree_builder = Id3TreeBuilder(data, Id3TreeBuilder.TestType.TOURNAMENT)
    elif argv[1] == '-c':
        id3_tree_builder = Id3TreeBuilder(data, Id3TreeBuilder.TestType.CLASSIC)
    else:
        print_usage_information()
    tree_root = id3_tree_builder.get_tree()
    print(tree_root)