# RESCUE_ws_python

The RESCUE software package lives in this repository. `rescue_ws` is the main functional directory, while `motor_control` holds servo and motor control scripts that were later integrated into the ROS framework in `rescue_ws`.

## Operation

### Setup
Before running RESCUE (and likely before embarking MARBLE into the competition course), the Raspberry Pi units (a Pi 4 B at the base and a Pi Zero W at the end effector) must be activated. To do so, plug the base Pi into a USB-C power cable and connect the battery to the integrated end effector circuit (yellow plug hanging from battery to matching port for circuit). The Raspberry Pi's should be running shell scripts that will enable their respective ROS nodes on boot such that the command listed below should work as soon as startup is complete (which could take upwards of 30 seconds to a minute for the Pi Zero W).

### Command
RESCUE can be launched with a single line to the terminal:
```
roslaunch rescue_pkg_noetic marble_dummy.launch type_flag:=<param> coord1:=<param> coord2:=<param> coord3:=<param>
```
This launches the `marble_dummy.launch` file, which in turn launches the `marble_dummy` node. This node can be swapped out for MARBLE's purposes, so long as publications, subscriptions, and dependencies match.

### Parameters
- `type_flag`: a character denoting the nature of the 3 input coordinates of the end effector target location
-   options:
-   `a` for pivot/rotation angles and extension distance
-   `c` for relative inertial coordinates

`coord1`: pivot angle in degrees or relative inertial _x_ in centimeters
`coord2`: rotation angle in degrees or relative inertial _y_ in centimeters
`coord3`: extension distance in centimeters or relative inertial _z_ in centimeters

* `type_flag`: a character denoting the nature of the 3 input coordinates of the end effector target location
  * `a` for pivot/rotation angles and extension distance
  * `c` for relative inertial coordinates

* `coord1`: pivot angle in degrees or relative inertial _x_ in centimeters
* `coord2`: rotation angle in degrees or relative inertial _y_ in centimeters
* `coord3`: extension distance in centimeters or relative inertial _z_ in centimeters
