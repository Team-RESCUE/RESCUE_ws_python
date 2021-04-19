
(cl:in-package :asdf)

(defsystem "rescue_pkg_noetic-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "Num" :depends-on ("_package_Num"))
    (:file "_package_Num" :depends-on ("_package"))
    (:file "location_command" :depends-on ("_package_location_command"))
    (:file "_package_location_command" :depends-on ("_package"))
  ))