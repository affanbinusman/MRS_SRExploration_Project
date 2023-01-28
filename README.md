This video link is the simulation demonstration of the project for the Multi-Robot Systems class at Arizona State University. 

The highlights of the project include: 
- Worked in a team of 2 to create a decentralized multi-robot system simulation of exploration and mapping for search and rescue of a target object using Python (Matplotlib, SciPy, PyLab, NumPy)
- Adopted non-linear Model Predictive Controller, RRT*, PID controller, and potential gradient obstacle avoidance algorithm for motion planning; and combination of Levy walk and Brownian motion for exploration with 97% object finding accuracy
- Analyzed local and global map coverage, and object identification statistics by varying exploration parameters; found the target object (100% accuracy) with a modified exploration algorithm

---

# MRS

In master branch : Run the exploration_mrs.py file to run the explorations. Different settings are possible by changing parameters in global_map(for obstacles and features to detect).


In working branch: simulation.py  file will execute the robot motion simultaneously. "nmpc" flag needs to be set to use mpc based navigation.
