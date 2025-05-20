from database.DB_connect import DBConnect
from model.retailers import Retailer
from model.edges import Edge

class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllRetailers():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """SELECT * from go_retailers"""

        cursor.execute(query)

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(year, country):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """SELECT least(gr1.Retailer_code, gr2.Retailer_code) as Retailer1, greatest(gr1.Retailer_code, gr2.Retailer_code) as Retailer2, COUNT(DISTINCT s1.Product_number) as peso
                   FROM go_daily_sales s1, go_daily_sales s2, go_retailers gr1, go_retailers gr2
                   WHERE YEAR(s1.Date) = YEAR(s2.Date) AND YEAR(s1.Date) = %s
                   and gr1.Country = %s and gr2.Country = %s
                   AND gr1.Retailer_code > gr2.Retailer_code
                   AND s1.Product_number = s2.Product_number
                   and s1.Retailer_code = gr1.Retailer_code and s2.Retailer_code = gr2.Retailer_code
                   GROUP BY gr1.Retailer_code, gr2.Retailer_code"""

        cursor.execute(query, (year, country, country,))

        for row in cursor:
            result.append(Edge(**row))

        cursor.close()
        conn.close()
        return result

