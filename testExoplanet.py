import unittest
import pandas
from exoplanetHomework import fetch_data, count_orphan_planets, find_hottest_host, create_timeline_summary

class TestExoplanetFunctions(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.url = "https://gist.githubusercontent.com/joelbirchler/66cf8045fcbb6515557347c05d789b4a/raw/9a196385b44d4288431eef74896c0512bad3defe/exoplanets"
        cls.dataframe = fetch_data(cls.url)
    
    def test_fetch_data(self):
        df = fetch_data(self.url)
        self.assertIsInstance(df, pandas.DataFrame)
    
    def test_count_orphan_planets(self):
        count = count_orphan_planets(self.dataframe)
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)
    
    def test_find_hottest_host(self):
        hottest_host = find_hottest_host(self.dataframe)
        self.assertIsInstance(hottest_host, str)
    
    def test_create_timeline_summary(self):
        summary = create_timeline_summary(self.dataframe)
        self.assertIsInstance(summary, pandas.DataFrame)

if __name__ == '__main__':
    unittest.main()
