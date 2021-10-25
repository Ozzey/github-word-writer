import random
import string
import subprocess
from datetime import date, timedelta
import os
import uuid


alphabet = {
    "N": [[0, 4], [0, 1, 4], [0, 2, 4], [0, 3, 4], [0, 4]],
    "I": [[0, 1, 2], [1], [1], [1], [0, 1, 2]],
    "G": [[0, 1, 2, 3, 4], [0], [0, 3, 4], [0, 4], [0, 1, 2, 3, 4]],
    "E": [[0, 1, 2, 3, 4], [0], [0, 1, 2, 3, 4], [0], [0, 1, 2, 3, 4]],
    "R": [[0, 1, 2, 3, 4], [0, 4], [0, 1, 2, 3, 4], [0, 3], [0, 4]],
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
        letter_shift_y = (height - letter_height) // 2

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
    repo_guid = uuid.uuid4()
    repo = "repo-{}".format(repo_guid)
    os.mkdir(repo)
    subprocess.call(
        "cd {} && git init && git config user.name \"{}\" && git config user.email \"{}\" && git remote add origin {}"
        .format(repo, username, email, origin), shell=True)
    return repo


def make_commit_on_date(repo, commit_date):
    for r in range(random.randint(8, 11)):
        random_text = ''.join(random.choice(string.digits) for _ in range(random.randint(500, 2000)))
        extension = random.choice([".cpp", ".py"])
        subprocess.call((
            "cd {} && echo \"{}\" >> {} && git add . && git commit -m \"auto generate commit\" &&" +
            "GIT_COMMITTER_DATE=\"{} 12:00:00\" git commit --amend --no-edit --date=\"{} 12:00:00\""
        ).format(repo, random_text, str(uuid.uuid4()) + extension, commit_date, commit_date), shell=True)


def push_repo(repo):
    subprocess.call("cd {} && git push -u origin master && cd ../ && rm -rf {}".format(repo, repo), shell=True)


def write_word(word, origin, username, email):
    repo = init_repo(origin, username, email)
    coords = get_coordinates_for_word(word)
    dates = transform_coordinates_to_dates(coords)
    print([str(date) for date in dates])
    [make_commit_on_date(repo, str(commit_date)) for commit_date in dates]
    push_repo(repo)


def do_everything():
    print("Input word: ", end="")
    word = input().strip()
    print("Input origin (repo url): ", end="")
    origin = input().strip()
    print("Input gh username: ", end="")
    username = input().strip()
    print("Input gh email: ", end="")
    email = input().strip()
    write_word(word, origin, username, email)


do_everything()
