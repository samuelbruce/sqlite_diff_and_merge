import os
import sqlite3
import sys

def main(sourceFile, destinationFile):
    sourceSql = exportSql(sourceFile)
    destinationSql = exportSql(destinationFile)
    os.system("cm diff " + sourceSql + " " + destinationSql)


def exportSql(dbFile):
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


if __name__ == "__main__":
    sourceFile = sys.argv[1]
    destinationFile = sys.argv[2]
    main(sourceFile, destinationFile)