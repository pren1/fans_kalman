import pandas as pd

class data_preprocessor(object):
	def __init__(self):
		'time interpolation interval: 5min = 5*60*1000ms'
		self.time_interpolation_interval = 5*60*1000

	def read_in_csv(self, file_name):
		# Read data from file 'filename.csv'
		# (in the same directory that your python process is based)
		self.data = pd.read_csv(file_name, header=None)
		# Preview the first 5 lines of the loaded data
		print(f"read in data: {self.data.head()}")

	def preprocess(self):
		time_line = self.data[0]
		follower_line = self.data[1]
		'First, let the timeline starts at zero'
		time_line -= time_line[0]
		time_line /= self.time_interpolation_interval
		'change type to int, we need integer here'
		time_line = time_line.astype(int)
		'build the origin data frame'
		origin_dataframe = pd.DataFrame(zip(time_line, follower_line), columns=['time', 'follower'])
		return origin_dataframe