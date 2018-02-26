import os
from glob import glob
import numpy as np
import shutil
import re
from configparser import ConfigParser

CONFIG_FILE = "config.ini"
MANGA_SECTION = "manga"
TESTING_SECTION = "testing"

DEBUG_STAGE_FORMAT = "Beginning {} stage"

config = ConfigParser()
config.read(CONFIG_FILE)

# parse TITLE
TITLE = config[MANGA_SECTION]["TITLE"]
CHAPTER_FOLDER_TEMPLATE = TITLE + " - {}"
# TODO: Add Check here

# parse directory
DIRECTORY = config[MANGA_SECTION]["DIRECTORY"]

# ensure directory exists
if not os.path.exists(DIRECTORY):
    error_msg = "{} must exists. Currently, it does not."
    raise Exception(error_msg.format(DIRECTORY))

# ensure it's a directory
if os.path.exists(DIRECTORY) and not os.path.isdir(DIRECTORY):
    error_msg = "{} must be a directory. "
    if os.path.isfile(DIRECTORY):
        error_msg += "Currently, it is a file."
    elif os.path.islink(DIRECTORY):
        error_msg += "Currently, it is a link."
    else:
        error_msg += "Currently, it's neither directory, file, nor link."
    raise Exception(error_msg.format(DIRECTORY))

# parse CHAPTER_RANGE_START
CHAPTER_RANGE_START = config[MANGA_SECTION]["CHAPTER_RANGE_START"]
try:
    if CHAPTER_RANGE_START != "":
        CHAPTER_RANGE_START = int(CHAPTER_RANGE_START)
        if CHAPTER_RANGE_START <= 0:
            raise Exception()
except ValueError:
    error_msg = "CHAPTER_RANGE_START must be whole number greater than zero. Currently, it is: {}"
    raise Exception(error_msg.format(CHAPTER_RANGE_START))
    
# parse CHAPTER_RANGE_FINISH
CHAPTER_RANGE_FINISH = config[MANGA_SECTION]["CHAPTER_RANGE_FINISH"]
try:
    if CHAPTER_RANGE_FINISH != "":
        CHAPTER_RANGE_FINISH = int(CHAPTER_RANGE_FINISH)
        if CHAPTER_RANGE_FINISH <= CHAPTER_RANGE_START:
            raise Exception()
except ValueError:
    error_msg = "CHAPTER_RANGE_FINISH must be whole number greater than zero. Currently, it is: {}"
    raise Exception(error_msg.format(CHAPTER_RANGE_FINISH))

# parse BACKUP_BOOLEAN
BACKUP_BOOLEAN = config[MANGA_SECTION]["BACKUP_BOOLEAN"]
try:
    BACKUP_BOOLEAN = bool(BACKUP_BOOLEAN)
except Exception:
    error_msg = "BACKUP_BOOLEAN must be either True or False. Currently, it is: {}"
    raise Exception(error_msg.format(BACKUP_BOOLEAN))

# obtain BACKUP_DIRECTORY
BACKUP_DIRECTORY = config[MANGA_SECTION]["BACKUP_DIRECTORY"]

# parse ZFILL_LENGTH_CHAPTER
ZFILL_LENGTH_CHAPTER = config[MANGA_SECTION]["ZFILL_LENGTH_CHAPTER"]
try:
    ZFILL_LENGTH_CHAPTER = int(ZFILL_LENGTH_CHAPTER)
    if ZFILL_LENGTH_CHAPTER < 1:
        raise ValueError
except ValueError:
    error_msg = "ZFILL_LENGTH_CHAPTER must be whole number greater than zero. Currently, it is: {}"
    raise Exception(error_msg.format(ZFILL_LENGTH_CHAPTER))

# parse ZFILL_LENGTH_PAGE
ZFILL_LENGTH_PAGE = config[MANGA_SECTION]["ZFILL_LENGTH_PAGE"]
try:
    ZFILL_LENGTH_PAGE = int(ZFILL_LENGTH_PAGE)
    if ZFILL_LENGTH_PAGE < 1:
        raise ValueError
