import mysql.connector

class DB:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Rajat@0707",
                auth_plugin='mysql_native_password'  # Specify the authentication plugin explicitly
            )
            self.mycursor = self.conn.cursor()
            print('Connection established')
        except mysql.connector.Error as err:
            print("Connection failed:", err)

    def fetch_city_names(self):
        try:
            self.mycursor.execute("""
            SELECT DISTINCT Destination FROM flights.flights
            UNION
            SELECT DISTINCT Source FROM flights.flights
            """)
            data = self.mycursor.fetchall()
            city = [row[0] for row in data]
            return city
        except mysql.connector.Error as err:
            print("Error fetching city names:", err)

    def fetch_all_flights(self, source, destination):
        try:
            self.mycursor.execute("""
            SELECT Airline, Route, Dep_Time, Duration, Price FROM flights.flights
            WHERE Source = %s AND Destination = %s
            """, (source, destination))
            data = self.mycursor.fetchall()
            return data
        except mysql.connector.Error as err:
            print("Error fetching flights:", err)

    def fetch_airline_frequency(self):

        airline= []
        frequency = []

        self.mycursor.execute("""SELECT Airline,COUNT(*) FROM flights.flights
        GROUP BY Airline
        """)

        data = self.mycursor.fetchall()

        for item in data:
            airline.append(item[0])
            frequency.append(item[1])

        return airline,frequency

    def busy_airport(self):

        city = []
        frequency = []

        self.mycursor.execute("""
        SELECT Source,COUNT(*) FROM (SELECT Source FROM flights.flights
							UNION ALL
							SELECT Destination FROM flights.flights) t
        GROUP BY t.Source
        ORDER BY COUNT(*) DESC
        """)

        data = self.mycursor.fetchall()

        for item in data:
            city.append(item[0])
            frequency.append(item[1])

        return city, frequency

    def daily_frequency(self):

        date = []
        frequency = []

        self.mycursor.execute("""
        SELECT Date_of_Journey,COUNT(*) FROM flights.flights
        GROUP BY Date_of_Journey
        """)

        data = self.mycursor.fetchall()

        for item in data:
            date.append(item[0])
            frequency.append(item[1])

        return date, frequency


