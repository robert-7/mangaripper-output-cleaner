import os
from glob import glob
import numpy as np
import shutil
import re
from configparser import ConfigParser

CONFIG_FILE = "config.ini"
MANGA_SECTION = "manga"
TESTING_SECTION = "testing"

config = ConfigParser()
config.read(CONFIG_FILE)

# parse TITLE
TITLE = config[MANGA_SECTION]["TITLE"]
CHAPTER_FOLDER_TEMPLATE = TITLE + " {}"
# TODO: Add Check here

# parse CHAPTER_RANGE_START
CHAPTER_RANGE_START = config[MANGA_SECTION]["CHAPTER_RANGE_START"]
try:
    CHAPTER_RANGE_START = int(CHAPTER_RANGE_START)
    if CHAPTER_RANGE_START <= 0:
        raise Exception()
except:
    error_msg = "CHAPTER_RANGE_START must be whole number greater than zero. Currently, it is: {}"
    raise Exception(error_msg.format(CHAPTER_RANGE_START))
    
# parse CHAPTER_RANGE_FINISH
CHAPTER_RANGE_FINISH = config[MANGA_SECTION]["CHAPTER_RANGE_FINISH"]
try:
    CHAPTER_RANGE_FINISH = int(CHAPTER_RANGE_FINISH)
    if CHAPTER_RANGE_FINISH <= CHAPTER_RANGE_START:
        raise Exception()
except:
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
except:
    error_msg = "BACKUP_BOOLEAN must be either True or False. Currently, it is: {}"
    raise Exception(error_msg.format(BACKUP_BOOLEAN))

# obtain BACKUP_DIRECTORY
BACKUP_DIRECTORY = config[MANGA_SECTION]["BACKUP_DIRECTORY"]

# parse ZFILL_LENGTH
ZFILL_LENGTH = config[MANGA_SECTION]["ZFILL_LENGTH"]
try:
    ZFILL_LENGTH = int(ZFILL_LENGTH)
except:
    error_msg = "ZFILL_LENGTH must be whole number greater than zero. Currently, it is: {}"
    raise Exception(error_msg.format(ZFILL_LENGTH))
    
# parse DEBUG_BOOLEAN
DEBUG_BOOLEAN = config[TESTING_SECTION]["DEBUG_BOOLEAN"]
try:
    DEBUG_BOOLEAN = bool(DEBUG_BOOLEAN)
except:
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
    print("ZFILL_LENGTH = {}".format(ZFILL_LENGTH))
    
def get_number_of_images(path=".", extension=".jpg"):
  list_dir = []
  list_dir = os.listdir(path)
  count = 0
  for file in list_dir:
    if file.endswith(extension): # eg: '.txt'
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

def backup():
    temp_chapters = np.arange(CHAPTER_RANGE_START, CHAPTER_RANGE_FINISH, CHAPTER_INCREMENT).tolist()
    chapters = []
    if BACKUP_BOOLEAN:
        if os.path.isdir(BACKUP_DIRECTORY):
            shutil.rmtree(BACKUP_DIRECTORY)
        os.makedirs(BACKUP_DIRECTORY)
        for chapter_index in range(len(temp_chapters)):
            chapter = temp_chapters[chapter_index]
            if int(chapter) == chapter:
                chapter = int(chapter)
                temp_chapters[chapter_index] = chapter
            chapter_folder = CHAPTER_FOLDER_TEMPLATE.format(chapter)
            if os.path.isdir(chapter_folder):
                os.chdir(BACKUP_DIRECTORY)
                os.mkdir(chapter_folder)
                os.chdir("..")
                copytree(chapter_folder, BACKUP_DIRECTORY + "/" + chapter_folder)
                chapters.append(chapter)
    
    return chapters
            
def convert():
    chapters = backup()
    
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
                if ("cred" not in missed):
                    error_message = "Glob missed some images: total={}, glob_caught={}"
                    raise Exception(error_message.format(number_of_images, number_of_images_by_glob))
        
        duplicate_handler = 1
        
        for name in glob_caught_images:
            chapter_as_string = str(chapter).zfill(ZFILL_LENGTH)
            page_as_string = re.findall(r'\d+', name)[-1].zfill(3)
            new_name = "{}-{}.jpg".format(chapter_as_string, page_as_string)
            if DEBUG_BOOLEAN:
                print(name + " -> " + new_name)
            
            # handle diplicates
            if os.path.isfile(new_name):
                duplicate_handler += 1
                new_name = new_name + "-" + str(duplicate_handler)
            
            # rename the file
            os.rename(name, new_name)
                
        os.chdir("..")

def convert2():
    os.chdir(CHAPTER_FOLDER_TEMPLATE.format(chapter))
    for name in glob('*'):
        new_name = "{}.jpg".format(name)
        print(new_name)
        os.rename(name, new_name)

def get_lower_bound(n):
    """ 00001-00010, 00011-00020, etc"""
    divisor = 10
    mod = n % divisor
    
    if mod == 0:
        lower = (n - divisor) + 0.5
    else:
        lower = n - (n%divisor) + 0.5
    
    return lower
    
def get_upper_bound(n):
    """ 00001-00010, 00011-00020, etc"""
    divisor = 10
    mod = n % divisor
    
    if mod == 0:
        upper = n    
    else:
        upper = int((n + divisor) - (n%divisor))
    
    return upper
    
        
def move():
    chapters = backup()
    for chapter in chapters:
        
        lower = str(get_lower_bound(chapter)).replace(".", ",").zfill(ZFILL_LENGTH)
        upper = str(get_upper_bound(chapter)).zfill(ZFILL_LENGTH)
        new_chapters_folder_range = "{}-{}".format(lower, upper)
        new_chapters_folder = CHAPTER_FOLDER_TEMPLATE.format(new_chapters_folder_range)
        if not os.path.isdir(new_chapters_folder):
            os.makedirs(new_chapters_folder)
        
        old_chapters_folder = CHAPTER_FOLDER_TEMPLATE.format(chapter)
        os.chdir(old_chapters_folder)
        for name in glob('*'):
            os.rename(name, "../{}/{}".format(new_chapters_folder, name))
        os.chdir("..")
        shutil.rmtree(old_chapters_folder)
        
def archive():
    glob_template = CHAPTER_FOLDER_TEMPLATE.format("*,5-*")
    glob_caught_folders = glob(glob_template)
    for folder in glob_caught_folders:
        shutil.make_archive(folder, 'zip', folder)
        
def to_cbz():
    glob_template = CHAPTER_FOLDER_TEMPLATE.format("*,5-*.zip")
    glob_caught_folders = glob(glob_template)
    for zip_file in glob_caught_folders:
        cbz_file = zip_file.replace(".zip", ".cbz")
        os.rename(zip_file, cbz_file)
        
def all():
    convert()
    move()
    archive()
    to_cbz()
