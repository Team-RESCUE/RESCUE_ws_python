# RESCUE_ws_python

The RESCUE software package lives in this repository. `rescue_ws` is the main functional directory, while `motor_control` holds servo and motor control scripts that were later integrated into the ROS framework in `rescue_ws`.

## Operation

### Setup
Before running RESCUE (and likely before embarking MARBLE into the competition course), the Raspberry Pi units (a Pi 4 B at the base and a Pi Zero W at the end effector) must be activated. To do so, plug the base Pi into a USB-C power cable and connect the battery to the integrated end effector circuit (yellow plug hanging from battery to matching port for circuit). The Raspberry Pi's should be running shell scripts that will enable their respective ROS nodes on boot such that the command listed below should work as soon as startup is complete (which could take upwards of 30 seconds to a minute for the Pi Zero W).

**Important Setup Notes** 

* The Raspberry Pi's will almost certainly need minor replacements in their `rc.local` files. At the bottom of the files will be a `ROS network setup` section with a set of ROS configuration IP addresses - specifically `ROS_MASTER_URI`,`ROS_HOSTNAME`, and `ROS_IP`. 
  * The `ROS_MASTER_URI` should contain a different IP address than the others - replace this IP with the local IP of the machine running the MARBLE node.
  * The other two parameters should contain the local IP address of their respective Raspberry Pi.
  * This section should be mimicked in the .bashrc file for the machine running the MARBLE node, but with all 3 IP addresses listed as the respective machine's local IP.

* The Pi's will also need local network connection processes reconfigured - they currently use a `wpa_supplicant.conf` file as described in [this](https://maker.pro/raspberry-pi/projects/how-to-connect-a-raspberry-pi-to-a-laptop-display) tutorial (other similar tutorials for Raspberry Pi headless setup can be found online as well).

* Due to testing constraints, local network testing was all performed over a local WiFi network. If MARBLE's local network behaves differently than a router might, then it may be worth re-formatting the automated connection setup currently used in `wpa_supplicant.conf`.

### Command
After initial setup, RESCUE can be launched with a single line to the terminal:
```
roslaunch rescue_pkg_noetic marble_dummy.launch type_flag:=<param> coord1:=<param> coord2:=<param> coord3:=<param>
```
This launches the `marble_dummy.launch` file, which in turn launches the `marble_dummy` node. This node can be swapped out for MARBLE's purposes, so long as publications, subscriptions, and dependencies match.

### Parameters
* `type_flag`: a character denoting the nature of the 3 input coordinates of the end effector target location
  * `a` for pivot/rotation angles and extension distance
  * `c` for relative inertial coordinates

* `coord1`: pivot angle in degrees or relative inertial _x_ in centimeters
* `coord2`: rotation angle in degrees or relative inertial _y_ in centimeters
* `coord3`: extension distance in centimeters or relative inertial _z_ in centimeters

### Other Asides
* The video data transfer automation functionality is still being finalized at the moment. A commit will be made to this repository shortly with that functionality integrated and documented in comments.
