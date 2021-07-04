import os
import sqlite3
from pathlib import Path

DB_PATH = os.path.join(
    Path(__file__).parents[2],
    'database/product_meta_analysis.db'
    )


class Database:
    def __init__(self, path=DB_PATH):
        self._con = sqlite3.connect(path)
        self._cur = self._con.cursor()

    def write(self, query):
        self._cur.execute(query)
        self._con.commit()

    def write_pandas(self, df, name):
        df.to_sql(name='name', con=self._con)
        self._con.commit()

    def read(self, query):
        self._cur.execute(query)
        result = self._cur.fetchall()
        return result

    def drop(self, name):
        query = f"""DROP TABLE {name}"""
        self.write(query)

    def close(self):
        self._con.close()
