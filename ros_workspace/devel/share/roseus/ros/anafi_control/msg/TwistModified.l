;; Auto-generated. Do not edit!


(when (boundp 'anafi_control::TwistModified)
  (if (not (find-package "ANAFI_CONTROL"))
    (make-package "ANAFI_CONTROL"))
  (shadow 'TwistModified (find-package "ANAFI_CONTROL")))
(unless (find-package "ANAFI_CONTROL::TWISTMODIFIED")
  (make-package "ANAFI_CONTROL::TWISTMODIFIED"))

(in-package "ROS")
;;//! \htmlinclude TwistModified.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass anafi_control::TwistModified
  :super ros::object
  :slots (_linear _angular ))

(defmethod anafi_control::TwistModified
  (:init
   (&key
    ((:linear __linear) (instance geometry_msgs::Vector3Stamped :init))
    ((:angular __angular) (instance geometry_msgs::Vector3Stamped :init))
    )
   (send-super :init)
   (setq _linear __linear)
   (setq _angular __angular)
   self)
  (:linear
   (&rest __linear)
   (if (keywordp (car __linear))
       (send* _linear __linear)
     (progn
       (if __linear (setq _linear (car __linear)))
       _linear)))
  (:angular
   (&rest __angular)
   (if (keywordp (car __angular))
       (send* _angular __angular)
     (progn
       (if __angular (setq _angular (car __angular)))
       _angular)))
  (:serialization-length
   ()
   (+
    ;; geometry_msgs/Vector3Stamped _linear
    (send _linear :serialization-length)
    ;; geometry_msgs/Vector3Stamped _angular
    (send _angular :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; geometry_msgs/Vector3Stamped _linear
       (send _linear :serialize s)
     ;; geometry_msgs/Vector3Stamped _angular
       (send _angular :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; geometry_msgs/Vector3Stamped _linear
     (send _linear :deserialize buf ptr-) (incf ptr- (send _linear :serialization-length))
   ;; geometry_msgs/Vector3Stamped _angular
     (send _angular :deserialize buf ptr-) (incf ptr- (send _angular :serialization-length))
   ;;
   self)
  )

(setf (get anafi_control::TwistModified :md5sum-) "2d3ab5e2b924162f6809bed7c278f6b8")
(setf (get anafi_control::TwistModified :datatype-) "anafi_control/TwistModified")
(setf (get anafi_control::TwistModified :definition-)
      "geometry_msgs/Vector3Stamped linear
geometry_msgs/Vector3Stamped angular
================================================================================
MSG: geometry_msgs/Vector3Stamped
# This represents a Vector3 with reference coordinate frame and timestamp
Header header
Vector3 vector

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: geometry_msgs/Vector3
# This represents a vector in free space. 
# It is only meant to represent a direction. Therefore, it does not
# make sense to apply a translation to it (e.g., when applying a 
# generic rigid transformation to a Vector3, tf2 will only apply the
# rotation). If you want your data to be translatable too, use the
# geometry_msgs/Point message instead.

float64 x
float64 y
float64 z
")



(provide :anafi_control/TwistModified "2d3ab5e2b924162f6809bed7c278f6b8")


