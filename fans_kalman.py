from data_preprosessor import data_preprocessor
from kalman_filter import KalmanFilter
import numpy as np
import matplotlib.pyplot as plt
import pdb
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

class fans_kalman(object):
	def __init__(self, initial_x0, sigma_w, sigma_v):
		self.sigma_w = sigma_w
		self.sigma_v = sigma_v
		self.define_kalman_parameters(initial_x0)
		self.define_kalman_filter()

	def define_kalman_parameters(self, initial_x0):
		'initialize the parameters of kalman filter here'
		dt = 1
		self.F = np.array([[1, dt],
		                   [0, 1]])

		self.H = np.array([1, 0]).reshape(1, 2)

		self.Q = np.array([[self.sigma_w, 0.0],
		                   [0.0, self.sigma_w]])

		self.R = np.array([self.sigma_v]).reshape(1, 1)

		self.P = np.array([[10., 0],
							[0, 10.]])

		'Notice that, the inital_x0 here actually is a state, which is a 2-d array'
		self.initial_x0 = np.array([[initial_x0],
							[0]])

	def define_kalman_filter(self):
		self.kf = KalmanFilter(F=self.F, H=self.H, Q=self.Q, R=self.R, P=self.P, x0=self.initial_x0)

	def predict_interface(self, new_measurement):
		'predict the value, and update the kalman filter'
		if new_measurement is not None:
			self.kf.update(new_measurement)
		'Otherwise, skip the measurement-update step...just perform the time-update'
		res = np.dot(self.H, self.kf.predict())[0]
		return res

def grid_search_interface(sigma_w, sigma_v, origin_data):
	'an interface for parameter grid search'
	pred_res = []
	input_data = origin_data['follower'].tolist()
	time_line = origin_data['time'].tolist()
	kalman_filter = fans_kalman(input_data[0], sigma_w = sigma_w, sigma_v = sigma_v)

	for time_index in range(time_line[-1]):
		new_obtained_value = None
		if time_index in time_line:
			'has new value here'
			new_obtained_value = input_data[time_line.index(time_index)]
		pred_res.append(kalman_filter.predict_interface(new_obtained_value))

	'simply turn the pred_res to an array'
	prediction_array = np.squeeze(np.asarray(pred_res))
	'At each origin time_step, see the predict difference, and get the absolute mean'
	'Notice that we want the prediction difference when there is [real] input occur'
	diff_list = []
	for (dataline_index, time_line_index) in enumerate(time_line):
		'at this time step, what is the abs diff?'
		# print(f"index:{dataline_index}, time_line:{time_line_index}")
		'Let us skip the first input, since we are unable to predict the initial value'
		if time_line_index == 0:
			continue
		diff = abs(prediction_array[time_line_index - 1] - input_data[dataline_index])
		diff_list.append(diff)
	mean_diff = np.mean(diff_list)

	return mean_diff

if __name__ == '__main__':
	dp = data_preprocessor()
	# dp.read_in_csv('kizuna.csv')
	dp.read_in_csv('mea.csv')
	origin_data = dp.preprocess()

	pred_res = []
	input_data = origin_data['follower'].tolist()
	time_line = origin_data['time'].tolist()
	'The following two parameter values is obtained from grid search'
	optimal_sigma_w = 0.5
	optimal_sigma_v = 0.2223
	'We need to provide the inital x0 value here'
	kalman_filter = fans_kalman(input_data[0], sigma_w=optimal_sigma_w, sigma_v=optimal_sigma_v)

	for time_index in range(time_line[-1]):
		new_obtained_value = None
		if time_index in time_line:
			'has new value here'
			new_obtained_value = input_data[time_line.index(time_index)]
		pred_res.append(kalman_filter.predict_interface(new_obtained_value))

	'simply turn the pred_res to an array'
	prediction_array = np.squeeze(np.asarray(pred_res))
	'At each origin time_step, see the predict difference, and get the absolute mean'
	diff_list = []
	pred_compare_list = []
	for (dataline_index, time_line_index) in enumerate(time_line):
		'at this time step, what is the abs diff?'
		# print(f"index:{dataline_index}, time_line:{time_line_index}")
		'Let us skip the first input, since we are unable to predict the initial value'
		if time_line_index == 0:
			pred_compare_list.append(input_data[0])
			continue
		diff = abs(prediction_array[time_line_index-1] - input_data[dataline_index])
		diff_list.append(diff)
		pred_compare_list.append(prediction_array[time_line_index-1])
	mean_diff = np.mean(diff_list)
	'plot using a magnifier'
	fig, ax = plt.subplots()
	ax.plot(time_line, input_data, '--ro', label='Follower Measurements')
	ax.plot(time_line, pred_compare_list, '--co', label='Kalman Filter Prediction')
	plt.xlabel('time')
	plt.title(f'mean prediction error: {mean_diff}')

	axins = zoomed_inset_axes(ax, 50, loc=2)  # zoom-factor: 2.5, location: upper-left
	axins.plot(time_line, input_data, '--ro', label='Follower Measurements')
	axins.plot(time_line, pred_compare_list, '--co', label='Kalman Filter Prediction')

	legend = axins.legend(loc='best', shadow=True, fontsize='small')
	legend.get_frame().set_facecolor('w')

	# x1, x2, y1, y2 = 32700, 32800, 998300, 999000  # specify the limits
	x1, x2, y1, y2 = 19600, 20200, 370200, 371600  # specify the limits
	axins.set_xlim(x1, x2)  # apply the x-limits
	axins.set_ylim(y1, y2)  # apply the y-limits

	plt.yticks(visible=False)
	plt.xticks(visible=False)

	mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")
	plt.show()