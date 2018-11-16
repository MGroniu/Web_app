import sqlite3


class CinemaModel:
############################contructor #####################################


    def __init__(self,cinema_id="",database_path="",movie_id=""):
        self.cinema_id = cinema_id
        self.database_path = database_path
        self.movie_id = movie_id


#################################################################  Movies Module ###########################################
    def get_all_movies(self):
        try:
            conn = sqlite3.connect(self.database_path)
            cur = conn.cursor()
            result = cur.execute("select movie_id, movie_name from movie_details")
            data = result.fetchall()
            conn.close()
        except Exception as e:
            print(e)
        return data


    def get_movies(self):
        try:
            conn = sqlite3.connect(self.database_path)
            cur = conn.cursor()
            result = cur.execute("select * from cinema_details cd "+
    "inner join movie_cinema_price_time mcpt on cd.cinema_id=mcpt.cinema_id "+
    "inner join movie_details md on mcpt.movie_id=md.movie_id "+
    "where cd.cinema_id = ?", self.cinema_id)
            data = result.fetchall()
            conn.close()
        except Exception as e:
            print(e)
        return data


    def get_all_movies_added(self):
        try:
            conn = sqlite3.connect(self.database_path)
            cur = conn.cursor()
            result = cur.execute("select * from cinema_details cd "+
    "inner join movie_cinema_price_time mcpt on cd.cinema_id=mcpt.cinema_id "+
    "inner join movie_details md on mcpt.movie_id=md.movie_id ")
            data = result.fetchall()
            conn.close()
        except Exception as e:
            print(e)
        return data



    def get_movie(self):
        try:
            conn = sqlite3.connect(self.database_path)
            cur = conn.cursor()
            result = cur.execute("select * from cinema_details cd " +
                                 "inner join movie_cinema_price_time mcpt on cd.cinema_id=mcpt.cinema_id " +
                                 "inner join movie_details md on mcpt.movie_id=md.movie_id " +
                                 "where md.movie_id=:movie_id and cd.cinema_id=:cinema_id", {"movie_id": self.movie_id, "cinema_id": self.cinema_id})
            print("result = ", result)
            data = result.fetchone()
            print(data)

            conn.close()
        except Exception as e:
            print(e)
        return data

####################################### Movie Module #####################
    def get_movie_details(self):
        try:
            conn = sqlite3.connect(self.database_path)
            cur = conn.cursor()
            result = cur.execute("SELECT * FROM movie_details")
            data = result.fetchall()
            print(data)
            conn.close()
        except Exception as e:
            print(e)
        return data
    def delete_movie_details(self):
        try:
            conn = sqlite3.connect(self.database_path)
            cur = conn.cursor()
            print(self.movie_id)
            rows_affected = cur.execute("Delete from movie_details where movie_id = ?",self.movie_id)

            conn.commit()
            print(rows_affected.rowcount)
            message = 1

            cur.close()
            return message
        except Exception as e: print(e)

        cur.close()
        message = 0
        return message


    def insert_movie_details(self,data):
        try:
            conn = sqlite3.connect(self.database_path)
            cur = conn.cursor()
            rows_affected = cur.execute("INSERT INTO movie_details(movie_name, movie_desc) VALUES(?, ?)",
                        (data[0], data[1]))

            conn.commit()
            message = 1
            cur.close()
            return message
        except Exception as e: print(e)

        cur.close()
        message = 0
        return message

