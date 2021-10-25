import math
import random
import string
import subprocess
from datetime import date, timedelta
import os
import uuid
from termcolor import cprint


alphabet = {
    "A": [[2], [1, 3], [1, 2, 3], [0, 1, 3, 4], [0, 4]],
    "B": [[0, 1, 2, 3], [0, 3, 4], [0, 1, 2, 3], [0, 3, 4], [0, 1, 2, 3]],
    "C": [[0, 1, 2, 3, 4], [0], [0], [0], [0, 1, 2, 3, 4]],
    "D": [[0, 1], [0, 2], [0, 3], [0, 4], [0, 1, 2, 3, 4]],
    "E": [[0, 1, 2, 3, 4], [0], [0, 1, 2, 3, 4], [0], [0, 1, 2, 3, 4]],
    "F": [[0, 1, 2, 3, 4], [0], [0, 1, 2, 3, 4], [0], [0]],
    "G": [[0, 1, 2, 3, 4], [0], [0, 3, 4], [0, 4], [0, 1, 2, 3, 4]],
    "H": [[0, 4], [0, 4], [0, 1, 2, 3, 4], [0, 4], [0, 4]],
    "I": [[0, 1, 2], [1], [1], [1], [0, 1, 2]],
    "J": [[4], [4], [4], [0, 4], [0, 1, 2, 3, 4]],
    "K": [[0, 4], [0, 3], [0, 1, 2], [0, 3], [0, 4]],
    "L": [[0], [0], [0], [0], [0, 1, 2, 3, 4]],
    "M": [[0, 4], [0, 1, 3, 4], [0, 2, 4], [0, 4], [0, 4]],
    "N": [[0, 4], [0, 1, 4], [0, 2, 4], [0, 3, 4], [0, 4]],
    "O": [[0, 1, 2, 3, 4], [0, 4], [0, 4], [0, 4], [0, 1, 2, 3, 4]],
    "P": [[0, 1, 2, 3, 4], [0, 4], [0, 1, 2, 3, 4], [0], [0]],
    "Q": [[0, 1, 2, 3, 4], [0, 4], [0, 4], [0, 4], [0, 1, 2, 3], [2, 3, 4]],
    "R": [[0, 1, 2, 3, 4], [0, 4], [0, 1, 2, 3, 4], [0, 3], [0, 4]],
    "S": [[1, 2, 3, 4], [0], [1, 2, 3], [4], [0, 1, 2, 3]],
    "T": [[0, 1, 2, 3, 4], [2], [2], [2], [2]],
    "U": [[0, 4], [0, 4], [0, 4], [0, 4], [0, 1, 2, 3, 4]],
    "V": [[0, 4], [0, 4], [1, 3], [1, 3], [2]],
    "W": [[0, 4], [0, 4], [0, 2, 4], [0, 1, 3, 4], [0, 4]],
    "X": [[0, 4], [1, 3], [2], [1, 3], [0, 4]],
    "Y": [[0, 4], [1, 3], [2], [2], [2]],
    "Z": [[0, 1, 2, 3, 4], [3], [2], [1], [0, 1, 2, 3, 4]],
    "0": [[1, 2], [0, 3], [0, 3], [0, 3], [1, 2]],
    "1": [[0], [0], [0], [0], [0]],
    "2": [[0, 1, 2], [3], [1, 2], [0], [1, 2, 3]],
    "3": [[0, 1, 2], [3], [0, 1, 2], [3], [0, 1, 2]],
    "4": [[0, 3], [0, 3], [0, 1, 2, 3], [3], [3]],
    "5": [[0, 1, 2, 3], [0], [0, 1, 2], [3], [0, 1, 2]],
    "6": [[1, 2, 3], [0], [0, 1, 2], [0, 3], [1, 2]],
    "7": [[0, 1, 2, 3], [2], [2], [1], [1]],
    "8": [[1, 2], [0, 3], [1, 2], [0, 3], [1, 2]],
    "9": [[1, 2], [0, 3], [1, 2, 3], [3], [1, 2]],
    "^": [[0, 2, 3, 4], [0, 2], [0, 1, 2, 3, 4], [2, 4], [0, 1, 2, 4]],
    " ": []
}


def letter_width(letter):
    return 0 if len(letter) == 0 else max([max(row) for row in letter]) + 1


def get_coordinates_for_word(word):
    width = 52
    height = 7
    space_width = 1

    letter_widths = [letter_width(alphabet[letter]) for letter in word]
    word_width = sum(letter_widths) + space_width * (len(word) - 1)
    x_border = (width - word_width) // 2

    if x_border <= 0:
        raise Exception("word is too big")

    coordinates = []
    for i in range(0, len(word)):
        letter_shift_x = x_border + sum(letter_widths[0:i]) + space_width * i
        letter_height = len(alphabet[word[i]])
        letter_shift_y = math.ceil((height - letter_height) / 2)

        if letter_shift_y <= 0:
            raise Exception("letter is too big")

        for dy in range(0, letter_height):
            for dx in alphabet[word[i]][dy]:
                coordinates.append((letter_shift_x + dx, letter_shift_y + dy))
    return coordinates


def transform_coordinates_to_dates(coordinates):
    start = date.today() - timedelta(days=date.today().weekday())
    start = start.replace(year=start.year - 1)
    return [start + timedelta(days=7 * x + y) for x, y in coordinates]


def init_repo(origin, username, email):
    repo_guid = str(uuid.uuid4()).split("-")[0]
    repo = "repo-{}".format(repo_guid)
    os.mkdir(repo)
    subprocess.call((
        "cd {} && git init 2>&1 >/dev/null && git config user.name \"{}\"" +
        " && git config user.email \"{}\" && git remote add origin {}"
    ).format(repo, username, email, origin), shell=True)
    return repo


def make_commit_on_date(repo, commit_date):
    for r in range(10):
        random_text = random.choice(string.digits)
        subprocess.call((
            "cd {} && echo \"{}\" >> {} && git add . && git commit -m \"auto generate commit\" 2>&1 >/dev/null &&" +
            "GIT_COMMITTER_DATE=\"{} 12:00:00\" git commit --amend --no-edit --date=\"{} 12:00:00\" 2>&1 >/dev/null"
        ).format(repo, random_text, repo + ".txt", commit_date, commit_date), shell=True)


def push_repo(repo):
    subprocess.call(
        "cd {} && git push -u origin master 2>&1 >/dev/null && cd ../ && rm -rf {}".format(repo, repo), shell=True)


def write_word(word, origin, username, email):
    cprint("Initializing repo ...", "red")
    repo = init_repo(origin, username, email)
    coords = get_coordinates_for_word(word)
    dates = transform_coordinates_to_dates(coords)
    cprint("Making commits ...", "red")
    [make_commit_on_date(repo, str(commit_date)) for commit_date in dates]
    cprint("Pushing commits ...", "red")
    push_repo(repo)


def check_word(word):
    if not all([letter in alphabet for letter in word]):
        raise Exception("Unsupported letter")


def do_everything():
    print("Input word: ", end="")
    word = input().strip()
    check_word(word)
    print("Input origin (repo url): ", end="")
    origin = input().strip()
    print("Input gh username: ", end="")
    username = input().strip()
    print("Input gh email: ", end="")
    email = input().strip()
    write_word(word, origin, username, email)


do_everything()
