import os
import sqlite3
import sys

def main(sourceFile, destinationFile):
    sourceSql = exportSql(sourceFile)
    destinationSql = exportSql(destinationFile)
    os.system("cm diff " + sourceSql + " " + destinationSql)
    input("Press Enter to continue...")


def exportSql(dbFile):
    sqlFile = dbFile[:-3] + ".sql"
    connection = sqlite3.connect(dbFile)
    with open(sqlFile, 'w') as f:
        f.write("PRAGMA foreign_keys = off;\n")
        for line in connection.iterdump():
            if "CREATE TABLE" in line:
                f.write("\n")
                f.write("--Table:\n")
            elif "COMMIT" in line:
                continue
            f.write("%s\n" % line)
        f.write("\n")
        f.write("COMMIT TRANSACTION;\n")
        f.write("PRAGMA foreign_keys = on;\n")
        return sqlFile


if __name__ == "__main__":
    sourceFile = sys.argv[1]
    destinationFile = sys.argv[2]
    main(sourceFile, destinationFile)