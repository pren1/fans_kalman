import sys
from fans_kalman import fans_kalman

sigma_w = 0.5
sigma_v = 0.2223

kalman_filter = None
lastNum = None
for line in sys.stdin:
    try:
        num = int(line)
    except Exception:
        'None data'
        if lastNum != None:
            'predict with None input'
            print(lastNum, flush=True)
            lastNum = kalman_filter.predict_interface(None)[0]
    else:
        'Has data'
        if kalman_filter == None:
            'create kalman filter'
            kalman_filter = fans_kalman(num, sigma_w=sigma_w, sigma_v=sigma_v)
        else:
            'predict with input'
            lastNum = kalman_filter.predict_interface(num)[0]
