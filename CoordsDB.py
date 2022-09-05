import sqlite3

class CoordsDB:
    def __init__(self):
        self._conn = None
        
        self._create_coords_table()

    def execute_query(self, query): # this query should never and will never recieve user input
        self._connect()
        cursor = self._conn.cursor()

        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()
        self._disconnect()

        return result

    def _connect(self):
        self._conn = sqlite3.connect('coords.db')

    def _disconnect(self):
        if self._conn:
            self._conn.close()

    # this probably only gets called manually while im setting up, forgot the if it diesnt exist
    def _create_coords_table(self):
        query = '''CREATE TABLE IF NOT EXISTS `coords` (
`xcoord` INTEGER NOT NULL,
`ycoord` INTEGER NOT NULL,
`zcoord` INTEGER NOT NULL,
`desc` VARCHAR(256),
`dim` VARCHAR(10)
);'''
        self.execute_query(query)

    def add_coord(self, xcoord, ycoord, zcoord, description, dimension):
        self._connect()
        cursor = self._conn.cursor()

        query = '''INSERT INTO coords
VALUES(?, ?, ?, ?, ?);
'''
        cursor.execute(query, (xcoord, ycoord, zcoord, description, dimension))

        res = cursor.fetchone()

        self._conn.commit()

        cursor.close()
        self._disconnect()

        print(res)

        return "joe"