####################################### Cinema Module ########################
    def get_cinema_details(self):
        try:
            conn = sqlite3.connect(self.database_path)
            cur = conn.cursor()
            result = cur.execute("SELECT * FROM cinema_details")
            data = result.fetchall()
            print(data)
            conn.close()
        except Exception as e:
            print(e)
        return data

    def get_cinema_details_by_id(self):
        try:
            conn = sqlite3.connect(self.database_path)
            cur = conn.cursor()
            result = cur.execute("SELECT * FROM cinema_details where cinema_id = ?", self.cinema_id)
            data = result.fetchall()
            conn.close()
        except Exception as e:
            print(e)
        return data



    def insert_cinema_details(self,data):
        try:
            print(data)
            conn = sqlite3.connect(self.database_path)
            cur = conn.cursor()
            rows_affected = cur.execute("INSERT INTO cinema_details(cinema_name, cinema_address) VALUES(?, ?)",
                        (data[0], data[1]))

            conn.commit()
            print(rows_affected.rowcount)
            message = 1

            cur.close()
            return message
        except Exception as e: print(e)

        cur.close()
        message = 0
        return message

    def deleteCinema(self):

        try:
            conn = sqlite3.connect(self.database_path)
            cur = conn.cursor()
            print(self.cinema_id)
            rows_affected = cur.execute("Delete from cinema_details where cinema_id = ?",self.cinema_id)

            conn.commit()
            print(rows_affected.rowcount)
            message = 1

            cur.close()
            return message
        except Exception as e: print(e)

        cur.close()
        message = 0
        return message


    def updateCinema(self,data):

        try:
            conn = sqlite3.connect(self.database_path)
            cur = conn.cursor()
            print("model",self.cinema_id)
            print(data[0])
            rows_affected = cur.execute(" UPDATE cinema_details SET cinema_name = ?, cinema_address = ? WHERE cinema_id = ?", (data[0],data[1],self.cinema_id))

            conn.commit()
            print(rows_affected.rowcount)
            message = 1

            cur.close()
            return message
        except Exception as e: print(e)

        cur.close()
        message = 0
        return message




#######################################################################################################################



    def insert_movie_cinema_price_time(self, data):
        try:
            print(data)
            conn = sqlite3.connect(self.database_path)
            cur = conn.cursor()
            rows_affected = cur.execute("INSERT INTO movie_cinema_price_time(cinema_id, movie_id, ticket_price, movie_time) VALUES(?, ?,?,?)",
                                        (data[0], data[1],data[2],data[3]))

            conn.commit()
            print(rows_affected.rowcount)
            message = 1

            cur.close()
            return message
        except:

            cur.close()
            message = 0
            return message



    def deleteMovieToCinema(self,id):

        try:
            conn = sqlite3.connect(self.database_path)
            cur = conn.cursor()
            print(self.cinema_id)
            rows_affected = cur.execute("Delete from movie_cinema_price_time where movie_price_time_id = ?",id)

            conn.commit()
            print(rows_affected.rowcount)
            message = 1

            cur.close()
            return message
        except:

            cur.close()
            message = 0
            return message


######################################Seats module###################################
    def insert_movie_cinema_seats(self,cinema_id,movie_id):

        try:
            print(cinema_id)
            print(movie_id)
            data=[]
            data.append(cinema_id)
            data.append(movie_id)
            i = 0
            seat = "available"
            while i < 9:
                data.append(seat)
                i+=1

            conn = sqlite3.connect(self.database_path)
            cur = conn.cursor()
            rows_affected = cur.execute(
                "INSERT INTO seats(cinema_id, movie_id, A1, A2 ,A3,A4,B1,B2,B3,B4) VALUES(?, ?,?,?,?,?,?,?,?,?)",
                (data[0], data[1], data[2], data[3],data[4],data[5],data[6],data[7],data[8],data[9]))

            conn.commit()
            print(rows_affected.rowcount)
            message = 1

            cur.close()
            return message
        except:

            cur.close()
            message = 0
            return message


    def get_seat_status(self):
        try:
            conn = sqlite3.connect(self.database_path)
            cur = conn.cursor()
            result = cur.execute("SELECT * FROM seats where cinema_id = ? and movie_id = ?", (self.cinema_id,self.movie_id))
            conn.commit()
            data = result.fetchall()
            conn.close()
        except Exception as e:
            print(e)
        return data

    def update_seat_status(self,seats):
        try:
            split_seats=seats.split(",")
            status = "not-available"
            print(self.cinema_id)
            print(self.movie_id)
            conn = sqlite3.connect(self.database_path)
            cur = conn.cursor()
            for item in split_seats:
                cur.execute("UPDATE seats SET " + item + " = ? WHERE cinema_id = ? and movie_id = ?", (status,self.cinema_id,self.movie_id))
                conn.commit()

            conn.close()
        except Exception as e:
            print(e)

