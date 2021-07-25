import datetime
import os
import sqlite3
import sys
import winsound


def diff(sourceFile, destinationFile):
    sourceSql = export_sql(sourceFile)
    destinationSql = export_sql(destinationFile)
    os.system("mergetool -s=" + sourceSql + " -d=" + destinationSql)
    # cleanup sql files
    for sqlFile in [sourceSql, destinationSql]:
        os.system("del " + sqlFile)


def merge(sourceFile, destinationFile, baseFile, outputFile):
    sourceSql = export_sql(sourceFile)
    destinationSql = export_sql(destinationFile)
    baseSql = export_sql(baseFile)
    outputSql = export_sql(outputFile)
    os.system("mergetool -s=" + sourceSql + " -d=" + destinationSql + " -b=" + baseSql + " -r=" + outputSql)
    import_sql(outputSql)
    # cleanup sql files
    for sqlFile in [sourceSql, destinationSql, baseSql, outputSql]:
        os.system("del " + sqlFile)


def export_sql(dbFile):
    # export contents of the .db file to an .sql file, mimicking the format of SQLiteStudio export
    sqlFile = dbFile[:-3] + ".sql"
    connection = sqlite3.connect(dbFile)
    with open(sqlFile, 'w') as f:
        # add header similar to SQLiteStudio export
        f.write("--\n")
        f.write("-- File generated with sqlite_diff_and_merge.py on " + datetime.datetime.now().strftime("%a %b %#d %H:%M:%S %Y") + "\n")
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


def import_sql(sqlFile):
    dbFile = sqlFile[:-4] + ".db"
    connection = sqlite3.connect(dbFile)
    cursor = connection.cursor()
    with open(sqlFile, "r") as f:   
        sql = f.read()
        cursor.executescript(sql)
    connection.commit()
    connection.close
    return dbFile


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
    # differentiate between diff and merge operations based on number of arguments
    if len(sys.argv) == 3:
        diff(sourceFile, destinationFile)
    elif len(sys.argv) == 5:
        baseFile = sys.argv[3]
        outputFile = sys.argv[4]
        merge(sourceFile, destinationFile, baseFile, outputFile)