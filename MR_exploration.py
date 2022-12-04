from robot_class import *
import random
import math
from collections import defaultdict

# Vishnu Add here
# For now only, minmax of ellipsoids
xmin1, xmin2 = 5, 5
xmax1, xmax2 = 10, 10
ymin1, ymin2 = 5, 90
ymax1, ymax2 = 10, 95

minmaxrbt1 = [[xmin1, ymin1], [xmin1, ymax1], [xmax1, ymin1], [xmax1, ymax1]]
minmaxrbt2 = [[xmin2, ymin2], [xmin2, ymax2], [xmax2, ymin2], [xmax2, ymax2]]
minmax = [minmaxrbt1, minmaxrbt2]

################################

# Functions
# Initializations of robots
def multiple_robots(no_of_robots):
    list1 = []  
    for i in range(no_of_robots):
        rbt = init_robot()
        list1.append(rbt)
    return list1 
    
def init_robot():
    x = 10
    y = random.randint(5,85)
    rbt = robot([x,y],1,1)
    rbt.get_sensor_readings_and_update()
    return rbt

# Explorations - levy walk with modifications. More comments in main section of code
# Three different implementations:
    # 1. Selects random point on frontier
    # 2. Selects random point on frontier which is close to current position
    # 3. Selects random point on frontier which is far to current position.
        # This is implemented by choosing points that are at a distance greater than x (on frontier) from robots current positions
        # The distance of these points are found from the min and max (on x-axis and y-axis) of ellipsoid (is the map for explored area of other robots)
max_counter = 100
def explore_frontier_random(rbt):
    return random_index(rbt)

def explore_frontier_far(rbt, allrobots, minmax):
    listofindexforpoints = list()
    numberofpoints = 5
    costlist = defaultdict()
        
    for _ in range(numberofpoints):
        counter = 0
        check = True
        while check:
            x = random_index(rbt)
            distance = euc_dist(rbt, x)
            if distance >= 25:
                listofindexforpoints.append(x)
                check = False
            counter += 1
            if counter >= max_counter:
                listofindexforpoints.append(explore_frontier_random(rbt)) 
                check = False

    print("(listofindexforpoints):" ,listofindexforpoints)
    print("listofindexforpoints[0]:" ,listofindexforpoints[0])
    for i, val in enumerate(allrobots):
        if val == rbt:
            continue
        else:
            for r in range(numberofpoints):
                minlist = list()
                minlistpointindex = list()

                for j in range(4):
                    minlist.append(euc_dist(val, x=listofindexforpoints[r] , minmax=minmax[i][j]))
                    minlistpointindex.append(listofindexforpoints[r])
                
                min_in_minlist = min(minlist)
                costlist[min_in_minlist] = minlistpointindex[minlist.index(min_in_minlist)]
                
            print("costlist", costlist)
            
            maxdistancevalue = max(costlist.keys())
            print(costlist[maxdistancevalue])
            return costlist[maxdistancevalue]

def explore_frontier_closeby(rbt):
    counter = 0
    while True:
        x = random_index(rbt)
        distance = euc_dist(rbt, x)
        if distance <= 7:
            print("Max counter NOT triggered")
            return x
        counter += 1
        if counter >= max_counter:
            print("Max counter triggered")
            return explore_frontier_random(rbt)

# Returns random index from the list of frontiers
def random_index(rbt):
    return random.randint(0, len(rbt.map.frontiers)-1)

# Euclidean distance
def euc_dist(rbt1, x=None, rbt2=None, minmax=None):
    if rbt2 is None and minmax is None:
        return math.sqrt(((rbt1.map.frontiers[x][0] - rbt1.cur_pos[0]) ** 2 ) + ((rbt1.map.frontiers[x][1] - rbt1.cur_pos[1]) ** 2 ))
    elif minmax is not None:
        return math.sqrt(((rbt1.map.frontiers[x][0] - minmax[0]) ** 2 ) + ((rbt1.map.frontiers[x][1] - minmax[1]) ** 2 ))
    else:
        ################# Yet to be implemented
        print("THIS FUNC IS NOT COMPLETE")
        return False

# Robot actions
def move_to_goal(rbt, x):
    copy = rbt
    rbt.update_goal(rbt.map.frontiers[x])
    rbt.find_path_to_goal(True)
    try:
        rbt.drive_along_path()
        rbt.get_sensor_readings_and_update()
    except Exception:
        rbt = copy
    return True

########################################
################# MAIN #################
########################################

# Initializing number of robots
robots = multiple_robots(2)

# # First movement of robots
for _ in range(2):
    for r in range(len(robots)):
        move_to_goal(robots[r], explore_frontier_random(robots[r]))

# # Exploration 
i, p = 0, 0
while i < 100:
    for r in range(len(robots)):
        if p == 0:
            # move_to_goal(robots[r], explore_frontier_far(robots[r]))   
            try:
                move_to_goal(robots[r], explore_frontier_far(robots[r], robots, minmax))   
            except Exception:
                continue
            print("Long walk")
        else:
            move_to_goal(robots[r], explore_frontier_closeby(robots[r]))
        i += 1
        
        # condition for fast wider exploration in the beginning
        if i > 10:
            p = random.randint(0,2)
        else:
            p = random.randint(0,1)

# Displaying explored areas
for r in range(len(robots)):
    plt.subplot(1,2,r+1) 
    robots[r].map.display_robot_map()
plt.show()