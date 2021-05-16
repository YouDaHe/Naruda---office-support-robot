from breezyslam.algorithms import RMHC_SLAM
from breezyslam.sensors import RPLidarA1 as LaserModel
from rplidar import RPLidar as Lidar
from roboviz import MapVisualizer # this occurs error when there's no display connected on odroid

from PIL import Image
import io
import os


MAP_SIZE_PIXELS     = 3000
MAP_SIZE_METERS     = 3 #10m * 10m plain
LIDAR_DEVICE        = '/dev/ttyUSB0'

MIN_SAMPLES         = 120 #default value 200, maximum 250, odroid maximum 140


class narlam:
    def __init__(self):
        self.flag = 0;
        self.lidar = Lidar(LIDAR_DEVICE)
        self.slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)
        self.viz = MapVisualizer(MAP_SIZE_PIXELS, MAP_SIZE_METERS, 'SLAM MAP') # no visualizer needed
        self.trajectory = []
        self.mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)
        self.iterator = self.lidar.iter_scans()

        self.previous_distances = None
        self.previous_angles    = None

        self.x      = 0.0
        self.y      = 0.0
        self.theta  = 0.0

    def slam_no_map(self, path_map_name):
        # doing slam with building maps from zero simultaneously
        next(self.iterator)

        while True:
            if self.flag == 1:
                break

            items = [item for item in next(self.iterator)]

            distances   = [item[2] for item in items]
            angles      = [item[1] for item in items]

            if len(distances) > MIN_SAMPLES:
                self.slam.update(distances, scan_angles_degrees=angles)
                self.previous_distances = distances.copy()
                self.previous_angles    = angles.copy()

            elif self.previous_distances is not None:
                self.slam.update(self.previous_distances, scan_angles_degrees=self.previous_angles)

            self.x, local_y, local_theta = self.slam.getpos()
            local_theta = local_theta % 360
            if local_theta < 0:
                self.theta = 360 + local.theta
            else:
                self.theta = local_theta

            self.slam.getmap(self.mapbytes)

            # save map generated by slam
            image = Image.frombuffer('L', (MAP_SIZE_PIXELS, MAP_SIZE_PIXELS), self.mapbytes, 'raw', 'L', 0, 1)
            image.save(path_map_name)

        self.lidar.stop()
        self.lidar.disconnect()


    def slam_yes_map(self, path_map_name):
        # doing localization only, with pre-built map image file.
        
        with open(path_map_name, "rb") as map_img:
            f = map_img.read()
            b = bytearray(f)
            self.slam.setmap(b)

        next(self.iterator)

        while True:
            if self.flag == 1:
                break

            items = [item for item in next(self.iterator)]

            distances   = [item[2] for item in items]
            angles      = [item[1] for item in items]

            if len(distances) > MIN_SAMPLES:
                self.slam.update(distances, scan_angles_degrees=angles, should_update_map = False)
                self.previous_distances = distances.copy()
                self.previous_angles    = angles.copy()

            elif self.previous_distances is not None:
                self.slam.update(self.previous_distances, scan_angles_degrees=self.previous_angles, should_update_map = False)

            self.x, self.y, self.theta = self.slam.getpos()
            
        self.lidar.stop()
        self.lidar.disconnect()



