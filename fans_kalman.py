from data_preprosessor import data_preprocessor
from kalman_filter import KalmanFilter
import numpy as np
import matplotlib.pyplot as plt
import pdb

class fans_kalman(object):
	def __init__(self, initial_x0, sigma_w, sigma_v):
		self.sigma_w = sigma_w
		self.sigma_v = sigma_v
		self.define_kalman_parameters(initial_x0)
		self.define_kalman_filter()

	def define_kalman_parameters(self, initial_x0):
		dt = 1
		self.F = np.array([[1, dt],
		                   [0, 1]])

		self.H = np.array([1, 0]).reshape(1, 2)

		self.Q = np.array([[self.sigma_w, 0.0],
		                   [0.0, self.sigma_w]])

		self.R = np.array([self.sigma_v*self.sigma_v]).reshape(1, 1)

		self.P = np.array([[10., 0],
							[0, 10.]])

		'Notice that, the inital_x0 here actually is a state, which is a 2-d array'
		self.initial_x0 = np.array([[initial_x0],
							[0]])

	def define_kalman_filter(self):
		self.kf = KalmanFilter(F=self.F, H=self.H, Q=self.Q, R=self.R, P=self.P, x0=self.initial_x0)

	def predict_interface(self, new_measurement):
		res = np.dot(self.H, self.kf.predict())[0]
		self.kf.update(new_measurement)
		return res

def grid_search_interface(sigma_w, sigma_v, processed_dataframe):
	'an interface for parameter grid search'
	pred_res = []
	input_data = processed_dataframe['follower']

	kalman_filter = fans_kalman(input_data[0], sigma_w = sigma_w, sigma_v = sigma_v)

	for data in input_data:
		pred_res.append(kalman_filter.predict_interface(data))
	'simply turn the pred_res to an array'
	prediction_array = np.squeeze(np.asarray(pred_res))
	mean_diff = np.mean(np.abs(input_data - prediction_array))
	return mean_diff

if __name__ == '__main__':
	dp = data_preprocessor()
	dp.read_in_csv('kizuna.csv')
	processed_dataframe = dp.preprocess()

	pred_res = []
	input_data = processed_dataframe['follower']

	optimal_sigma_w = 0.16334897959183672
	optimal_sigma_v = 0.7347204081632653
	kalman_filter = fans_kalman(input_data[0], sigma_w=optimal_sigma_w, sigma_v=optimal_sigma_v)

	for data in input_data:
		pred_res.append(kalman_filter.predict_interface(data))

	'simply turn the pred_res to an array'
	prediction_array = np.squeeze(np.asarray(pred_res))
	mean_diff = np.mean(np.abs(input_data - prediction_array))
	'also, calculate the l2 distance'
	plt.plot(input_data, c='r', label='Follower Measurements')
	plt.plot(prediction_array, c='c', label='Kalman Filter Prediction')
	plt.legend()
	plt.title(f'mean_dist: {mean_diff}')
	plt.show()