import sys

import racey_module


def main():
    the_directory, = sys.argv[1:]
    racey_module.racey_function(the_directory)


if __name__ == "__main__":
    main()
