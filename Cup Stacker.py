#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain = Brain()

# Robot configuration code
brain_inertial = Inertial()
left_drive_smart = Motor(Ports.PORT6, False)
right_drive_smart = Motor(Ports.PORT2, True)
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, brain_inertial, 259.34, 320, 40, MM, 1)
sideways_motor_a = Motor(Ports.PORT7, False)
sideways_motor_b = Motor(Ports.PORT10, True)
sideways = MotorGroup(sideways_motor_a, sideways_motor_b)
crane = Motor(Ports.PORT4, False)
claw = Motor(Ports.PORT3, False)
front_distance = Distance(Ports.PORT1)
base_distance = Distance(Ports.PORT5)


# Wait for sensor(s) to fully initialize
wait(100, MSEC)

# generating and setting random seed
def initializeRandomSeed():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    systemTime = brain.timer.system() * 100
    urandom.seed(int(xaxis + yaxis + zaxis + systemTime)) 

# Initialize random seed 
initializeRandomSeed()

vexcode_initial_drivetrain_calibration_completed = False
def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    global vexcode_initial_drivetrain_calibration_completed
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Inertial")
    brain_inertial.calibrate()
    while brain_inertial.is_calibrating():
        sleep(25, MSEC)
    vexcode_initial_drivetrain_calibration_completed = True
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)


# Calibrate the Drivetrain
calibrate_drivetrain()

#endregion VEXcode Generated Robot Configuration
# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode EXP Python Project
# 
# ------------------------------------------

# Library imports
from vex import *

# Begin project code

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#Configure side drivetrain
side_drivetrain = SmartDrive(sideways_motor_a, sideways_motor_b, brain_inertial, 259.34, 320, 40, MM, 1)
drivetrain.set_drive_velocity(10, PERCENT)
crane.set_max_torque(100, PERCENT)
side_drivetrain.set_drive_velocity(10, PERCENT)
claw.set_max_torque(15, PERCENT)

#Measures in MM
MAX_VISION_RANGE = 300

DISTANCE_FOR_TOP_LAYER = 185
DISTANCE_FOR_MIDDLE_LAYER = 190
DISTANCE_FOR_BOTTOM_LAYER = 167

SIDE_DISTANCE_FOR_TOP_LAYER = -120
SIDE_DISTANCE_FOR_MIDDLE_LAYER = -85
SIDE_DISTANCE_FOR_BOTTOM_LAYER = 20

current_pos = Point(0, 0)
    
def drive_forward(distance):
    if distance >= 0:
        drivetrain.drive_for(FORWARD, distance, MM)
    else:
        drivetrain.drive_for(REVERSE, -distance, MM)
    # Distance tracking
    global current_pos
    current_pos = Point(current_pos.x, current_pos.y + distance)

def drive_sideward(distance):
    if distance >= 0:
        side_drivetrain.drive_for(FORWARD, distance, MM)
    else:
        side_drivetrain.drive_for(REVERSE, -distance, MM)
    # Distance tracking
    global current_pos
    current_pos = Point(current_pos.x + distance, current_pos.y)

def get_cup():
    # Reverse to not hit the side of any cups
    drive_forward(-50)

    # Open claw
    claw.spin(REVERSE)

    # Locate
    while front_distance.object_distance(MM) > MAX_VISION_RANGE:
        drive_sideward(18)
    drive_sideward(36)

    # Drive towards cup (+20 due to sensor inaccuracy)
    drive_forward(front_distance.object_distance(MM) + 20)
    wait(0.1, SECONDS)

    # Close claw
    claw.spin(FORWARD)
    wait(1, SECONDS)

    # Lift crane
    crane.spin_to_position(360, DEGREES, wait=True)
        
def drive_to_point(x, y):
    global current_pos
    move_side = x - current_pos.x
    move_forward = y - current_pos.y
    drive_forward(move_forward)
    drive_sideward(move_side)

def place_cup(crane_angle):
    crane.spin_to_position(crane_angle, DEGREES, wait=True)
    # Open claw small amount so other cups not hit
    claw.spin_for(REVERSE, 5, DEGREES)
    crane.spin_to_position(360, DEGREES, wait=True)
    
