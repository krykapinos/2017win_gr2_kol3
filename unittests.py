#github username: JakubKolybacz

import unittest
from kol1 import Wind, Route, Plane


class test_wind(unittest.TestCase):
	def setup(self):
		self.wind = Wind()


class test_route(unittest.TestCase):
	def setup(self):
		self.route = Route()



if __name__ == '__main__':
	unittest.main()
