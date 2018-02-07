import time

# Regular Price - Keep Normal Pricing
class UseRateCalc():
	def __init__(self):
		# Regular Price - Keep Normal Pricing
		self.BUS_TYPES1 = {
			'14_pax': {
				'base_price' : 365,
				'extra_hourly_price': 85,
				'image_path': ''
			},
			'23_pax': {
				'base_price' : 440,
				'extra_hourly_price': 90,
				'image_path': ''
			},
			'28_pax': {
				'base_price' : 500,
				'extra_hourly_price': 95,
				'image_path': ''
			},
			'40_pax': {
				'base_price': 540,
				'extra_hourly_price': 95,
				'image_path': ''
			},
			'49_pax': {
				'base_price': 600,
				'extra_hourly_price': 105,
				'image_path': ''
			}
		}

		# BUS_TYPES2 Price Decrease - Low Demand
		self.BUS_TYPES2 = {
			'14_pax': {
				'base_price' : 365,
				'extra_hourly_price': 70,
				'image_path': ''
			},
			'23_pax': {
				'base_price' : 440,
				'extra_hourly_price': 75,
				'image_path': ''
			},
			'28_pax': {
				'base_price' : 500,
				'extra_hourly_price': 80,
				'image_path': ''
			},
			'40_pax': {
				'base_price': 540,
				'extra_hourly_price': 80,
				'image_path': ''
			},
			'49_pax': {
				'base_price': 600,
				'extra_hourly_price': 90,
				'image_path': ''
			}
		}

		# BUS_TYPES3 Price Increase - High Demand
		self.BUS_TYPES3 = {
			'14_pax': {
				'base_price': 365,
				'extra_hourly_price': 95,
				'image_path': ''
			},
			'23_pax': {
				'base_price': 440,
				'extra_hourly_price': 100,
				'image_path': ''
			},
			'28_pax': {
				'base_price': 500,
				'extra_hourly_price': 105,
				'image_path': ''
			},
			'40_pax': {
				'base_price': 540,
				'extra_hourly_price': 110,
				'image_path': ''
			},
			'49_pax': {
				'base_price': 600,
				'extra_hourly_price': 115,
				'image_path': ''
			}
		}

		"""Storage for both peak and slow dates"""
		self.price_idx = {
			'premium' : {
				'Jan': [4, 6, 11, 12, 13, 16, 20, 21, 27, 28, 29, 31], 
				'Feb': [1, 3, 4, 8, 10, 12, 14, 15, 16, 17, 23, 24],
				'Mar': [2, 3, 4, 13, 16, 17, 21, 23, 24, 27, 28], 
				'Apr': [4, 6, 18, 19, 20, 21, 22, 23, 25, 27, 28],
				'May': [5, 6, 13, 15, 16, 19, 20, 21, 26, 27, 28], 
				'Jun': [2, 4, 6, 9, 10, 16, 17, 20, 22, 23, 24, 25, 30],
				'Jul': [1, 2, 7, 8, 9, 14, 21, 22, 23, 25, 28, 29, 30], 
				'Aug': [4, 5, 6, 8, 11, 12, 13, 18, 19, 20, 25, 26],
				'Sep': [1, 2, 8, 9, 10, 15, 16, 17, 22, 23, 29], 
				'Oct': [5, 6, 7, 10, 11, 12, 16, 17, 21, 26, 27, 28],
				'Nov': [2, 3, 4, 7, 16, 17, 18, 19, 28, 30], 
				'Dec': [1, 2, 7, 8, 9, 12, 13, 14, 15]
			},
			'discount':{
				'Jan': [2, 3, 7, 8, 9, 14, 15, 18, 19, 23, 25], 
				'Feb': [6, 9, 11, 13, 21, 25, 28],
				'Mar': [1, 5, 6, 7, 8, 11, 12, 15, 18, 19, 21, 25, 26], 
				'Apr': [1, 8, 9, 10, 13, 14, 15, 16],
				'May': [1, 4, 9, 10, 17, 22, 24, 25, 29, 31], 
				'Jun': [1, 5, 12, 14, 15, 19, 21, 28],
				'Jul': [3, 5, 6, 10, 12, 13, 19, 26], 
				'Aug': [7, 9, 10, 16, 21, 23, 28, 30, 31],
				'Sep': [4, 5, 6, 7, 12, 18, 25, 28], 
				'Oct': [1, 2, 4, 8, 15, 21, 22, 29, 30, 31],
				'Nov': [9, 12, 13, 21, 22, 23, 29], 
				'Dec': [4, 11, 16, 17, 18, 21, 22, 23, 31]
			}
		}

		return

	# -- get seconds from hours --
	def get_seconds(self, web_date):
		tmp = web_date.split(" ")
		if len(tmp) == 2:
			tmpsecs = time.strptime(tmp[0]+" "+tmp[1], "%d/%m/%Y %H")
		if len(tmp) < 2:
			tmpsecs = time.strptime(tmp[0]+" 00", "%d/%m/%Y %H")
		web_secs = time.mktime(tmpsecs)

		return web_secs

	def base_rental_cost(self, rates, bus_type, static_cost):
		return rates[bus_type]['base_price']


	def additional_rental_cost(self, rates, bus_type, hours):
		hours = max(0, hours)  # This will normalize any negative numbers to 0

		return hours * rates[bus_type]['extra_hourly_price']


	#def total_cost(bus_type, hours, use_rate):
	def total_cost(self, start_date, end_date, mileage):
		rates = self.BUS_TYPES1

		curr_month = time.strftime("%b", time.localtime())
		curr_day = int(time.strftime("%d", time.localtime()))

		if curr_month in self.price_idx['premium'].keys():
			if curr_day in self.price_idx['premium'][curr_month]:
				rates = self.BUS_TYPES2
		if curr_month in self.price_idx['discount'].keys():
			if curr_day in self.price_idx['discount'][curr_month]:
				rates = self.BUS_TYPES3

		# -- get hours --
		start_secs = self.get_seconds(start_date)
		end_secs = self.get_seconds(end_date)
		hours = int((end_secs - start_secs) / 3600)

		extra_hours = hours - 3

		# -- calculate price --
		prices = []
		for i in rates.keys():
			base_price = self.base_rental_cost(rates, i, mileage)
			additional = self.additional_rental_cost(rates, i, extra_hours)
			prices.append({'bus_type': i, 'price': base_price + additional, 'image': rates[i]['image_path']})

		#return self.base_rental_cost(rates, bus_type, use_rate) + self.additional_rental_cost(rates, bus_type, extra_hours)
		return prices


# FIrst version tool
# Baseline for building next level tool
class DateCalculator():
	def __init__(self):
		self.mileage_calculator(600)

		self.bus_types = {
			'14_pax': {
				'base_price': 365,
				'extra_hourly_price': 85
			},
			'23_pax': {
				'base_price': 440,
				'extra_hourly_price': 90
			},
			'28_pax': {
				'base_price': 500,
				'extra_hourly_price': 95
			},
			'40_pax': {
				'base_price': 540,
				'extra_hourly_price': 95
			},
			'49_pax': {
				'base_price': 600,
				'extra_hourly_price': 105
			},
		}

		return

	def mileage_calculator(self, x):
		return x * .42

	def base_rental_cost(self, bus_type):
		return self.bus_types[bus_type]['base_price']

	def additional_rental_cost(self, bus_type, hours):
		hours = max(0, hours)  # This will normalize any negative numbers to 0
		return hours * self.bus_types[bus_type]['extra_hourly_price']

	def total_cost(self, bus_type, hours):
		extra_hours = hours - 3
		return self.base_rental_cost(bus_type) + self.additional_rental_cost(bus_type, extra_hours)




date_price = DateCalculator()
use_rt = UseRateCalc()
