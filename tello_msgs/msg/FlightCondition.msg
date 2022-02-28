std_msgs/Header header

int32 pitch   # pitch in degrees
int32 roll    # roll in degrees
int32 yaw     # yaw in degrees relative to startup orientation

float32 vgx     # x velocity in m/s, +forward
float32 vgy     # y velocity in m/s, +right
float32 vgz     # z velocity in m/s, +down
float32 wgz     # z angular velocity in rad/sec, +ccw

int32 tof     # time of flight distance in cm
int32 h       # height in cm

float32 baro  # barometric altitude in m
int32 time    # time used by motor in seconds

# Acceleration includes gravity
float32 agx   # x acceleration in mm/s^2, +forward
float32 agy   # y acceleration in mm/s^2, +right
float32 agz   # z acceleration in mm/s^2, +down
float32 awgz  # z angular acceleration in rad/s^2, +ccw