except ValueError:
    error_msg = "ZFILL_LENGTH_PAGE must be whole number greater than zero. Currently, it is: {}"
    raise Exception(error_msg.format(ZFILL_LENGTH_PAGE))

# parse BUCKETS_RANGE
BUCKETS_RANGE = config[MANGA_SECTION]["BUCKETS_RANGE"]
try:
    BUCKETS_RANGE = int(BUCKETS_RANGE)
    if BUCKETS_RANGE < 1:
        raise Exception()
except ValueError:
    error_msg = "BUCKETS_RANGE must be whole number greater than zero. Currently, it is: {}"
    raise Exception(error_msg.format(BUCKETS_RANGE))

# parse DEBUG_BOOLEAN
DEBUG_BOOLEAN = config[TESTING_SECTION]["DEBUG_BOOLEAN"]
try:
    DEBUG_BOOLEAN = bool(DEBUG_BOOLEAN)
except Exception:
    error_msg = "DEBUG_BOOLEAN must be either True or False. Currently, it is: {}"
    raise Exception(error_msg.format(DEBUG_BOOLEAN))

# print all config values if we're in debug mode    
if DEBUG_BOOLEAN:
    print("Printing values since DEBUG_BOOLEAN is True")
    print("CHAPTER_FOLDER_TEMPLATE = {}".format(CHAPTER_FOLDER_TEMPLATE))
    print("CHAPTER_RANGE_START = {}".format(CHAPTER_RANGE_START))
    print("CHAPTER_RANGE_FINISH = {}".format(CHAPTER_RANGE_FINISH))
    print("BACKUP_BOOLEAN = {}".format(BACKUP_BOOLEAN))
    print("BACKUP_DIRECTORY = {}".format(BACKUP_DIRECTORY))
    print("ZFILL_LENGTH_CHAPTER = {}".format(ZFILL_LENGTH_CHAPTER))
    print("ZFILL_LENGTH_PAGE = {}".format(ZFILL_LENGTH_PAGE))
    print("BUCKETS_RANGE = {}".format(BUCKETS_RANGE))
    print("DIRECTORY = {}".format(DIRECTORY))


def _get_chapter_titles(path="."):
    list_dir = os.listdir(path)
    chapter_titles_found = []

    # for every file in our list
    for file in list_dir:

        # if the title we're looking for is in the file
        if TITLE in file:

            # add it to the list of chapter file names
            chapter_titles_found.append(file)

    return chapter_titles_found


def _get_chapter_numbers_as_strings():
    chapter_numbers = []
    chapter_titles_found = _get_chapter_titles()
    for chapter_title in chapter_titles_found:
        chapter_number_as_string = _get_chapter_number_from_title_as_string(chapter_title)
        chapter_numbers.append(chapter_number_as_string)

    return chapter_numbers


def _get_chapter_numbers_as_floats():
    chapter_numbers_as_floats = []
    chapter_numbers_as_strings = _get_chapter_numbers_as_strings()
    for chapter_title_as_string in chapter_numbers_as_strings:
        chapter_number_as_float = float(chapter_title_as_string)
        chapter_numbers_as_floats.append(chapter_number_as_float)

    return chapter_numbers_as_floats


def _get_max_chapter_length():
    max_chapter_length = 0
    chapter_numbers = _get_chapter_numbers_as_strings()
    for chapter_number in chapter_numbers:
        if len(chapter_number) > max_chapter_length:
            max_chapter_length = len(chapter_number)

    return max_chapter_length


def _get_min_chapter_length():
    min_chapter_length = 100
    chapter_numbers = _get_chapter_numbers_as_strings()
    for chapter_number in chapter_numbers:
        if len(chapter_number) < min_chapter_length:
            min_chapter_length = len(chapter_number)

    return min_chapter_length


