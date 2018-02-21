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
CHAPTER_FOLDER_TEMPLATE = TITLE + " {}"
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
    CHAPTER_RANGE_START = int(CHAPTER_RANGE_START)
    if CHAPTER_RANGE_START <= 0:
        raise Exception()
except ValueError:
    error_msg = "CHAPTER_RANGE_START must be whole number greater than zero. Currently, it is: {}"
    raise Exception(error_msg.format(CHAPTER_RANGE_START))
    
# parse CHAPTER_RANGE_FINISH
CHAPTER_RANGE_FINISH = config[MANGA_SECTION]["CHAPTER_RANGE_FINISH"]
try:
    CHAPTER_RANGE_FINISH = int(CHAPTER_RANGE_FINISH)
    if CHAPTER_RANGE_FINISH <= CHAPTER_RANGE_START:
        raise Exception()
except ValueError:
    error_msg = "CHAPTER_RANGE_FINISH must be whole number greater than zero. Currently, it is: {}"
    raise Exception(error_msg.format(CHAPTER_RANGE_FINISH))

# parse CHAPTER_INCREMENT
CHAPTER_INCREMENT = config[MANGA_SECTION]["CHAPTER_INCREMENT"]
if CHAPTER_INCREMENT == "0.5":
    CHAPTER_INCREMENT = 0.5
elif CHAPTER_INCREMENT == "1":
    CHAPTER_INCREMENT = 1
else:
    error_msg = "CHAPTER_INCREMENT must be 0.5 or 1. Currently, it is: {}"
    raise Exception(error_msg.format(CHAPTER_INCREMENT))

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
    print("CHAPTER_INCREMENT = {}".format(CHAPTER_INCREMENT))
    print("BACKUP_BOOLEAN = {}".format(BACKUP_BOOLEAN))
    print("BACKUP_DIRECTORY = {}".format(BACKUP_DIRECTORY))
    print("ZFILL_LENGTH_CHAPTER = {}".format(ZFILL_LENGTH_CHAPTER))
    print("ZFILL_LENGTH_PAGE = {}".format(ZFILL_LENGTH_PAGE))
    print("BUCKETS_RANGE = {}".format(BUCKETS_RANGE))
    print("DIRECTORY = {}".format(DIRECTORY))


def get_number_of_chapters(path="."):
    list_dir = os.listdir(path)
    count = 0

    # for every file in our list
    for file in list_dir:

        # if the title we're looking for is in the file
        if TITLE in file:

            # increment our counter
            count += 1
    return count


def get_number_of_images(path=".", extension=".jpg"):
    list_dir = os.listdir(path)
    count = 0
    for file in list_dir:
        if file.endswith(extension):  # eg: '.txt'
            count += 1
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

    temp_chapters = np.arange(CHAPTER_RANGE_START, CHAPTER_RANGE_FINISH, CHAPTER_INCREMENT).tolist()
    chapters = []
    if BACKUP_BOOLEAN:
        if os.path.isdir(dir_name):
            shutil.rmtree(dir_name)
        os.makedirs(dir_name)

        number_of_chapters = get_number_of_chapters()
        if number_of_chapters == 0:
            error_msg = "There are no chapters with the title '{}' in the " \
                        "directory '{}'. Check the appropriate variables in the configuration file."
            raise Exception(error_msg.format(TITLE, DIRECTORY))

        for chapter_index in range(len(temp_chapters)):  # type: list
            chapter = temp_chapters[chapter_index]
            if int(chapter) == chapter:
                chapter = int(chapter)
                temp_chapters[chapter_index] = chapter
            chapter_folder = CHAPTER_FOLDER_TEMPLATE.format(chapter)
            if os.path.isdir(chapter_folder):
                os.chdir(dir_name)
                os.mkdir(chapter_folder)
                os.chdir("..")
                copytree(chapter_folder, dir_name + "/" + chapter_folder)
                chapters.append(chapter)

    return chapters


