from data_preprosessor import data_preprocessor
from kalman_filter import KalmanFilter
import numpy as np
import matplotlib.pyplot as plt
import pdb

class fans_kalman(object):
	def __init__(self, initial_x0):
		self.define_kalman_parameters(initial_x0)
		self.define_kalman_filter()

	def define_kalman_parameters(self, initial_x0):
		dt = 1
		sigma_w = 0.05
		sigma_v = 0.05

		self.F = np.array([[1, dt],
		                   [0, 1]])

		self.H = np.array([1, 0]).reshape(1, 2)

		self.Q = np.array([[sigma_w, 0.0],
		                   [0.0, sigma_w]])

		self.R = np.array([sigma_v*sigma_v]).reshape(1, 1)

		self.P = np.array([[100., 0],
							[0, 100.]])

		'Notice that, the inital_x0 here actually is a state, which is a 2-d array'
		self.initial_x0 = np.array([[initial_x0],
							[0]])

	def define_kalman_filter(self):
		self.kf = KalmanFilter(F=self.F, H=self.H, Q=self.Q, R=self.R, P=self.P, x0=self.initial_x0)

	def predict_interface(self, new_measurement):
		res = np.dot(self.H, self.kf.predict())[0]
		self.kf.update(new_measurement)
		return res

if __name__ == '__main__':
	dp = data_preprocessor()
	dp.read_in_csv('kizuna.csv')
	processed_dataframe = dp.preprocess()

	pred_res = []
	input_data = processed_dataframe['follower']

	kalman_filter = fans_kalman(input_data[0])

	for data in input_data:
		pred_res.append(kalman_filter.predict_interface(data))

	'also, calculate the l2 distance'
	plt.plot(np.asarray(input_data), c='r', label='follower Measurements')
	plt.plot(np.asarray(pred_res), c='c', label='Kalman Filter Prediction')
	plt.legend()
	# plt.title(f'mean_dist: {mean_dist}')
	plt.show()

