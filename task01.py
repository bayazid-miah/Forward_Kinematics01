{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "0",
   "metadata": {
    "jupyter": {
     "source_hidden": true
    }
   },
   "source": [
    "# Task 1: Basics - loading data, visualization, segmentation, filtering"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "1",
   "metadata": {},
   "source": [
    "## 1.1 Loading data and filtering it"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "2",
   "metadata": {},
   "source": [
    "The processing order for optical motion capture data is usually as follows:\n",
    "1. Record OMC data (marker trajectories) + force plate data (ground reaction forces)\n",
    "2. Label markers and fill gaps in the marker trajectories (already done for you)\n",
    "3. Scale musculoskeletal model to the subject (more info [here](https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53089741/Tutorial+3+-+Scaling+Inverse+Kinematics+and+Inverse+Dynamics))\n",
    "4. Inverse kinematics: calculate joint angles from marker trajectories\n",
    "5. Filter marker trajectories and joint angles -- to remove high-frequency noise. Always filter whole trajectories, not only segments ()\n",
    "6. Inverse dynamics: calculate joint moments from joint angles and ground reaction forces"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "3",
   "metadata": {},
   "source": [
    "**To Do:**\n",
    "\n",
    "Go to filter.py and implement a 4th zero-lag Butterworth low-pass filter with a cutoff frequency of 6 Hz. You can use the scipy functions `scipy.signal.butter` and `scipy.signal.filtfilt` for this.\n",
    "\n",
    "Then run the next cell to visualize the effect of filtering on the marker trajectories. You should see that high-frequency noise is removed, but the overall shape of the signal is preserved."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "4",
   "metadata": {},
   "outputs": [
    {
     "ename": "AttributeError",
     "evalue": "type object 'filter' has no attribute 'butterworth_lowpass_filter'",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mAttributeError\u001b[0m                            Traceback (most recent call last)",
      "Cell \u001b[0;32mIn[8], line 19\u001b[0m\n\u001b[1;32m     16\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mmatplotlib\u001b[39;00m\u001b[38;5;21;01m.\u001b[39;00m\u001b[38;5;21;01mpyplot\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mas\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mplt\u001b[39;00m\n\u001b[1;32m     18\u001b[0m grf_data \u001b[38;5;241m=\u001b[39m load_data\u001b[38;5;241m.\u001b[39mload_grf_data()\n\u001b[0;32m---> 19\u001b[0m filtered_grf_data \u001b[38;5;241m=\u001b[39m \u001b[38;5;28mfilter\u001b[39m\u001b[38;5;241m.\u001b[39mbutterworth_lowpass_filter(grf_data, cutoff\u001b[38;5;241m=\u001b[39m\u001b[38;5;241m6\u001b[39m, fs\u001b[38;5;241m=\u001b[39m\u001b[38;5;241m100\u001b[39m, order\u001b[38;5;241m=\u001b[39m\u001b[38;5;241m4\u001b[39m)\n\u001b[1;32m     21\u001b[0m range_ \u001b[38;5;241m=\u001b[39m \u001b[38;5;28mslice\u001b[39m(\u001b[38;5;241m1000\u001b[39m, \u001b[38;5;241m1200\u001b[39m)\n\u001b[1;32m     22\u001b[0m plt\u001b[38;5;241m.\u001b[39mplot(grf_data[\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mtime\u001b[39m\u001b[38;5;124m'\u001b[39m][range_], grf_data[\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mground_force_vy\u001b[39m\u001b[38;5;124m'\u001b[39m][range_], label\u001b[38;5;241m=\u001b[39m\u001b[38;5;124m'\u001b[39m\u001b[38;5;124munfiltered\u001b[39m\u001b[38;5;124m'\u001b[39m)\n",
      "\u001b[0;31mAttributeError\u001b[0m: type object 'filter' has no attribute 'butterworth_lowpass_filter'"
     ]
    }
   ],
   "source": [
    "\"\"\"from utils import filter, load_data\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "grf_data = load_data.load_grf_data()\n",
    "# This filter needs to be implemented by you in utils/filter.py first!\n",
    "filtered_grf_data = filter.butterworth_lowpass_filter(grf_data, cutoff=6, fs=100, order=4)\n",
    "range = slice(1000, 1200)\n",
    "plt.plot(grf_data['time'][range], grf_data['ground_force_vy'][range], label='unfiltered')\n",
    "plt.plot(filtered_grf_data['time'][range], filtered_grf_data['ground_force_vy'][range], label='filtered')\n",
    "plt.xlabel('time (s)')\n",
    "plt.ylabel('ground force vertical (N)')\n",
    "plt.legend()\"\"\"\n",
    "\n",
    "\n",
    "from utils import load_data\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "grf_data = load_data.load_grf_data()\n",
    "filtered_grf_data = filter.butterworth_lowpass_filter(grf_data, cutoff=6, fs=100, order=4)\n",
    "\n",
    "range_ = slice(1000, 1200)\n",
    "plt.plot(grf_data['time'][range_], grf_data['ground_force_vy'][range_], label='unfiltered')\n",
    "plt.plot(filtered_grf_data['time'][range_], filtered_grf_data['ground_force_vy'][range_], label='filtered')\n",
    "plt.xlabel('time (s)')\n",
    "plt.ylabel('ground force vertical (N)')\n",
    "plt.legend()\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "5",
   "metadata": {},
   "source": [
    "Run `pytest tests.py` to check if the first part of your implementation is correct - 2 tests should pass now."
   ]
  },
  {
   "cell_type": "markdown",
   "id": "6",
   "metadata": {},
   "source": [
    "## 1.2 Segmenting gait cycles\n",
    "We can use the vertical ground reaction force (GRF) to identify heel strikes and toe offs. A common threshold is 20 N: if the vertical GRF exceeds this value, the foot is on the ground. Always use the unfiltered GRF data for this.\n",
    "\n",
    "Next cell plots the points we roughly search for:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "7",
   "metadata": {},
   "outputs": [
    {
     "ename": "TypeError",
     "evalue": "'Series' object cannot be interpreted as an integer",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mTypeError\u001b[0m                                 Traceback (most recent call last)",
      "Cell \u001b[0;32mIn[9], line 1\u001b[0m\n\u001b[0;32m----> 1\u001b[0m plt\u001b[38;5;241m.\u001b[39mplot(grf_data[\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mtime\u001b[39m\u001b[38;5;124m'\u001b[39m][\u001b[38;5;28mrange\u001b[39m], grf_data[\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mground_force_vy\u001b[39m\u001b[38;5;124m'\u001b[39m][\u001b[38;5;28mrange\u001b[39m], label\u001b[38;5;241m=\u001b[39m\u001b[38;5;124m'\u001b[39m\u001b[38;5;124munfiltered\u001b[39m\u001b[38;5;124m'\u001b[39m)\n\u001b[1;32m      2\u001b[0m plt\u001b[38;5;241m.\u001b[39mplot(\u001b[38;5;241m10.08\u001b[39m, \u001b[38;5;241m0\u001b[39m, \u001b[38;5;124m'\u001b[39m\u001b[38;5;124mro\u001b[39m\u001b[38;5;124m'\u001b[39m)  \u001b[38;5;66;03m# heel strike 1\u001b[39;00m\n\u001b[1;32m      3\u001b[0m plt\u001b[38;5;241m.\u001b[39mplot(\u001b[38;5;241m11.03\u001b[39m, \u001b[38;5;241m0\u001b[39m, \u001b[38;5;124m'\u001b[39m\u001b[38;5;124mro\u001b[39m\u001b[38;5;124m'\u001b[39m)\n",
      "File \u001b[0;32m/opt/anaconda3/lib/python3.13/site-packages/pandas/core/series.py:1097\u001b[0m, in \u001b[0;36mSeries.__getitem__\u001b[0;34m(self, key)\u001b[0m\n\u001b[1;32m   1095\u001b[0m \u001b[38;5;28;01mdef\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21m__getitem__\u001b[39m(\u001b[38;5;28mself\u001b[39m, key):\n\u001b[1;32m   1096\u001b[0m     check_dict_or_set_indexers(key)\n\u001b[0;32m-> 1097\u001b[0m     key \u001b[38;5;241m=\u001b[39m com\u001b[38;5;241m.\u001b[39mapply_if_callable(key, \u001b[38;5;28mself\u001b[39m)\n\u001b[1;32m   1099\u001b[0m     \u001b[38;5;28;01mif\u001b[39;00m key \u001b[38;5;129;01mis\u001b[39;00m \u001b[38;5;28mEllipsis\u001b[39m:\n\u001b[1;32m   1100\u001b[0m         \u001b[38;5;28;01mif\u001b[39;00m using_copy_on_write() \u001b[38;5;129;01mor\u001b[39;00m warn_copy_on_write():\n",
      "File \u001b[0;32m/opt/anaconda3/lib/python3.13/site-packages/pandas/core/common.py:384\u001b[0m, in \u001b[0;36mapply_if_callable\u001b[0;34m(maybe_callable, obj, **kwargs)\u001b[0m\n\u001b[1;32m    373\u001b[0m \u001b[38;5;250m\u001b[39m\u001b[38;5;124;03m\"\"\"\u001b[39;00m\n\u001b[1;32m    374\u001b[0m \u001b[38;5;124;03mEvaluate possibly callable input using obj and kwargs if it is callable,\u001b[39;00m\n\u001b[1;32m    375\u001b[0m \u001b[38;5;124;03motherwise return as it is.\u001b[39;00m\n\u001b[0;32m   (...)\u001b[0m\n\u001b[1;32m    381\u001b[0m \u001b[38;5;124;03m**kwargs\u001b[39;00m\n\u001b[1;32m    382\u001b[0m \u001b[38;5;124;03m\"\"\"\u001b[39;00m\n\u001b[1;32m    383\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;28mcallable\u001b[39m(maybe_callable):\n\u001b[0;32m--> 384\u001b[0m     \u001b[38;5;28;01mreturn\u001b[39;00m maybe_callable(obj, \u001b[38;5;241m*\u001b[39m\u001b[38;5;241m*\u001b[39mkwargs)\n\u001b[1;32m    386\u001b[0m \u001b[38;5;28;01mreturn\u001b[39;00m maybe_callable\n",
      "\u001b[0;31mTypeError\u001b[0m: 'Series' object cannot be interpreted as an integer"
     ]
    }
   ],
   "source": [
    "plt.plot(grf_data['time'][range], grf_data['ground_force_vy'][range], label='unfiltered')\n",
    "plt.plot(10.08, 0, 'ro')  # heel strike 1\n",
    "plt.plot(11.03, 0, 'ro')  # heel strike 2"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "8",
   "metadata": {},
   "source": [
    "**To Do:**\n",
    "\n",
    "Now, implement the function `segment_gait_cycles` in `utils/segment.py` that segments the data into individual gait cycles based on heel strikes. Use a threshold of 60 N on the unfiltered vertical ground reaction force to identify heel strikes. The function should also clean the data: remove gait cycles that do not reach a minimum force of 300 N (to remove partial steps, noise outliers, etc.). Then, remove all gait cycles that are +- 2 standard deviations away from the mean gait cycle duration (to remove outliers). The function should return a list of data frames, each containing one gait cycle. \n",
    "\n",
    "Then execute the next cell to see all gait cycles overlaid. Do you see a clear pattern as in the lecture slides?"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "9",
   "metadata": {},
   "outputs": [
    {
     "ename": "TypeError",
     "evalue": "'NoneType' object is not iterable",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mTypeError\u001b[0m                                 Traceback (most recent call last)",
      "Cell \u001b[0;32mIn[10], line 3\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21;01mutils\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;28;01mimport\u001b[39;00m segment\n\u001b[1;32m      2\u001b[0m gait_cycles \u001b[38;5;241m=\u001b[39m segment\u001b[38;5;241m.\u001b[39msegment_gait_cycles(grf_data\u001b[38;5;241m.\u001b[39mground_force_vy, data\u001b[38;5;241m=\u001b[39mgrf_data, threshold\u001b[38;5;241m=\u001b[39m\u001b[38;5;241m60\u001b[39m)\n\u001b[0;32m----> 3\u001b[0m \u001b[38;5;28;01mfor\u001b[39;00m i, cycle \u001b[38;5;129;01min\u001b[39;00m \u001b[38;5;28menumerate\u001b[39m(gait_cycles):\n\u001b[1;32m      4\u001b[0m     plt\u001b[38;5;241m.\u001b[39mplot(cycle[\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mtime\u001b[39m\u001b[38;5;124m'\u001b[39m], cycle[\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mground_force_vy\u001b[39m\u001b[38;5;124m'\u001b[39m])\n\u001b[1;32m      5\u001b[0m plt\u001b[38;5;241m.\u001b[39mxlabel(\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mtime (s)\u001b[39m\u001b[38;5;124m'\u001b[39m)\n",
      "\u001b[0;31mTypeError\u001b[0m: 'NoneType' object is not iterable"
     ]
    }
   ],
   "source": [
    "from utils import segment\n",
    "gait_cycles = segment.segment_gait_cycles(grf_data.ground_force_vy, data=grf_data, threshold=60)\n",
    "for i, cycle in enumerate(gait_cycles):\n",
    "    plt.plot(cycle['time'], cycle['ground_force_vy'])\n",
    "plt.xlabel('time (s)')\n",
    "plt.ylabel('ground force vertical (N)')\n",
    "plt.legend()\n",
    "print(f'Number of gait cycles remaining: {len(gait_cycles)}')"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "10",
   "metadata": {},
   "source": [
    "## 1.3 Ensemble averaging gait cycles\n",
    "\n",
    "**To Do:**\n",
    "\n",
    "Implement a function `ensemble_average` in `utils/segment.py` that takes a list of data frames (gait cycles) and returns the ensemble average and standard deviation. The function should first resample each gait cycle to 100 data points (using linear interpolation), then calculate the mean and standard deviation across all cycles.\n",
    "\n",
    "Then execute the next cell to visualize the ensemble average and standard deviation of the vertical ground reaction force across all gait cycles. You should see a smooth curve representing the average GRF pattern during walking, with shaded areas indicating variability across cycles.\n",
    "\n",
    "This should look like the plots in the lecture slides."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "11",
   "metadata": {},
   "outputs": [
    {
     "ename": "TypeError",
     "evalue": "object of type 'NoneType' has no len()",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mTypeError\u001b[0m                                 Traceback (most recent call last)",
      "Cell \u001b[0;32mIn[7], line 1\u001b[0m\n\u001b[0;32m----> 1\u001b[0m ensemble_average, ensemble_std \u001b[38;5;241m=\u001b[39m segment\u001b[38;5;241m.\u001b[39mensemble_average(gait_cycles)\n\u001b[1;32m      2\u001b[0m plt\u001b[38;5;241m.\u001b[39mplot(ensemble_average[\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mtime\u001b[39m\u001b[38;5;124m'\u001b[39m], ensemble_average[\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mground_force_vy\u001b[39m\u001b[38;5;124m'\u001b[39m], label\u001b[38;5;241m=\u001b[39m\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mensemble average\u001b[39m\u001b[38;5;124m'\u001b[39m)\n\u001b[1;32m      3\u001b[0m plt\u001b[38;5;241m.\u001b[39mfill_between(ensemble_average[\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mtime\u001b[39m\u001b[38;5;124m'\u001b[39m], \n\u001b[1;32m      4\u001b[0m                  ensemble_average[\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mground_force_vy\u001b[39m\u001b[38;5;124m'\u001b[39m] \u001b[38;5;241m-\u001b[39m ensemble_std[\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mground_force_vy\u001b[39m\u001b[38;5;124m'\u001b[39m],\n\u001b[1;32m      5\u001b[0m                  ensemble_average[\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mground_force_vy\u001b[39m\u001b[38;5;124m'\u001b[39m] \u001b[38;5;241m+\u001b[39m ensemble_std[\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mground_force_vy\u001b[39m\u001b[38;5;124m'\u001b[39m],\n\u001b[1;32m      6\u001b[0m                  color\u001b[38;5;241m=\u001b[39m\u001b[38;5;124m'\u001b[39m\u001b[38;5;124mgray\u001b[39m\u001b[38;5;124m'\u001b[39m, alpha\u001b[38;5;241m=\u001b[39m\u001b[38;5;241m0.5\u001b[39m, label\u001b[38;5;241m=\u001b[39m\u001b[38;5;124m'\u001b[39m\u001b[38;5;124m±1 std dev\u001b[39m\u001b[38;5;124m'\u001b[39m)\n",
      "File \u001b[0;32m~/Downloads/Archive/utils/segment.py:29\u001b[0m, in \u001b[0;36mensemble_average\u001b[0;34m(cycles)\u001b[0m\n\u001b[1;32m     19\u001b[0m \u001b[38;5;28;01mdef\u001b[39;00m\u001b[38;5;250m \u001b[39m\u001b[38;5;21mensemble_average\u001b[39m(cycles):\n\u001b[1;32m     20\u001b[0m \u001b[38;5;250m    \u001b[39m\u001b[38;5;124;03m\"\"\"Compute the ensemble average and standard deviation of segmented gait cycles.\u001b[39;00m\n\u001b[1;32m     21\u001b[0m \u001b[38;5;124;03m    \u001b[39;00m\n\u001b[1;32m     22\u001b[0m \u001b[38;5;124;03m    Parameters:\u001b[39;00m\n\u001b[0;32m   (...)\u001b[0m\n\u001b[1;32m     27\u001b[0m \u001b[38;5;124;03m    - std_cycle: pandas DataFrame with the standard deviation across all cycles\u001b[39;00m\n\u001b[1;32m     28\u001b[0m \u001b[38;5;124;03m    \"\"\"\u001b[39;00m\n\u001b[0;32m---> 29\u001b[0m     \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;28mlen\u001b[39m(cycles) \u001b[38;5;241m==\u001b[39m \u001b[38;5;241m0\u001b[39m:\n\u001b[1;32m     30\u001b[0m         \u001b[38;5;28;01mreturn\u001b[39;00m \u001b[38;5;28;01mNone\u001b[39;00m, \u001b[38;5;28;01mNone\u001b[39;00m\n\u001b[1;32m     32\u001b[0m     \u001b[38;5;28;01mpass\u001b[39;00m\n",
      "\u001b[0;31mTypeError\u001b[0m: object of type 'NoneType' has no len()"
     ]
    }
   ],
   "source": [
    "ensemble_average, ensemble_std = segment.ensemble_average(gait_cycles)\n",
    "plt.plot(ensemble_average['time'], ensemble_average['ground_force_vy'], label='ensemble average')\n",
    "plt.fill_between(ensemble_average['time'], \n",
    "                 ensemble_average['ground_force_vy'] - ensemble_std['ground_force_vy'],\n",
    "                 ensemble_average['ground_force_vy'] + ensemble_std['ground_force_vy'],\n",
    "                 color='gray', alpha=0.5, label='±1 std dev')\n",
    "plt.xlabel('time (s)')\n",
    "plt.ylabel('ground force vertical (N)')\n",
    "plt.legend()"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "12",
   "metadata": {},
   "source": [
    "If that all worked, check out the test function again: `pytest tests.py` - 1 more test should pass now!"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "13",
   "metadata": {},
   "source": [
    "## 1.4 To do: Visualize joint angles"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "14",
   "metadata": {},
   "source": [
    "**To Do:**\n",
    "\n",
    "Visualize the following ensemble averages with standard deviations:\n",
    "- Hip flexion/extension\n",
    "- Knee flexion/extension\n",
    "- Ankle dorsiflexion/plantarflexion\n",
    "- Ground reaction force (horizontal and vertical)\n",
    "Make it look nice (labels, legends, etc.) and compare to the plots in the lecture slides. Do they look similar?"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "15",
   "metadata": {},
   "outputs": [],
   "source": [
    "\"\"\"\n",
    "    Plot joint angles here\n",
    "\"\"\"\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "16",
   "metadata": {},
   "source": [
    "Tests running? Plots done? Great! You are done with assignment 1. "
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
