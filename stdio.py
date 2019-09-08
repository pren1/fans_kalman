import sys
from fans_kalman import fans_kalman

sigma_w = 0.5
sigma_v = 0.2223

kalman_filter = None

for line in sys.stdin:
  try:
    num = int(line)
  except Exception:
    if kalman_filter != None:
      print(kalman_filter.predict_interface(None)[0], flush=True)
  else:
    if kalman_filter == None:
      kalman_filter = fans_kalman(num, sigma_w=sigma_w, sigma_v=sigma_v)
    else:
      print(kalman_filter.predict_interface(num)[0], flush=True)
