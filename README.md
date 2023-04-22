# sqlite_diff_and_merge

A tool for diff and merge of sqlite databases in Plastic SCM.
It exports the contents of an sqlite .db file to an .sql file.
Diff and merge are then handled by calling Plastic's mergetool.
After merge, the resulting .sql is imported back to the .db

## HOW TO CONFIGURE IN PLASTIC:

### Configure Diff tool
* Preferences -> Diff tools -> Add
	* select "External diff tool"
	* enter command line as follows (edit path to sqlite_diff_and_merge workspace as necessary):
	* python.exe "PATH_TO_WORKSPACE\sqlite_diff_and_merge\sqlite_diff_and_merge.py" @sourcefile @destinationfile
	* select "Use with files that match the following pattern:" and enter
		* .db
	* change the order of rules so that .db rule is applied before $text and $bin

### Configure Merge tool
* Preferences -> Merge tools -> Add
	* select "External merge tool"
	* enter command line as follows (edit path to sqlite_diff_and_merge workspace as necessary):
		* python.exe "PATH_TO_WORKSPACE\sqlite_diff_and_merge.py" @sourcefile @destinationfile @basefile @output
	* select "Use with files that match the following pattern:" and enter
		* .db
	* change the order of rules so that .db rule is applied before $text and $bin

## NOTE:
An error may be raised in Plastic if the file type has not been set correctly.
If this happens, open "C:\Users\%USERNAME%\AppData\Local\plastic4\client.conf"
Find the <DiffToolData> or <MergeToolData> element that corresponds to the diff or merge tool
Change the content of the child <FileType> element to "enBinaryFile"

## HOW TO USE:
In pending changes or diff view, right-click on the .db file and select "External Diff", or highlight the file and hit Ctrl-D
