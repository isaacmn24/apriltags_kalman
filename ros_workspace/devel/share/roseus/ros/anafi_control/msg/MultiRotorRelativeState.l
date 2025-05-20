;; Auto-generated. Do not edit!


(when (boundp 'anafi_control::MultiRotorRelativeState)
  (if (not (find-package "ANAFI_CONTROL"))
    (make-package "ANAFI_CONTROL"))
  (shadow 'MultiRotorRelativeState (find-package "ANAFI_CONTROL")))
(unless (find-package "ANAFI_CONTROL::MULTIROTORRELATIVESTATE")
  (make-package "ANAFI_CONTROL::MULTIROTORRELATIVESTATE"))

(in-package "ROS")
;;//! \htmlinclude MultiRotorRelativeState.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass anafi_control::MultiRotorRelativeState
  :super ros::object
  :slots (_header _rel_p_x _rel_p_y _rel_p_z _rel_v_x _rel_v_y _rel_v_z _rel_yaw _roll _pitch _yaw _v_z _roll_rate _pitch_rate _yaw_rate ))

(defmethod anafi_control::MultiRotorRelativeState
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:rel_p_x __rel_p_x) 0.0)
    ((:rel_p_y __rel_p_y) 0.0)
    ((:rel_p_z __rel_p_z) 0.0)
    ((:rel_v_x __rel_v_x) 0.0)
    ((:rel_v_y __rel_v_y) 0.0)
    ((:rel_v_z __rel_v_z) 0.0)
    ((:rel_yaw __rel_yaw) 0.0)
    ((:roll __roll) 0.0)
    ((:pitch __pitch) 0.0)
    ((:yaw __yaw) 0.0)
    ((:v_z __v_z) 0.0)
    ((:roll_rate __roll_rate) 0.0)
    ((:pitch_rate __pitch_rate) 0.0)
    ((:yaw_rate __yaw_rate) 0.0)
    )
   (send-super :init)
   (setq _header __header)
   (setq _rel_p_x (float __rel_p_x))
   (setq _rel_p_y (float __rel_p_y))
   (setq _rel_p_z (float __rel_p_z))
   (setq _rel_v_x (float __rel_v_x))
   (setq _rel_v_y (float __rel_v_y))
   (setq _rel_v_z (float __rel_v_z))
   (setq _rel_yaw (float __rel_yaw))
   (setq _roll (float __roll))
   (setq _pitch (float __pitch))
   (setq _yaw (float __yaw))
   (setq _v_z (float __v_z))
   (setq _roll_rate (float __roll_rate))
   (setq _pitch_rate (float __pitch_rate))
   (setq _yaw_rate (float __yaw_rate))
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:rel_p_x
   (&optional __rel_p_x)
   (if __rel_p_x (setq _rel_p_x __rel_p_x)) _rel_p_x)
  (:rel_p_y
   (&optional __rel_p_y)
   (if __rel_p_y (setq _rel_p_y __rel_p_y)) _rel_p_y)
  (:rel_p_z
   (&optional __rel_p_z)
   (if __rel_p_z (setq _rel_p_z __rel_p_z)) _rel_p_z)
  (:rel_v_x
   (&optional __rel_v_x)
   (if __rel_v_x (setq _rel_v_x __rel_v_x)) _rel_v_x)
  (:rel_v_y
   (&optional __rel_v_y)
   (if __rel_v_y (setq _rel_v_y __rel_v_y)) _rel_v_y)
  (:rel_v_z
   (&optional __rel_v_z)
   (if __rel_v_z (setq _rel_v_z __rel_v_z)) _rel_v_z)
  (:rel_yaw
   (&optional __rel_yaw)
   (if __rel_yaw (setq _rel_yaw __rel_yaw)) _rel_yaw)
  (:roll
   (&optional __roll)
   (if __roll (setq _roll __roll)) _roll)
  (:pitch
   (&optional __pitch)
   (if __pitch (setq _pitch __pitch)) _pitch)
  (:yaw
   (&optional __yaw)
   (if __yaw (setq _yaw __yaw)) _yaw)
  (:v_z
   (&optional __v_z)
   (if __v_z (setq _v_z __v_z)) _v_z)
  (:roll_rate
   (&optional __roll_rate)
   (if __roll_rate (setq _roll_rate __roll_rate)) _roll_rate)
  (:pitch_rate
   (&optional __pitch_rate)
   (if __pitch_rate (setq _pitch_rate __pitch_rate)) _pitch_rate)
  (:yaw_rate
   (&optional __yaw_rate)
   (if __yaw_rate (setq _yaw_rate __yaw_rate)) _yaw_rate)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; float64 _rel_p_x
    8
    ;; float64 _rel_p_y
    8
    ;; float64 _rel_p_z
    8
    ;; float64 _rel_v_x
    8
    ;; float64 _rel_v_y
    8
    ;; float64 _rel_v_z
    8
    ;; float64 _rel_yaw
    8
    ;; float64 _roll
    8
    ;; float64 _pitch
    8
    ;; float64 _yaw
    8
    ;; float64 _v_z
    8
    ;; float64 _roll_rate
    8
    ;; float64 _pitch_rate
    8
    ;; float64 _yaw_rate
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; float64 _rel_p_x
       (sys::poke _rel_p_x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _rel_p_y
       (sys::poke _rel_p_y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _rel_p_z
       (sys::poke _rel_p_z (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _rel_v_x
       (sys::poke _rel_v_x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _rel_v_y
       (sys::poke _rel_v_y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _rel_v_z
       (sys::poke _rel_v_z (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _rel_yaw
       (sys::poke _rel_yaw (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _roll
       (sys::poke _roll (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _pitch
       (sys::poke _pitch (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _yaw
       (sys::poke _yaw (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _v_z
       (sys::poke _v_z (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _roll_rate
       (sys::poke _roll_rate (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _pitch_rate
       (sys::poke _pitch_rate (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _yaw_rate
       (sys::poke _yaw_rate (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; float64 _rel_p_x
     (setq _rel_p_x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _rel_p_y
     (setq _rel_p_y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _rel_p_z
     (setq _rel_p_z (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _rel_v_x
     (setq _rel_v_x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _rel_v_y
     (setq _rel_v_y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _rel_v_z
     (setq _rel_v_z (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _rel_yaw
     (setq _rel_yaw (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _roll
     (setq _roll (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _pitch
     (setq _pitch (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _yaw
     (setq _yaw (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _v_z
     (setq _v_z (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _roll_rate
     (setq _roll_rate (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _pitch_rate
     (setq _pitch_rate (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _yaw_rate
     (setq _yaw_rate (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get anafi_control::MultiRotorRelativeState :md5sum-) "992f417326c3849f951a20961ff27171")
(setf (get anafi_control::MultiRotorRelativeState :datatype-) "anafi_control/MultiRotorRelativeState")
(setf (get anafi_control::MultiRotorRelativeState :definition-)
      "Header header
float64 rel_p_x
float64 rel_p_y
float64 rel_p_z
float64 rel_v_x
float64 rel_v_y
float64 rel_v_z
float64 rel_yaw
float64 roll
float64 pitch
float64 yaw
float64 v_z
float64 roll_rate
float64 pitch_rate
float64 yaw_rate





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

")



(provide :anafi_control/MultiRotorRelativeState "992f417326c3849f951a20961ff27171")