def find_placed_cup():
    while base_distance.object_distance(MM) > MAX_VISION_RANGE:
        # Small drive amount for greater precision
        drive_sideward(-5)

def align():
    # Re-aligns the robot to original heading if out by more than 1 degree
    if drivetrain.heading(DEGREES) > 1 and drivetrain.heading(DEGREES) < 359:
        drivetrain.turn_to_heading(0, DEGREES)

# Cup 1
get_cup()
align()
drive_to_point(0, 0)
align()
place_cup(0)
drive_sideward(100)
crane.spin_to_position(0, DEGREES, wait=True)

# Subsequent cups follow this method after picking up the cup:
#   Drive to the right of the stack (drive_to_point)
#   Scan for the furthest right cup on bottom layer (find_placed_cup)
#   Drive forward/backward to get the the correct y-coordinate for placement
#   Drive left to get the the correct x-coordinate for placement
#   Place the cup
#   Drive to the right of the stack and drop claw ready to get the next cup

# Cup 2
get_cup()
align()
drive_to_point(100, 0)
align()
find_placed_cup()
distance_to_move = base_distance.object_distance(MM) - DISTANCE_FOR_BOTTOM_LAYER
drive_forward(distance_to_move)
drive_sideward(SIDE_DISTANCE_FOR_BOTTOM_LAYER)
place_cup(0)
drive_sideward(90)
crane.spin_to_position(0, DEGREES, wait=True)

# Push cups together to reduce gaps
drive_forward(distance_to_move + 40)
claw.set_velocity(10, PERCENT)
claw.spin_for(REVERSE, 30, DEGREES)
claw.set_velocity(50, PERCENT)
drive_sideward(-10)
drive_sideward(10)
drive_forward(-distance_to_move - 40)


# Cup 3 (Top of 1 and 2)
get_cup()
align()
drive_to_point(200, 0)
align()
find_placed_cup()
drive_forward(base_distance.object_distance(MM) - DISTANCE_FOR_MIDDLE_LAYER)
drive_sideward(SIDE_DISTANCE_FOR_MIDDLE_LAYER)
place_cup(180)

drive_sideward(150)
crane.spin_to_position(0, DEGREES, wait=True)
# Bigger stack

# Cup 4 (Bottom Layer)
get_cup()
align()
drive_to_point(200, 0)
align()
find_placed_cup()
distance_to_move = base_distance.object_distance(MM) - DISTANCE_FOR_BOTTOM_LAYER
drive_forward(distance_to_move)
drive_sideward(SIDE_DISTANCE_FOR_BOTTOM_LAYER)
place_cup(0)
drive_sideward(84)
crane.spin_to_position(0, DEGREES, wait=True)

# Push cups together to reduce gaps
drive_forward(distance_to_move + 40)
claw.set_velocity(10, PERCENT)
claw.spin_for(REVERSE, 30, DEGREES)
claw.set_velocity(50, PERCENT)
drive_sideward(-10)
drive_sideward(10)
drive_forward(-distance_to_move - 40)

# Cup 5 (Top of 2 and 4)
get_cup()
align()
drive_to_point(300, 0)
align()
find_placed_cup()
drive_forward(base_distance.object_distance(MM) - DISTANCE_FOR_MIDDLE_LAYER)
drive_sideward(SIDE_DISTANCE_FOR_MIDDLE_LAYER)
place_cup(180)
drive_sideward(150)
crane.spin_to_position(0, DEGREES, wait=True)

# Cup 6 (Top Layer)
get_cup()
align()
drive_to_point(300, 0)
align()
find_placed_cup()
drive_forward(base_distance.object_distance(MM) - DISTANCE_FOR_TOP_LAYER)
drive_sideward(SIDE_DISTANCE_FOR_TOP_LAYER)
place_cup(300)

# Fully open claw
claw.spin(REVERSE)

# Move away from the stack and drop the claw
drive_forward(-70)
crane.spin_to_position(360, DEGREES, wait=True)
drive_forward(-70)
crane.spin_to_position(0, DEGREES, wait=True)
claw.stop()