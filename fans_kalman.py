from data_preprosessor import data_preprocessor
from kalman_filter import KalmanFilter
import numpy as np
import matplotlib.pyplot as plt
import pdb

class fans_kalman(object):
	def __init__(self):
		self.define_kalman_parameters()
		self.define_kalman_filter()

	def define_kalman_parameters(self):
		dt = 1
		self.F = np.array([[1, dt, 0], [0, 1, dt], [0, 0, 1]])
		self.H = np.array([1, 0, 0]).reshape(1, 3)
		self.Q = np.array([[0.05, 0.05, 0.0], [0.05, 0.05, 0.0], [0.0, 0.0, 0.0]])
		self.R = np.array([0.5]).reshape(1, 1)

	def define_kalman_filter(self):
		self.kf = KalmanFilter(F=self.F, H=self.H, Q=self.Q, R=self.R)

	def predict_interface(self, new_measurement):
		res = np.dot(self.H, self.kf.predict())[0]
		self.kf.update(new_measurement)
		return res

if __name__ == '__main__':
	dp = data_preprocessor()
	dp.read_in_csv('kizuna.csv')
	processed_dataframe = dp.preprocess()
	kalman_filter = fans_kalman()

	pred_res = []
	input_data = processed_dataframe['follower']
	for data in input_data:
		pred_res.append(kalman_filter.predict_interface(data))
	plt.plot(np.asarray(input_data)[1000:], c='r', label='follower Measurements')
	plt.plot(np.asarray(pred_res)[1000:], c='c', label='Kalman Filter Prediction')
	plt.legend()
	plt.show()
