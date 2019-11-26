class Rectangle:
	def __init__(self, length, breadth, unit_cost):
		self.length = length
		self.breadth = breadth
		self.unit_cost = unit_cost
	def get_perimeter(self):
		return 2 * (self.length + self.breadth)
	def get_area(self):
		return self.length * self.breadth
	def calculate_cost(self):
		area = self.get_area()
		return area * self.unit_cost
		# breadth = 120 cm, length = 160 cm, 1 cm^2 = Rs 2000
r = Rectangle(160, 120, 2000)
q = Rectangle(160,120,1000)
if (r or q):
	print(r is q)
print("Area of Rectangle: %s cm^2" % (r.get_area())
print("Cost of rectangular field: Rs. %s " %(r.calculate_cost())