'''
Naruda: 2019-1 AJOU Univ. major of Software department Capstone project
Robot main firmware made by "Park Jun-Hyuk" (github nickname 'BrightBurningPark').

Robot can drive by itself, localize position and direction in given map.
it can also build the map from zero.

I Love my school and the Capstone Program SO MUCH. it's true story ^^.
'''
# python basic or pip-installed library import
import os
import math
import time
import signal
import threading

# adding ./lib dir to use modules
import sys
sys.path.append('./lib')
# modules under lib directory
import ntdriver         # network driver
import pathengine       # shortest path finding engine
import rpslam           # BreezySLAM(tinySLAM Implementation) with RPLidar A1

# General variables like Path, Var, Name, etc...
PATH_ROBOT = "/home/odroid/capdi/robot" # robot SW top path
PATH_MAP = PATH_ROBOT + "/maps"          # map directory
PATH_LIB = PATH_ROBOT + "/lib"          # libraries
MAP_NAME_NO_SLAM = 'MAP_NO_SLAM.pgm'    # map name generated by no_map_slam
MAP_NAME_YES_SLAM = 'MAP_YES_SLAM.pgm'  # map name pre-drawn
MAP_NAME_PATH_PLANNING = 'MAP_PATH_PLANNING.png' #png map name, for pathplanning

def handler(signum, frame):
    narslam.flag = 1
    t_slam.join()
    sys.exit(-1)

if __name__ == "__main__":
    print ('firmware started')
    narslam = rpslam.narlam()
    t_slam = threading.Thread(target=narslam.slam_no_map, args=(PATH_MAP, MAP_NAME_NO_SLAM, MAP_NAME_PATH_PLANNING))
    t_slam.start()

    nxt = ntdriver.lego_nxt()
    nxt.connect()

    signal.signal(signal.SIGTSTP, handler)

    while True:
        '''
        if not narslam.viz.display(narslam.x/1000, narslam.y/1000, narslam.theta, narslam.mapbytes):
            exit(0)
        '''
        cmd = input('Command>> ')
        if cmd == 'exit':
            narslam.flag = 1
            t_slam.join()
            #os.rename(PATH_MAP+'/'+MAP_NAME_NO_SLAM, PATH_MAP+'/'+MAP_NAME_YES_SLAM)
            print(narslam.x, narslam.y, narslam.theta)
            sys.exit(0)
        nxt.send(cmd)
        print('(', narslam.x/1000, '|', narslam.y, '|', narslam.theta, ')')

        
