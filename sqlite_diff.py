import os
import sqlite3
import sys

def main(sourceFile, destinationFile):
    sourceSql = exportSql(sourceFile)
    destinationSql = exportSql(destinationFile)
    os.system("cm diff " + sourceSql + " " + destinationSql)


def export_sql(dbFile):
    sqlFile = dbFile[:-3] + ".sql"
    connection = sqlite3.connect(dbFile)
    with open(sqlFile, 'w') as f:
        f.write("PRAGMA foreign_keys = off;\n")
        skipTable = False
        for line in connection.iterdump():
            if "CREATE TABLE" in line:
                tableName = line[13:line[13:].find(" ")+13]
                skipTable = False
                f.write("\n")
                f.write("--Table: " + tableName + "\n")
                f.write("%s\n" % line)
            elif "DELETE FROM" in line:
				# this is sqlite_sequence table, skip it
                skipTable = True
                continue
            elif "COMMIT" in line:
                continue
            elif skipTable is False:
                f.write("%s\n" % line)
        f.write("\n")
        f.write("COMMIT TRANSACTION;\n")
        f.write("PRAGMA foreign_keys = on;\n")
        return sqlFile

def get_column_names(line):
    # from a line containing a CREATE TABLE command return a string containing, in parentheses, a comma-separated list of the table's column names
    columnNames = []
    i = line.find("(")
    while True:
        line = line[i + 1:]
        i = line.find(" ")
        if i == -1:
            break
        s = line[:i]
        if s == "CONSTRAINT" or s == "PRIMARY" or s == "UNIQUE" or s == "CHECK" or s == "FOREIGN":
            # we have reached table constraints so there are no more columns
            break
        else:
            columnNames.append(s)
            i = line.find(", ") + 1
    temp = "("
    for columnName in columnNames:
        temp = temp + columnName + ", "
    columnNames = temp[:-2] + ")"
    return columnNames


if __name__ == "__main__":
    sourceFile = sys.argv[1]
    destinationFile = sys.argv[2]
    main(sourceFile, destinationFile)