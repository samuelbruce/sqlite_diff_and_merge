import datetime
import os
import sqlite3
import sys


def diff(sourceFile, destinationFile):
    sourceSql = export_sql(sourceFile)
    destinationSql = export_sql(destinationFile)
    os.system("cm diff " + sourceSql + " " + destinationSql)


def merge(sourceFiles, destinationFile, baseFile, outputFile):
    sourceSql = export_sql(sourceFile)
    destinationSql = export_sql(destinationFile)
    baseSql = export_sql(baseFile)

def export_sql(dbFile):
    # export contents of the .db file to an .sql file, mimicking the format of SQLiteStudio export
    sqlFile = dbFile[:-3] + ".sql"
    connection = sqlite3.connect(dbFile)
    with open(sqlFile, 'w') as f:
        # add header similar to SQLiteStudio export
        f.write("--\n")
        f.write("-- File generated with sqlite_diff.py on " + datetime.datetime.now().strftime("%a %b %#d %H:%M:%S %Y") + "\n")
        f.write("--\n")
        f.write("-- Text encoding used: UTF-8\n")
        f.write("--\n")
        f.write("PRAGMA foreign_keys = off;\n")
        tableName = ""
        columnNames = ""
        skipTable = False
        for line in connection.iterdump():
            if "CREATE TABLE" in line:
                tableName = line[13:line[13:].find(" ")+13]
                columnNames = get_column_names(line)
                skipTable = False
                f.write("\n")
                f.write("-- Table: " + tableName + "\n")
                f.write("DROP TABLE IF EXISTS " + tableName + ";\n")
                f.write("%s\n" % line)
            elif "DELETE FROM" in line:
				# this is sqlite_sequence table, skip it
                skipTable = True
                continue
            elif "COMMIT" in line:
                continue
            elif skipTable is False:
                if "INSERT INTO" in line:
                    # remove quotes around table name
                    t = line.find(tableName)
                    line = line[:t - 1] + tableName + line[t + len(tableName) + 1:]
                    v = line.find("VALUES")
                    # add space after VALUES
                    line = line[:v + 6] + " " + line[v + 6:]
                    # add column names before VALUES, add spaces after commas in VALUES clause
                    line = line[:v - 1] + " " + columnNames + " " + line[v:].replace(",", ", ")
                f.write("%s\n" % line)
        f.write("\n")
        f.write("COMMIT TRANSACTION;\n")
        f.write("PRAGMA foreign_keys = on;\n")
        return sqlFile

def get_column_names(line):
    # from a line containing a CREATE TABLE command return a string containing, in parentheses, a comma-separated list of the table's column names
    # tested for all cases in cpq.db as at 23/07/21
    columnNames = []
    i = line.find("(")
    while True:
        # truncate start of line
        line = line[i + 1:]
        # find the next space or comma, whichever comes first
        i = line.find(" ")
        j = line.find(",")
        if j > 0:
            i = min(i, j)
        if i == -1:
            # there are no more spaces, this is the last column and has no type name
            i = line.find(")")
            s = line[:i]
        else:
            s = line[:i]
            if ")" in s:
                # deal with cases ending in WITHOUT ROWID
                s = s[:-1]
        if "CONSTRAINT" in s or "PRIMARY" in s or "UNIQUE" in s or "CHECK" in s or "FOREIGN" in s:
            # we have reached table constraints so there are no more columns
            break
        else:
            columnNames.append(s)
            i = line.find(", ") + 1
            if i == 0:
                # there are no more commas so there are no more columns
                break
    temp = "("
    for columnName in columnNames:
        temp = temp + columnName + ", "
    columnNames = temp[:-2] + ")"
    return columnNames


if __name__ == "__main__":
    sourceFile = sys.argv[1]
    destinationFile = sys.argv[2]
    if len(sys.argv) == 3:
        diff(sourceFile, destinationFile)
    elif len(sys.argv) == 5:
        merge(sourceFiles, destinationFile, baseFile, outputFile)