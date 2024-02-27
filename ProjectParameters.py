# Agent Parameters
AGGRESSIVE_BOUNDS = (0, 1)
HARVEST_BOUNDS = (0, 1)
MEMORY_BOUNDS = (0, 20)
INTERACTION_RADIUS = 0.5
VISION_RAIDUS = 4
DISTANCE_PER_STEP = 0.2
CHANCE_TO_REMEMBER_BUSH = 0.3
CHANCE_TO_REMEMBER_CAVE = 0.7
CHANCE_TO_USE_MEMORY = 0.1
# Calorie parameters
MAX_AGGR_CAL = 200
MAX_HARVEST_CAL = 100
CAL_PER_MEM = 50
# Initialization
INIT_NUM_AGENTS = 100 # Number of agents could change
INIT_NUM_CAVES = 50
INIT_CAVE_CAP = (3, 7) 
INIT_NUM_BUSHES = 150
INIT_BUSH_CAP = (400, 800) 
MAP_SIZE = 200 # Square
# How long to run
NUM_DAYS = 1000
STEPS_PER_DAY = 500
# Checkpointing
DAYS_PER_CHECKPOINT = 25
# Visualization
NUM_BINS = 10