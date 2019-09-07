import pandas as pd
import matplotlib.pyplot as plt
import pdb

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
		'time interpolation process'
		time_line /= self.time_interpolation_interval
		'change type to int, we need integer here'
		time_line = time_line.astype(int)
		'build the origin data frame for evaluate'
		origin_dataframe = pd.DataFrame(zip(time_line, follower_line), columns=['time', 'follower'])
		res_time_line = []
		res_follower_line = []
		current_follower = 0
		time_line_iter_index = 0
		for time_index in range(time_line.iloc[-1] + 1):
			if time_index >= time_line[time_line_iter_index]:
				'time to update the follower value'
				current_follower = follower_line[time_line_iter_index]
				time_line_iter_index += 1
			res_time_line.append(time_index)
			res_follower_line.append(current_follower)

		'Done!, build a new dataframe here, and show the data'
		df = pd.DataFrame(list(zip(res_time_line, res_follower_line)),
		                  columns=['time', 'follower'])
		# df.plot(x='time', y='follower')
		# plt.title('origin data')
		# plt.show()
		return df, origin_dataframe

if __name__ == '__main__':
	'read in csv'
	dp = data_preprocessor()
	dp.read_in_csv('kizuna.csv')
	processed_dataframe = dp.preprocess()