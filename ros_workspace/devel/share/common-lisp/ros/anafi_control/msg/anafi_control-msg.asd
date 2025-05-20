
(cl:in-package :asdf)

(defsystem "anafi_control-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
               :std_msgs-msg
)
  :components ((:file "_package")
    (:file "MultiRotorRelativeState" :depends-on ("_package_MultiRotorRelativeState"))
    (:file "_package_MultiRotorRelativeState" :depends-on ("_package"))
    (:file "State" :depends-on ("_package_State"))
    (:file "_package_State" :depends-on ("_package"))
    (:file "TwistModified" :depends-on ("_package_TwistModified"))
    (:file "_package_TwistModified" :depends-on ("_package"))
    (:file "TwistStampedModified" :depends-on ("_package_TwistStampedModified"))
    (:file "_package_TwistStampedModified" :depends-on ("_package"))
    (:file "Waypoint" :depends-on ("_package_Waypoint"))
    (:file "_package_Waypoint" :depends-on ("_package"))
  ))