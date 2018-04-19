import unittest
from final_proj_yk import *





class TestDatabase(unittest.TestCase):

    def test_dog_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Name FROM Dogs'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Shiba Inu',), result_list)
        self.assertEqual(len(result_list), 190)

        sql = '''
            SELECT Name, [Rank], Height, Weight, LifeExpectancy
            FROM Dogs
	        WHERE Groups="Sporting Group"
            ORDER BY [Rank]
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        #print(result_list)
        self.assertEqual(len(result_list), 30)
        self.assertEqual(result_list[3][2], 11)
        self.assertEqual(result_lsit[29][4], 14)

        conn.close()

    # def test_groups_table(self):
    #     conn = sqlite3.connect(DBNAME)
    #     cur = conn.cursor()
    #
    #     sql = '''
    #         SELECT EnglishName
    #         FROM Countries
    #         WHERE Region="Oceania"
    #     '''
    #     results = cur.execute(sql)
    #     result_list = results.fetchall()
    #     self.assertIn(('Australia',), result_list)
    #     self.assertEqual(len(result_list), 27)
    #
    #     sql = '''
    #         SELECT COUNT(*)
    #         FROM Countries
    #     '''
    #     results = cur.execute(sql)
    #     count = results.fetchone()[0]
    #     self.assertEqual(count, 250)
    #
    #     conn.close()
    #
    # def test_joins(self):
    #     conn = sqlite3.connect(DBNAME)
    #     cur = conn.cursor()
    #
    #     sql = '''
    #         SELECT Alpha2
    #         FROM Bars
    #             JOIN Countries
    #             ON Bars.CompanyLocationId=Countries.Id
    #         WHERE SpecificBeanBarName="Hacienda Victoria"
    #             AND Company="Arete"
    #     '''
    #     results = cur.execute(sql)
    #     result_list = results.fetchall()
    #     self.assertIn(('US',), result_list)
    #     conn.close()



if __name__ == "__main__":
    unittest.main()
