import os

from file import deserializer, serializer
from threader import get_user_input

file_structure = []


def main(input_structure):
    if os.path.exists('file-structure.img'):
        input_structure = deserializer()

    print('\n********** File System Simulator **********\n')
    flat_directory = get_user_input(input_structure)
    serializer(flat_directory)


if __name__ == "__main__":
    main(file_structure)
