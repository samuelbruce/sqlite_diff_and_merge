sqlite_diff_and_merge.py

A tool for diff and merge of sqlite databases in Plastic SCM.
It exports the contents of an sqlite .db file to a text .sql file.
Diff and merge are then handled by calling Plastic's mergetool.
After merge, the resulting .sql is imported back to the .db

HOW TO CONFIGURE IN PLASTIC:

Preferences -> Diff tools -> Add
	select "External diff tool"
	enter command line as follows (edit path to sqlite_diff_and_merge.py as necessary):
		python.exe "C:\Users\Xero\wkspaces\sqlite_diff_and_merge\sqlite_diff_and_merge.py" @sourcefile @destinationfile
	select "Use with files that match the following pattern:" and enter
		.db

Preferences -> Merge tools -> Add
	select "External merge tool"
	enter command line as follows (edit path to sqlite_diff_and_merge.py as necessary):
		python.exe "C:\Users\Xero\wkspaces\sqlite_diff_and_merge\sqlite_diff_and_merge.py" @sourcefile @destinationfile @basefile @output
	select "Use with files that match the following pattern:" and enter
		.db