def _get_max_chapter():
    max_chapter = 0
    chapter_numbers = _get_chapter_numbers_as_strings()
    for chapter_number in chapter_numbers:
        chapter_number = float(chapter_number)
        if chapter_number > max_chapter:
            max_chapter = len(chapter_number)

    max_chapter


def _get_min_chapter():
    min_chapter = 0
    chapter_numbers = _get_chapter_numbers_as_strings()
    for chapter_number in chapter_numbers:
        chapter_number = float(chapter_number)
        if chapter_number < min_chapter:
            min_chapter = len(min_chapter)

    min_chapter


def _get_chapter_number_from_title_as_string(chapter_title):
    if TITLE not in chapter_title:
        error_msg = "chapter title '{}' doesn't include TITLE '{}' in the name. How did we get here?"
        raise Exception(error_msg.format(chapter_title, TITLE))

    # get relevant contents after title
    after = chapter_title.split(TITLE)[1].strip()

    # sometimes you'll see a title with nothing but the chapter number after
    #   0 kara Hajimeru Manga Kyoushitsu 001
    # sometimes the title won't have the chapter number zero-padded
    #   A Love for Sweet Things 1
    #   A Love for Sweet Things 2
    #   A Love for Sweet Things 3
    # sometimes you'll see a title with a 'Ch.' before the chapter number
    #   .hack//4 koma Ch.001: Delicacy-chan
    # sometimes you'll see a title with a 'Chapter' before the chapter number
    #   Grand Blue Chapter 037.001
    # sometimes you'll see 'Ch.Extra'???
    #   Ai Kara Hajimaru Vol.001 Ch.Extra 001: Sugarless Kiss
    # sometimes you'll see a title with a 'Vol: ' and 'Ch: ' mentioned
    #   29-sai Hitorimi Chuuken Boukensha no Nichijou Vol.001 Ch.003: Father?
    # sometimes you'll see a title with a 'vol: ' and 'ch: ' mentioned
    #   Rakujitsu no Pathos vol.003 ch.023
    # sometimes you'll see inconsistencies
    #   Raisekamika Chapter 010
    #   Raisekamika Vol.002 Ch.009
    # sometimes you'll see multiple occurrences of a chapter
    #   Rakuen Vol.001 Ch.003.003 Read Online
    #   Rakuen Vol.001 Ch.003.002 Read Online
    #   Rakuen Vol.001 Ch.003.001 Read Online
    # sometimes you'll see two occurrences of the number
    #   Ai Yuugi Vol.001 Ch.003: Love Game (003)
    # chapters can start at zero?
    #   AI07 Ch.000
    # two occurrences of the same chapter?
    #   Aibu de Jirashite Vol.Extra Ch.000: 001
    #   Aibu de Jirashite Vol.001 Ch.005
    #   ...
    #   Aibu de Jirashite Vol.001 Ch.001 Read Online

    # remove the volume, since we're not interested in it
    if "Vol" in after or "vol" in after:
        if "Vol" in after:
            after = after.split("Vol")[1]

        elif "vol" in after:
            after = after.split("vol")[1]

        # we should also remove the volume number that's comes after, cases:
        #   Vol.001
        #   Vol.Extra
        # a period or colon between
        while (after[0] == ".") or \
                (after.startswith("Extra")) or \
                (after[0].isdigit()):

            # handle these separately
            if (after[0] == ".") or (after[0].isdigit()):
                after = after[1:]
            elif after.startswith("Extra"):
                after = after.split("Extra")

        # remove whitespace
        after.lstrip()

    # remove the chapter indicator (if it's given)
    if "Chapter" in after or "Ch" in after or "ch" in after:
        if "Chapter" in after:
            after = after.split("Chapter")[1]

        elif "Ch" in after:
            after = after.split("Ch")[1]

        elif "ch" in after:
            after = after.split("ch")[1]

        # we should also remove what comes after the chapter indicator and before the number
        #   Chapter 001
        #   Ch.001
        #   Ch.Extra 001
        # a period or colon between
        while (after[0] == ".") or \
                (after[0] == " ") or \
                (after.startswith("Extra")):

            # handle these separately
            if (after[0] == ".") or (after[0] == " "):
                after = after[1:]
            elif after.startswith("Extra"):
                after = after.split("Extra")[1]

    # in our own custom templating, we should have something like:
    #   '- 01.0'
    if "- " in after:
        after = after.split("- ")[1]

    # after should now start with the chapter number
    #   001
    #   001.001:
    chapter_number = ""
    while len(after) != 0 and (after[0].isdigit() or after[0] == "."):
        chapter_number += after[0]
        after = after[1:]

    # we should crash if we couldn't find the chapter number
    if chapter_number == "":
        error_msg = "couldn't find the chapter_number from the chapter title '{}'"
        raise Exception(error_msg.format(chapter_title))

    return chapter_number


