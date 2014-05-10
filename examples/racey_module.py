import os


def racey_function(the_directory):
    if not os.path.exists(the_directory):
        os.mkdir(the_directory)

    os.rmdir(the_directory)