def convert():

    chapters = backup(BACKUP_DIRECTORY + "_before_convert")
    
    for chapter in chapters:
        if DEBUG_BOOLEAN:
            print("Chapter {}".format(chapter))
        chapter_folder = CHAPTER_FOLDER_TEMPLATE.format(chapter)
        os.chdir(chapter_folder)
        number_of_images = get_number_of_images()
        glob_regex = '*[0-9][0-9][0-9]*.jpg'
        glob_caught_images = glob(glob_regex)
        number_of_images_by_glob = len(glob_caught_images)
        if number_of_images != number_of_images_by_glob:
            glob_missed_images = set(glob("*")) - set(glob(glob_regex))
            for missed in glob_missed_images:
                if ("cred" not in missed) and ("gb" not in missed):
                    error_message = "Glob missed some images: total={}, glob_caught={}. This file is called: {}"
                    raise Exception(error_message.format(number_of_images, number_of_images_by_glob, missed))

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
            # mshingeki-no-kyojin-9734011.jpg
            if len(page_as_string) > 3:
                mode = "force_to_be_index"
            if mode == "force_to_be_index":
                page_as_string = str(i+1).zfill(3)

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
    if int(n) == n:
        n = str(n) + ",0"
    else:
        n = str(n).replace(".", ",")

    return n


def _get_lower_bound_as_string(n, chapters):
    """
    We want to get the lower bound for the bucket of chapters.
    00001-00010, 00011-00020, etc
    """
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


def _get_upper_bound_as_string(n, chapters):
    """
    We want to get the upper bound for the bucket of chapters.
    00001-00010, 00011-00020, etc
    """
    mod = n % BUCKETS_RANGE

    if mod == 0:
        upper = n
    else:
        upper = int((n + BUCKETS_RANGE) - (n % BUCKETS_RANGE))

    # we also want to ensure the highest chapter in a book title isn't above
    # CHAPTER_RANGE_START
    max_n = max(chapters)
    if upper > max_n:
        upper = max_n

    return _get_bound_as_string(upper)


def move():
    # once again, we want to backup the chapters
    chapters = backup(BACKUP_DIRECTORY + "_before_move")

    # we need the maximum chapter length
    if int(max(chapters)) == max(chapters):

        # example: if the max chapter is 14, it'll look like 14,0 in the
        # chapter title, and so we need a length of 4
        needed_zfill_length_chapter = len(str(max(chapters))) + 2

    else:

        # example: if the max chapter is 14.5, it'll look like 14,4 in the
        # chapter title, and so we need a length of 4
        needed_zfill_length_chapter = len(str(max(chapters)))

    # for every chapter...
    for chapter in chapters:

        # get the lower and upper bound for the bucket of chapters
        lower = str(_get_lower_bound_as_string(chapter, chapters)).\
            zfill(needed_zfill_length_chapter)
        upper = str(_get_upper_bound_as_string(chapter, chapters)).\
            zfill(needed_zfill_length_chapter)
        new_chapters_folder_range = "{}-{}".format(lower, upper)
        new_chapters_folder = CHAPTER_FOLDER_TEMPLATE.format(new_chapters_folder_range)

        # this is a hack... we really only need to create this directory once every BUCKETS_RANGE times
        if not os.path.isdir(new_chapters_folder):
            os.makedirs(new_chapters_folder)

        old_chapters_folder = CHAPTER_FOLDER_TEMPLATE.format(chapter)
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
        print(DEBUG_STAGE_FORMAT.format("convert"))
    convert()

    if DEBUG_BOOLEAN:
        print(DEBUG_STAGE_FORMAT.format("move"))
    move()

    if DEBUG_BOOLEAN:
        print(DEBUG_STAGE_FORMAT.format("archive"))
    archive()

    if DEBUG_BOOLEAN:
        print(DEBUG_STAGE_FORMAT.format("to_cbz"))
    to_cbz()
