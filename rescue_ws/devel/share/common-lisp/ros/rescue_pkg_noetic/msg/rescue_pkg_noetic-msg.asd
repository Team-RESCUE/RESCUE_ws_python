
(cl:in-package :asdf)

(defsystem "rescue_pkg_noetic-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "Num" :depends-on ("_package_Num"))
    (:file "_package_Num" :depends-on ("_package"))
    (:file "co2" :depends-on ("_package_co2"))
    (:file "_package_co2" :depends-on ("_package"))
    (:file "location_command" :depends-on ("_package_location_command"))
    (:file "_package_location_command" :depends-on ("_package"))
    (:file "pan_tilt" :depends-on ("_package_pan_tilt"))
    (:file "_package_pan_tilt" :depends-on ("_package"))
    (:file "sensor_cmd" :depends-on ("_package_sensor_cmd"))
    (:file "_package_sensor_cmd" :depends-on ("_package"))
  ))