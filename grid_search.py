import pdb
from fans_kalman import grid_search_interface
import tqdm
import numpy as np
from data_preprosessor import data_preprocessor

class grid_search(object):
	def __init__(self):
		self.sigma_w_grid = np.linspace(0.0001, 1.0, num=50)
		self.sigma_v_grid = np.linspace(0.0001, 1.0, num=50)

		dp = data_preprocessor()
		dp.read_in_csv('kizuna.csv')
		self.processed_dataframe = dp.preprocess()

	def run_grid_search(self):
		minimum_error = np.Inf
		saved_sigma_w = -1
		saved_sigma_v = -1
		for sigma_w in tqdm.tqdm(self.sigma_w_grid):
			for sigma_v in tqdm.tqdm(self.sigma_v_grid):
				val = grid_search_interface(sigma_w=sigma_w, sigma_v=sigma_v, processed_dataframe=self.processed_dataframe)
				if minimum_error > val:
					minimum_error = val
					saved_sigma_w = sigma_w
					saved_sigma_v = sigma_v
		print(f"optimized parameter sets: sigma_w: {saved_sigma_w}, sigma_v: {saved_sigma_v}, gives mean error: {minimum_error}")

if __name__ == '__main__':
	gs = grid_search()
	gs.run_grid_search()