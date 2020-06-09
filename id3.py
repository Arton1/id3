from id3_tree_builder import Id3TreeBuilder
import re
from sys import argv
from random import choice


def print_usage_information():
    print("Usage: python id3.py option dataset_file_path")
    print("option: 'c' as classic, 't' as tournament, 'cmp [k_value]' to compare two previous test types")
    print("dataset_file_path: path to data with classes as first column")

def get_mean_loss(data, k, id3_test_type):
    amount_of_test_data = len(data)//k
    total_loss = 0
    for validation_index in range(k):
        test_data = data[amount_of_test_data*validation_index : amount_of_test_data*(validation_index+1)]
        training_data = data[:amount_of_test_data*validation_index] + data[amount_of_test_data*(validation_index+1):]
        id3_tree_builder = Id3TreeBuilder(training_data, id3_test_type)
        tree_root = id3_tree_builder.get_tree()
        amount_of_missed_classifications = 0
        for test_object in test_data:
            classification = tree_root.classify(test_object[1:])  # First element is object's classification
            if classification != test_object[0]:
                amount_of_missed_classifications += 1
        total_loss += amount_of_missed_classifications/len(test_data)
    return total_loss / k


def compare_ID3_implementations(data, k=10):
    """ Comparison using k-fold cross-validation
    """
    amount_of_tournament_mean_losses = 100
    mean_loss_classic = round(get_mean_loss(data, k, Id3TreeBuilder.TestType.CLASSIC), 6)
    total_tournament_mean_loss = 0
    for tournament_mean_loss in range(amount_of_tournament_mean_losses):  # Multiple checks, because id3 with tournament is not deterministic
        total_tournament_mean_loss += get_mean_loss(data, k, Id3TreeBuilder.TestType.TOURNAMENT)
    mean_loss_tournament = round(total_tournament_mean_loss/amount_of_tournament_mean_losses, 5)
    print(f"Mean loss of highest information gain test type: {mean_loss_classic}")
    print(f"Mean loss of tournament test type for {amount_of_tournament_mean_losses} iterations: {mean_loss_tournament}")


if __name__ == "__main__":
    if len(argv) != 3 and len(argv) != 4:
        print_usage_information()
        quit()
    try:
        if len(argv) == 3:
            file = open(argv[2])
        elif len(argv) == 4:
            file = open(argv[3])
    except IOError:
        print("File doesn't exist")
        quit()
    else:
        with file:
            text = file.readlines()
    data = list(re.findall(r"[\w?]+", line) for line in text)
    if argv[1] == 't':
        id3_tree_builder = Id3TreeBuilder(data, Id3TreeBuilder.TestType.TOURNAMENT)
    elif argv[1] == 'c':
        id3_tree_builder = Id3TreeBuilder(data, Id3TreeBuilder.TestType.CLASSIC)
    elif argv[1] == 'cmp':
        compare_ID3_implementations(data, int(argv[2]))
        quit()
    else:
        print_usage_information()
        quit()
    tree_root = id3_tree_builder.get_tree()
    print(tree_root)