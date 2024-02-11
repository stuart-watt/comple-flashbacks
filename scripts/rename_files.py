from os import listdir
from os.path import isfile, join
import os

import fire


def rename_files(path, year_month):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    print(onlyfiles)

    for file in onlyfiles:
        old_file = os.path.join(path, file)
        new_file = os.path.join(path, year_month + file)
        os.rename(old_file, new_file)

    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    print(onlyfiles)


if __name__ == "__main__":
    fire.Fire(rename_files)
