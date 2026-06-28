uint8 IDLE=0
uint8 ACTIVE=1
uint8 PAUSED=2
uint8 EMERGENCY_STOP=3
uint8 SHUTDOWN=4

uint8 robot_state

bool mission_active

float32 linear_velocity
float32 angular_velocity

float32 battery_percentage

builtin_interfaces/Time stamp