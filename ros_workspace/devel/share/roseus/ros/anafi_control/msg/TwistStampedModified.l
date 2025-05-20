;; Auto-generated. Do not edit!


(when (boundp 'anafi_control::TwistStampedModified)
  (if (not (find-package "ANAFI_CONTROL"))
    (make-package "ANAFI_CONTROL"))
  (shadow 'TwistStampedModified (find-package "ANAFI_CONTROL")))
(unless (find-package "ANAFI_CONTROL::TWISTSTAMPEDMODIFIED")
  (make-package "ANAFI_CONTROL::TWISTSTAMPEDMODIFIED"))

(in-package "ROS")
;;//! \htmlinclude TwistStampedModified.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass anafi_control::TwistStampedModified
  :super ros::object
  :slots (_header _twist ))

(defmethod anafi_control::TwistStampedModified
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:twist __twist) (instance anafi_control::TwistModified :init))
    )
   (send-super :init)
   (setq _header __header)
   (setq _twist __twist)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:twist
   (&rest __twist)
   (if (keywordp (car __twist))
       (send* _twist __twist)
     (progn
       (if __twist (setq _twist (car __twist)))
       _twist)))
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; anafi_control/TwistModified _twist
    (send _twist :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; anafi_control/TwistModified _twist
       (send _twist :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; anafi_control/TwistModified _twist
     (send _twist :deserialize buf ptr-) (incf ptr- (send _twist :serialization-length))
   ;;
   self)
  )

(setf (get anafi_control::TwistStampedModified :md5sum-) "953cf8d869ec497d6eb74723a9307a2e")
(setf (get anafi_control::TwistStampedModified :datatype-) "anafi_control/TwistStampedModified")
(setf (get anafi_control::TwistStampedModified :definition-)
      "Header header
anafi_control/TwistModified twist
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
MSG: anafi_control/TwistModified
geometry_msgs/Vector3Stamped linear
geometry_msgs/Vector3Stamped angular
================================================================================
MSG: geometry_msgs/Vector3Stamped
# This represents a Vector3 with reference coordinate frame and timestamp
Header header
Vector3 vector

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



(provide :anafi_control/TwistStampedModified "953cf8d869ec497d6eb74723a9307a2e")