def _cleanup_chapter_number(str_n):
    """Given something like '001.001', return 1.1'"""

    if str_n.find(".") != -1:
        before, after = str_n.split(".")
        before = str(int(before))
        after = str(int(after))
        return_float = float(".".join([before, after]))

    else:
        return_float = float(str(int(str_n)))

    return return_float


def get_number_of_images(path=".", accepted_file_extensions=('png', 'jpg', 'jpeg')):
    list_dir = os.listdir(path)
    count = 0
    for file in list_dir:
        for accepted_file_extension in accepted_file_extensions:
            if file.endswith(accepted_file_extension):
                count += 1
                break
    return count


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def backup(dir_name):

    # start in correct directory
    os.chdir(DIRECTORY)

    # if the BACKUP_BOOLEAN is specified (it should always be)
    if BACKUP_BOOLEAN:

        # (re)create the backup directory
        if os.path.isdir(dir_name):
            shutil.rmtree(dir_name)
        os.makedirs(dir_name)

        # get the chapters
        chapters_titles_found = _get_chapter_titles()

        # fail if no chapters were found
        if len(chapters_titles_found) == 0:
            error_msg = "There are no chapters with the title '{}' in the " \
                        "directory '{}'. Check the appropriate variables in the configuration file."
            raise Exception(error_msg.format(TITLE, DIRECTORY))

        # move all the folders
        for chapter_title in chapters_titles_found:

            # sanity check that folder exists
            if not os.path.isdir(chapter_title):
                error_msg = "chapter_folder '{}' is not a folder."
                raise Exception(error_msg.format(chapter_title))

            os.chdir(dir_name)
            os.mkdir(chapter_title)
            os.chdir("..")
            copytree(chapter_title, dir_name + "/" + chapter_title)


def fix_folders():

    backup(BACKUP_DIRECTORY + "_before_fix_folders")

    # get the chapters
    chapters_titles_found = _get_chapter_titles()
    chapter_titles_and_numbers_fixed = []
    max_chapter_number_length = 0
    for chapter_title in chapters_titles_found:
        chapter_number = _get_chapter_number_from_title_as_string(chapter_title)
        chapter_number = _cleanup_chapter_number(chapter_number)
        if len(str(chapter_number)) > max_chapter_number_length:
            max_chapter_number_length = len(str(chapter_number))
        chapter_titles_and_numbers_fixed.append((chapter_title, chapter_number))

    for (chapter_title, chapter_number) in chapter_titles_and_numbers_fixed:
        chapter_number = str(chapter_number).zfill(max_chapter_number_length)
        new_chapter_title = CHAPTER_FOLDER_TEMPLATE.format(chapter_number)
        os.rename(chapter_title, new_chapter_title)


