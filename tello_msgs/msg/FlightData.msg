std_msgs/Header header

#######
# Raw string
#######

string raw

#######
# SDK version
#######

uint8 SDK_UNKNOWN=0
uint8 SDK_1_3=1
uint8 SDK_2_0=2
uint8 sdk

#######
# SDK 1.3+ fields
#######



int32 templ   # lowest temp in C
int32 temph   # highest temp in C

int32 tof     # time of flight distance in cm
int32 h       # height in cm

int32 bat     # battery %

float32 baro  # barometric altitude in m
int32 time    # time used by motor in seconds


#######
# SDK 2.0+ fields
#######

int32 mid     # mission pad id, or -1 if not found
int32 x       # x coord relative to mission pad in cm, or 0 if not found
int32 y       # y coord relative to mission pad in cm, or 0 if not found
int32 z       # z coord relative to mission pad in cm, or 0 if not found