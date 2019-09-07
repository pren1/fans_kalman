# Fans_Kalman
To predict the fans of any vtuber

The kalman impl is inherited and modified from here: https://github.com/zziz/kalman-filter.git

We expect that there is an update of the follower number every 5 minutes. If there isn't, the follower number will remain unchanged, and it will be used as an input. 

Run:

```
python3 fans_kalman.py
```
to see the prediction result.

Run: 

```
python3 grid_search.py
```
to find the two optimized parameters: 
  1. sigma_w: variance of the process noise
  2. sigma_v: variance of the measurement noise

The grid search has been done, and the optimized parameter has been found. The model is trained on the data from kizuna ai, 
and it is tested on the data from mea. Here are the result:

Mean prediction error on the training set (kizuna.csv):

<p>
    <img src="model_picture/kizuna.png"/>
</p>

Mean prediction error on the test set (mea.csv):

<p>
    <img src="model_picture/mea.png"/>
</p>

For more details, please take a look at my code :D

