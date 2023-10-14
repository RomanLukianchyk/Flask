import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


class WebAppTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Edge()

    def test_loads_common_report(self):
        self.driver.get("http://127.0.0.1:5000/report")

        self.assertEqual(self.driver.title, "Common Report")

    def test_loads_ordered_report(self):
        self.driver.get("http://127.0.0.1:5000/report/drivers")

        self.assertEqual(self.driver.title, "Ordered Report")

    def test_loads_driver_report(self):
        self.driver.get("http://127.0.0.1:5000/report/driver?driver_id=SVF")

        self.assertEqual(self.driver.title, "Driver Report")

    def test_loads_driver_list(self):
        self.driver.get("http://127.0.0.1:5000/driver_list")

        self.assertEqual(self.driver.title, "Driver List")

    def test_key_components_present_common_report(self):
        self.driver.get("http://127.0.0.1:5000/report")

        title_element = self.driver.find_element(By.TAG_NAME, "h1")
        best_time_element = self.driver.find_element(By.XPATH, "//h2[text()='Лучшее время:']")
        invalid_time_element = self.driver.find_element(By.XPATH, "//h2[text()='Гонщики с неправильным временем:']")

        self.assertTrue(title_element.is_displayed())
        self.assertTrue(best_time_element.is_displayed())
        self.assertTrue(invalid_time_element.is_displayed())

    def test_key_components_present_ordered_report(self):
        self.driver.get("http://127.0.0.1:5000/report/drivers")

        title_element = self.driver.find_element(By.TAG_NAME, "h1")
        sorting_element = self.driver.find_element(By.XPATH, "//h3[text()='Сортировка:']")
        best_time_element = self.driver.find_element(By.XPATH, "//h2[text()='Лучшее время:']")
        invalid_time_element = self.driver.find_element(By.XPATH, "//h2[text()='Гонщики с неправильным временем:']")

        self.assertTrue(title_element.is_displayed())
        self.assertTrue(sorting_element.is_displayed())
        self.assertTrue(best_time_element.is_displayed())
        self.assertTrue(invalid_time_element.is_displayed())

    def test_key_components_present_driver_list(self):
        self.driver.get("http://127.0.0.1:5000/driver_list")

        title_element = self.driver.find_element(By.TAG_NAME,"h1")
        driver_list_element = self.driver.find_element(By.TAG_NAME, "ul")

        self.assertTrue(title_element.is_displayed())
        self.assertTrue(driver_list_element.is_displayed())

    def test_key_components_present_driver_report(self):
        self.driver.get("http://127.0.0.1:5000/report/driver?driver_id=SVF")

        title_element = self.driver.find_element(By.TAG_NAME, "h1")
        best_time_element = self.driver.find_element(By.XPATH, "//h2[text()='Лучшее время гонщика:']")
        invalid_time_element = self.driver.find_element(By.XPATH, "//h4[text()='Гонщик с неправильным временем:']")

        self.assertTrue(title_element.is_displayed())
        self.assertTrue(best_time_element.is_displayed())
        self.assertTrue(invalid_time_element.is_displayed())


if __name__ == '__main__':
    unittest.main()
