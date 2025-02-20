
(cl:in-package :asdf)

(defsystem "uav_msgs-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
               :std_msgs-msg
)
  :components ((:file "_package")
    (:file "uav_pose" :depends-on ("_package_uav_pose"))
    (:file "_package_uav_pose" :depends-on ("_package"))
  ))