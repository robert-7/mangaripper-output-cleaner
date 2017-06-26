import os
from glob import glob
import numpy as np
import shutil
import re

CHAPTER_FOLDER_TEMPLATE = "Shingeki no Kyojin Gaiden - Kuinaki Sentaku {}"
CHAPTER_RANGE_START  = 0.5
CHAPTER_RANGE_FINISH = 9
CHAPTER_INCREMENT = 0.5
BACKUP_BOOLEAN = True
BACKUP_DIRECTORY = "backup"
ZFILL_LENGTH = 5

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
        chapter_folder = CHAPTER_FOLDER_TEMPLATE.format(chapter)
        os.chdir(chapter_folder)
        
        number_of_images = get_number_of_images()
        glob_caught_images = glob('*[0-9][0-9][0-9]*.jpg')
        number_of_images_by_glob = len(glob_caught_images)
        if number_of_images != number_of_images_by_glob:
            error_message = "Glob missed some images: total={}, glob_caught={}"
            raise Exception(error_message.format(number_of_images, number_of_images_by_glob))
        
        duplicate_handler = 1
        
        for name in glob_caught_images:
            chapter_as_string = str(chapter).zfill(ZFILL_LENGTH)
            page_as_string = re.findall(r'\d+', name)[-1].zfill(3)
            new_name = "{}-{}.jpg".format(chapter_as_string, page_as_string)
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