import sqlite3
import csv

import click
from flask import current_app
from flask import g


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

    """ Used for determining list of CSV columns.
    with open(current_app.root_path + "/schema.csv", newline='') as f:
        print('%r' % f)
        csvreader = csv.reader(f)
        columns = None
        for row in csvreader:
            columns = row
            break

        for column in columns:
            n = column.lower() \
                    .replace("# of ", "") \
                    .replace("(","") \
                    .replace(")","") \
                    .replace("?","") \
                    .replace(" ", "_")
            print(n)
    """

@click.command("import-csv")
@click.option('-f', '--file', help='Path to CSV to import.')
def import_csv(file):
    db = get_db()

    with open(file, newline='') as f:
        csvreader = csv.reader(f)
        columns = None
        first_row = True
        row_count = 1
        for row in csvreader:
            if first_row:
                columns = row
                first_row = False
                continue
            index = 0
            new_row = []
            for column in row:
                try:
                    normalized_column = columns[index].lower() \
                        .replace("# of ", "") \
                        .replace("(","") \
                        .replace(")","") \
                        .replace("?","") \
                        .replace(" ", "_")
                except:
                    print(index, row_count, row)
                    return
                new_row += [(normalized_column, column)]
                index += 1

            cs = ""
            vs = ""
            for x in new_row:
                cs += x[0] + ','
                vs += '"' + x[1] + '",'
            cs = cs[:-1]
            vs = vs[:-1]

            new_row_script = "INSERT INTO leads ({c}) VALUES ({v})".format( \
                c = cs,
                v = vs
            )
            try:
                db.executescript(new_row_script)
            except:
                print("error line {}".format(row_count))
                print(new_row_script)
                return
            row_count += 1
    db.commit()
    click.echo("Imported the CSV.")

@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(import_csv)
