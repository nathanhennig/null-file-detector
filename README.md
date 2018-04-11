# Null-File Detector

## Description and background:
When performing data recovery services, sometimes the damage is too significant to fully recover all files.  When that occurs, it often requires a great deal of time examining the recovered data and separating out the files that are damaged to the point of uselessness.
This tool is intended to significantly reduce the time spent on this stage of recovery by automating the process of examining files for damage.  None of the tools currently available are well-suited to this task.

## Requirements:
Python 2.7

## Usage:
The dist folder contains pre-compiled executables. The Windows executable supports drag-and-drop for single file scanning. The executable can be placed in a folder and ran using the GUI to scan that single folder.

For more detailed control, the executables can also be run at the command line level. Use the '--help' switch to see all command line options.
The program can also be run directly using Python 2.7 by running main.py in the null folder.

### Testing:
The test suite can be run by using 'python -m unittest discover' in the root of the repository. Please note that the last test will require 5-15 minutes to complete.

### Compiling:
The executables were compiled using py2exe for Windows and cx_freeze --onefile for Linux.