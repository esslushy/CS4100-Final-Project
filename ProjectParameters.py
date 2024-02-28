# Agent Parameters
AGGRESSIVE_BOUNDS = (0, 1)
HARVEST_BOUNDS = (0, 1)
MEMORY_BOUNDS = (0, 20)
INTERACTION_RADIUS = 1
VISION_RADIUS = 6
DISTANCE_PER_STEP = 0.5
CHANCE_TO_REMEMBER_BUSH = 0.3
CHANCE_TO_REMEMBER_CAVE = 0.7
CHANCE_TO_USE_MEMORY = 0.1
CHANCE_TO_GET_BORED = 0.05
FAT_PRESERVATION_PERCENT = 0.5
# Calorie parameters
MAX_AGGR_CAL = 200
MAX_HARVEST_CAL = 100
CAL_PER_MEM = 50
# Initialization
INIT_NUM_AGENTS = 150 # Number of agents could change
INIT_NUM_CAVES = 75
INIT_CAVE_CAP = (3, 7) 
INIT_NUM_BUSHES = 100
INIT_BUSH_CAP = (400, 800) 
MAP_SIZE = 50 # Square
# How long to run
NUM_DAYS = 100
STEPS_PER_DAY = 250
# How much of the day to consider morning and evening.
MORNING_PERCENT = 0.15
EVENING_PERCENT = 0.15
# Checkpointing
DAYS_PER_CHECKPOINT = 5
# Visualization
VISUALIZE = True
NUM_BINS = 25