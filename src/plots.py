import matplotlib.pyplot as plt
import numpy as np
import json
import statistics
from pathlib import Path

checkpoints = Path("../checkpoints/")

mean_agg = [] # list of mean aggressiveness values per checkpoint
std_agg = [] # list of std aggressiveness values per checkpoint 

mean_mem = [] # list of mean memory values per checkpoint
std_mem = [] # list of std memory values per checkpoint 

mean_hvst = [] # list of mean harvest values per checkpoint
std_hvst = [] # list of std harvest values per checkpoint 

# with open(checkpoints.joinpath(f"checkpoint_{current_day}.json"), "wt+") as f:

# obtains mean aggressiveness and std aggressivness
def get_agg():
    with open("../checkpoints/checkpoint_0.json", "r") as f:
        data = json.load(f)
        print(np.array(range(100)))

get_agg()
    
# plots the mean aggressiveness with std 
