# An example of how to control 2 drones using the ros2 CLI
# Uses "rc x y z yaw" to control velocity
# Do _not_ launch the joystick nodes

ros2 service call /drone1/tello_action tello_msgs/TelloAction "{cmd: 'takeoff'}"
sleep 4

ros2 service call /drone1/move_cmd tello_interfaces/srv/HexaCmd "{dir: xy, dist: 1.57}" # 90 degree rot

sleep 10

ros2 service call /drone1/move_cmd tello_interfaces/srv/HexaCmd "{dir: x, dist: 2.8}"

sleep 7

ros2 service call /drone1/move_cmd tello_interfaces/srv/HexaCmd "{dir: y, dist: -9.3}"

sleep 10

ros2 service call /drone1/move_cmd tello_interfaces/srv/HexaCmd "{dir: xy, dist: 1.58}" # 90 degree rot

sleep 10

ros2 service call /drone1/move_cmd tello_interfaces/srv/HexaCmd "{dir: y, dist: -2}"

sleep 7

ros2 service call /drone1/move_cmd tello_interfaces/srv/HexaCmd "{dir: xy, dist: 1.57}" # 90 degree rot

sleep 10

ros2 service call /drone1/move_cmd tello_interfaces/srv/HexaCmd "{dir: y, dist: -9.3}"

sleep 10

ros2 service call /drone1/move_cmd tello_interfaces/srv/HexaCmd "{dir: xy, dist: 1.58}" # 90 degree rot

sleep 10

ros2 service call /drone1/move_cmd tello_interfaces/srv/HexaCmd "{dir: y, dist: 2}"

sleep 10

ros2 service call /drone1/move_cmd tello_interfaces/srv/HexaCmd "{dir: xy, dist: -1.58}" # 90 degree rot

sleep 10

ros2 service call /drone1/move_cmd tello_interfaces/srv/HexaCmd "{dir: y, dist: 9.3}"

sleep 10

ros2 service call /drone1/move_cmd tello_interfaces/srv/HexaCmd "{dir: x, dist: 2.0}"

sleep 7

ros2 service call /drone1/move_cmd tello_interfaces/srv/HexaCmd "{dir: xy, dist: 1.57}" # 90 degree rot

sleep 10

ros2 service call /drone1/move_cmd tello_interfaces/srv/HexaCmd "{dir: x, dist: 5}"

sleep 10

ros2 service call /drone1/move_cmd tello_interfaces/srv/HexaCmd "{dir: xy, dist: 3.14}" # 90 degree rot

sleep 10

ros2 service call /drone1/tello_action tello_msgs/TelloAction "{cmd: 'land'}"

