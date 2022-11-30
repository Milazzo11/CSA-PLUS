CSA+ Grading Application

Rename zip file to "hw.zip"
Run hw_run.py

Use incomplete.py to unzip student folders in the "incomplete" folder.  
Will also create text files for comments with each student's name using the incomplete.txt file contents as a template.

Use inc_rezip.py to rezip all folders in the "incomplete" folder.  
This makes it really easy to unzip (using incomplete.py), correct the student's who submitted incorrectly, 
then rezip using inc_rezip.py, and then copy the zipped files back to the "hw" folder to continue using hw_run.py for the remaining assignments.

Use formatter.py to reformat comment data (will copy formatted comments to "fcomms" folder).

Use data_compile.py to import data into google sheets using API.

Optionally put files/directories to be copied into student submission folders in the "copylib" folder.