def fix_images():
    # backup(BACKUP_DIRECTORY + "_before_fix_images")

    minimum_number_of_images = 1

    chapters_titles_found = _get_chapter_titles()
    chapters_with_too_little_images = []
    for chapter_title in chapters_titles_found:
        os.chdir(chapter_title)
        number_of_images = get_number_of_images()
        if number_of_images <= minimum_number_of_images:
            chapters_with_too_little_images.append(chapter_title)

    if len(chapters_with_too_little_images) > 0:
        error_message = "Glob caught less than or equal to {} images in these directories: {}."
        raise Exception(
            error_message.format(minimum_number_of_images,
                                 chapters_with_too_little_images))

    for chapter_title in chapters_titles_found:
        chapter = _get_chapter_number_from_title_as_string(chapter_title)

        if DEBUG_BOOLEAN:
            print("Chapter {}".format(chapter))
        chapter_folder = CHAPTER_FOLDER_TEMPLATE.format(chapter)
        os.chdir(chapter_folder)
        number_of_images = get_number_of_images()
        accepted_file_extensions = ('png', 'jpg', 'jpeg')
        rejected_file_extensions = ('txt',)
        potential_substrings = ("cred", "gb")
        glob_regex_base = '*[0-9][0-9][0-9]*'
        glob_caught_images = []
        for file_extension in accepted_file_extensions:
            glob_caught_images_with_file_extension = glob(glob_regex_base + '.' + file_extension)
            glob_caught_images.extend(glob_caught_images_with_file_extension)
        number_of_images_by_glob = len(glob_caught_images)

        if number_of_images_by_glob <= 1:
            error_message = "Glob caught less than or equal to {} images in the {} directory."
            raise Exception(
                error_message.format(minimum_number_of_images, chapter_title))

        if number_of_images != number_of_images_by_glob:
            glob_missed_images = set(glob("*")) - set(glob_caught_images)
            for missed in glob_missed_images:

                # we might get some random files that absolutely shouldn't
                # be in here. Delete them.
                for rejected_file_extension in rejected_file_extensions:
                    if missed.endswith(rejected_file_extension):
                        os.remove(missed)

                # raise an error if it's not a recognized filename
                for potential_substring in potential_substrings:
                    if potential_substring not in missed:
                        error_message = "Glob missed some images: total={}, glob_caught={}. " \
                                        "This file is called '{}' in the {} directory."
                        raise Exception(
                            error_message.format(
                                number_of_images, number_of_images_by_glob,
                                missed, chapter_title))

        # we need this variable to handle duplicates
        duplicate_handler = 1

        # for every image of interest...
        mode = "capture"
        for i in range(len(glob_caught_images)):
            name = glob_caught_images[i]
            chapter_as_string = str(chapter).zfill(ZFILL_LENGTH_CHAPTER)

            # this ensures we capture the given image index and output it accordingly
            page_as_string = re.findall(r'\d+', name)[-1].zfill(3)

            # an additional check to handle exceptions: Shingeki no Kyojin -
            # Chapter 97 from mangahere.cc has images with format like so:
            # shingeki-no-kyojin-9734011.jpg
            if len(page_as_string) > 3:
                mode = "force_to_be_index"
            if mode == "force_to_be_index":
                page_as_string = str(i + 1).zfill(3)

            new_name = "{}-{}.jpg".format(chapter_as_string, page_as_string)
            if DEBUG_BOOLEAN:
                print(name + " -> " + new_name)

            # handle duplicates
            if os.path.isfile(new_name):
                duplicate_handler += 1
                new_name = new_name + "-" + str(duplicate_handler)

            # rename the file
            os.rename(name, new_name)

        os.chdir("..")


def _get_bound_as_string(n):
    return str(n)


def _get_lower_bound_as_string(str_n, chapters):
    """
    We want to get the lower bound for the bucket of chapters.
    00001-00010, 00011-00020, etc
    """
    n = float(str_n)
    mod = n % BUCKETS_RANGE

    if mod == 0:
        lower = (n - BUCKETS_RANGE) + 0.5
    else:
        lower = n - (n % BUCKETS_RANGE) + 0.5

    # we also want to ensure the lowest chapter in a book title isn't below
    # CHAPTER_RANGE_START
    min_n = min(chapters)
    if lower < min_n:
        lower = min_n

    # ensure our book titles only have valid chapters
    if lower not in chapters:
        for potential_lower in chapters:
            if potential_lower > lower:
                lower = potential_lower
                break

    return _get_bound_as_string(lower)


