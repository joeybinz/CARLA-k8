# Copied from https://carla.readthedocs.io/en/latest/tuto_first_steps/

import carla
import random
import logging
import time
from subprocess import Popen, PIPE

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("connecting to carla...")
# Connect to the client and retrieve the world object
client = carla.Client('localhost', 2000)
world = client.get_world()

logging.info("connected to carla!")

logging.info("resetting world...")
client.load_world('Town05')

logging.info("spawning vehicles...")
# Get the blueprint library and filter for the vehicle blueprints
vehicle_blueprints = world.get_blueprint_library().filter('*vehicle*')

# Get the map's spawn points
spawn_points = world.get_map().get_spawn_points()

# Spawn 50 vehicles randomly distributed throughout the map
# for each spawn point, we choose a random vehicle from the blueprint library
for i in range(0, 50):
    world.try_spawn_actor(random.choice(
        vehicle_blueprints), random.choice(spawn_points))

ego_vehicle = world.spawn_actor(random.choice(
    vehicle_blueprints), random.choice(spawn_points))

logging.info("creating camera...")
# Create a transform to place the camera on top of the vehicle
camera_init_trans = carla.Transform(carla.Location(z=1.5))

# We create the camera through a blueprint that defines its properties
camera_bp = world.get_blueprint_library().find('sensor.camera.rgb')
camera_bp.set_attribute("image_size_x", '800')
camera_bp.set_attribute("image_size_y", '600')
camera_bp.set_attribute("sensor_tick", '0.5')

# We spawn the camera and attach it to our ego vehicle
camera = world.spawn_actor(camera_bp, camera_init_trans, attach_to=ego_vehicle)

p = Popen(["ffmpeg",
           "-f", "rawvideo",
           "-pixel_format", "bgra",
           "-framerate", "2",
           "-video_size", "800x600",
           "-i", "-",
           "-vcodec", "libx264",
           "-f", "flv", "rtmp://localhost/live/test"
           ], stdin=PIPE)


def push_image(image):
    p.stdin.write(image.raw_data)


camera.listen(push_image)


logging.info("starting auto pilot...")
for vehicle in world.get_actors().filter('*vehicle*'):
    vehicle.set_autopilot(True)

logging.info("done, sleeping...")
while True:
    time.sleep(60)
