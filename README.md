# mangaripper-output-cleaner
After downloading manga using MangaRipper, this program renames the files and folders to give the user files that are more Kobo/Kindle-friendly.

# Usage 

The commands listed below can be used to restructure your files. By default, it will always create a backup of the chapter folders and the `./backup` folder.

## convert()
This command cleans the filenames by renaming them to a zero-padded `CHAPTER-PAGE` format. Example:

| Pathname Before                | Pathname After                     |
| ------------------------------ | ---------------------------------- |
| Shingeki no Kyojin 1/a0001.jpg | Shingeki no Kyojin 1/00001-001.jpg |
| Shingeki no Kyojin 1/a0002.jpg | Shingeki no Kyojin 1/00001-002.jpg |
| ...                            | ...                                |
| Shingeki no Kyojin 1/a0044.jpg | Shingeki no Kyojin 1/00001-044.jpg |
| Shingeki no Kyojin 2/b0001.jpg | Shingeki no Kyojin 2/00002-001.jpg |
| ...                            | ...                                |

## move()
Moves the files to grouped folders. Example:

| Pathname Before                     | Pathname After                               |
| ----------------------------------- | -------------------------------------------- |
| Shingeki no Kyojin 1/00001-001.jpg  | Shingeki no Kyojin 0000,5-0010/00001-001.jpg |
| Shingeki no Kyojin 1/00001-002.jpg  | Shingeki no Kyojin 0000,5-0010/00001-002.jpg |
| ...                                 | ...                                          |
| Shingeki no Kyojin 1/00001-044.jpg  | Shingeki no Kyojin 0000,5-0010/00001-044.jpg |
| Shingeki no Kyojin 2/00002-001.jpg  | Shingeki no Kyojin 0000,5-0010/00002-001.jpg |
| ...                                 | ...                                          |
| Shingeki no Kyojin 11/00011-001.jpg | Shingeki no Kyojin 0010,5-0020/00011-001.jpg |
| ...                                 | ...                                          |

## archive()
Archive the folders. The default, and only supported format, is .zip. Example:

| Pathname Before                 | Pathname After                     |
| ------------------------------- | ---------------------------------- |
| Shingeki no Kyojin 0000,5-0010\ | Shingeki no Kyojin 0000,5-0010.zip |
| Shingeki no Kyojin 0010,5-0020\ | Shingeki no Kyojin 0010,5-0020.zip |
| ...                             | ...                                |

## to_cbz()
Renames the archived files so they end in the .cbz format -- one that is handled by Kobo and Kindle e-book readers. Example:

| Pathname Before                    | Pathname After                     |
| ---------------------------------- | ---------------------------------- |
| Shingeki no Kyojin 0000,5-0010.zip | Shingeki no Kyojin 0000,5-0010.cbz |
| Shingeki no Kyojin 0010,5-0020.zip | Shingeki no Kyojin 0010,5-0020.cbz |
| ...                                | ...                                |

## all()
Performs the actions in order:
* convert()
* move()
* archive()
* to_cbz()

# Issues
If you experience any issues, please add them here: https://github.com/robert-7/mangaripper-output-cleaner/issues . It's known to the author that the downloaded images can have many exceptional names that break the format. These cases are handled on a case-by-case basis.