def _get_upper_bound_as_string(str_n, chapters):
    """
    We want to get the upper bound for the bucket of chapters.
    00001-00010, 00011-00020, etc
    """
    n = float(str_n)
    mod = n % BUCKETS_RANGE

    if mod == 0:
        upper = n
    else:
        upper = (n + BUCKETS_RANGE) - (n % BUCKETS_RANGE)

    # we also want to ensure the highest chapter in a book title isn't above
    # CHAPTER_RANGE_START
    max_n = max(chapters)
    if upper > max_n:
        upper = max_n

    return _get_bound_as_string(upper)


def move():
    # once again, we want to backup the chapters
    backup(BACKUP_DIRECTORY + "_before_move")

    # get the chapters
    chapter_numbers_as_strings = _get_chapter_numbers_as_strings()
    chapter_numbers_as_floats = _get_chapter_numbers_as_floats()
    max_chapter_number_length = _get_max_chapter_length()

    # for every chapter...
    for i in range(len(chapter_numbers_as_strings)):

        chapter_number_as_string = chapter_numbers_as_strings[i]
        chapter_number_as_float = chapter_numbers_as_floats[i]

        # get the lower and upper bound for the bucket of chapters
        lower = str(_get_lower_bound_as_string(chapter_number_as_float, chapter_numbers_as_floats)).\
            zfill(max_chapter_number_length)
        upper = str(_get_upper_bound_as_string(chapter_number_as_float, chapter_numbers_as_floats)).\
            zfill(max_chapter_number_length)
        new_chapters_folder_range = "{}-{}".format(lower, upper)
        new_chapters_folder = CHAPTER_FOLDER_TEMPLATE.format(new_chapters_folder_range)

        # this is a hack... we really only need to create this directory once every BUCKETS_RANGE times
        if not os.path.isdir(new_chapters_folder):
            os.makedirs(new_chapters_folder)

        old_chapters_folder = CHAPTER_FOLDER_TEMPLATE.format(chapter_number_as_string)
        os.chdir(old_chapters_folder)

        # for every image...
        for name in glob('*'):

            # move the image to it's bucket folder
            os.rename(name, "../{}/{}".format(new_chapters_folder, name))

        # go back out
        os.chdir("..")

        # remove the old chapters folder
        shutil.rmtree(old_chapters_folder)


def archive():
    """
    Takes every bucket folder and zips them up.
    """

    glob_template = CHAPTER_FOLDER_TEMPLATE.format("*")
    glob_caught_folders = glob(glob_template)
    for folder in glob_caught_folders:
        shutil.make_archive(folder, 'zip', folder)


def to_cbz():
    """
    Takes every bucket .zip folder and changes the extension to .cbz.
    """

    glob_template = CHAPTER_FOLDER_TEMPLATE.format("*.zip")
    glob_caught_folders = glob(glob_template)
    for zip_file in glob_caught_folders:
        cbz_file = zip_file.replace(".zip", ".cbz")
        os.rename(zip_file, cbz_file)


if __name__ == "__main__":

    # start in correct directory
    os.chdir(DIRECTORY)

    if DEBUG_BOOLEAN:
        print(DEBUG_STAGE_FORMAT.format("fix_folders"))
    fix_folders()

    if DEBUG_BOOLEAN:
        print(DEBUG_STAGE_FORMAT.format("fix_images"))
    fix_images()

    if DEBUG_BOOLEAN:
        print(DEBUG_STAGE_FORMAT.format("move"))
    move()

    if DEBUG_BOOLEAN:
        print(DEBUG_STAGE_FORMAT.format("archive"))
    archive()

    if DEBUG_BOOLEAN:
        print(DEBUG_STAGE_FORMAT.format("to_cbz"))
    to_cbz()
