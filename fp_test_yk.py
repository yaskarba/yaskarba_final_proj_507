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
        self.assertEqual(result_list[29][4], 14)

        conn.close()

    def test_groups_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT GroupName
            FROM Groups
            WHERE Id=6
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        for item in result_list:
            x=item[0]
        y=x.strip()
        self.assertEqual(y, "Terrier Group")

        sql = '''
            SELECT COUNT(*)
            FROM Groups
        '''
        results = cur.execute(sql)
        count = results.fetchone()[0]
        self.assertEqual(count, 7)

        conn.close()


class TestGraphing(unittest.TestCase):
    def test_weights(self):
        try:
            plot_weights()
        except:
            self.fail()
    def test_heights(self):
        try:
            plot_heights()
        except:
            self.fail()
    def test_life_expectancys(self):
        try:
            plot_life_expectancy()
        except:
            self.fail()

    def test_compare(self):
        try:
            compare_dogs("Shiba Inu", "Tibetan Spaniel")
        except:
            self.fail()

class TestAverages(unittest.TestCase):
    def test_weights(self):
        group_list=["Sporting Group", "Working Group", "Toy Group", "Non-Sporting Group", "Herding Group", "Terrier Group", "Hound Group"]
        test_1=weights()
        self.assertEqual(test_1[0], 52.0)
        self.assertEqual(len(test_1), 7)

    def test_heights(self):
        group_list=["Sporting Group", "Working Group", "Toy Group", "Non-Sporting Group", "Herding Group", "Terrier Group", "Hound Group"]
        test_2=heights()
        self.assertEqual(test_2[6], 20.73)
    def test_life_expectancys(self):
        test_3=life_expectancy()
        self.assertEqual(test_3[5], 13.1)






if __name__ == "__main__":
    unittest.main()
