;; Auto-generated. Do not edit!


(when (boundp 'uav_msgs::uav_pose)
  (if (not (find-package "UAV_MSGS"))
    (make-package "UAV_MSGS"))
  (shadow 'uav_pose (find-package "UAV_MSGS")))
(unless (find-package "UAV_MSGS::UAV_POSE")
  (make-package "UAV_MSGS::UAV_POSE"))

(in-package "ROS")
;;//! \htmlinclude uav_pose.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass uav_msgs::uav_pose
  :super ros::object
  :slots (_header _position _velocity _orientation _covariance _angVelocity _thrust _flightmode _POI ))

(defmethod uav_msgs::uav_pose
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:position __position) (instance geometry_msgs::Point :init))
    ((:velocity __velocity) (instance geometry_msgs::Point :init))
    ((:orientation __orientation) (instance geometry_msgs::Quaternion :init))
    ((:covariance __covariance) (make-array 100 :initial-element 0.0 :element-type :float))
    ((:angVelocity __angVelocity) (instance geometry_msgs::Point :init))
    ((:thrust __thrust) 0.0)
    ((:flightmode __flightmode) 0)
    ((:POI __POI) (instance geometry_msgs::Point :init))
    )
   (send-super :init)
   (setq _header __header)
   (setq _position __position)
   (setq _velocity __velocity)
   (setq _orientation __orientation)
   (setq _covariance __covariance)
   (setq _angVelocity __angVelocity)
   (setq _thrust (float __thrust))
   (setq _flightmode (round __flightmode))
   (setq _POI __POI)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:position
   (&rest __position)
   (if (keywordp (car __position))
       (send* _position __position)
     (progn
       (if __position (setq _position (car __position)))
       _position)))
  (:velocity
   (&rest __velocity)
   (if (keywordp (car __velocity))
       (send* _velocity __velocity)
     (progn
       (if __velocity (setq _velocity (car __velocity)))
       _velocity)))
  (:orientation
   (&rest __orientation)
   (if (keywordp (car __orientation))
       (send* _orientation __orientation)
     (progn
       (if __orientation (setq _orientation (car __orientation)))
       _orientation)))
  (:covariance
   (&optional __covariance)
   (if __covariance (setq _covariance __covariance)) _covariance)
  (:angVelocity
   (&rest __angVelocity)
   (if (keywordp (car __angVelocity))
       (send* _angVelocity __angVelocity)
     (progn
       (if __angVelocity (setq _angVelocity (car __angVelocity)))
       _angVelocity)))
  (:thrust
   (&optional __thrust)
   (if __thrust (setq _thrust __thrust)) _thrust)
  (:flightmode
   (&optional __flightmode)
   (if __flightmode (setq _flightmode __flightmode)) _flightmode)
  (:POI
   (&rest __POI)
   (if (keywordp (car __POI))
       (send* _POI __POI)
     (progn
       (if __POI (setq _POI (car __POI)))
       _POI)))
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; geometry_msgs/Point _position
    (send _position :serialization-length)
    ;; geometry_msgs/Point _velocity
    (send _velocity :serialization-length)
    ;; geometry_msgs/Quaternion _orientation
    (send _orientation :serialization-length)
    ;; float64[100] _covariance
    (* 8    100)
    ;; geometry_msgs/Point _angVelocity
    (send _angVelocity :serialization-length)
    ;; float64 _thrust
    8
    ;; int32 _flightmode
    4
    ;; geometry_msgs/Point _POI
    (send _POI :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; geometry_msgs/Point _position
       (send _position :serialize s)
     ;; geometry_msgs/Point _velocity
       (send _velocity :serialize s)
     ;; geometry_msgs/Quaternion _orientation
       (send _orientation :serialize s)
     ;; float64[100] _covariance
     (dotimes (i 100)
       (sys::poke (elt _covariance i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; geometry_msgs/Point _angVelocity
       (send _angVelocity :serialize s)
     ;; float64 _thrust
       (sys::poke _thrust (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; int32 _flightmode
       (write-long _flightmode s)
     ;; geometry_msgs/Point _POI
       (send _POI :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; geometry_msgs/Point _position
     (send _position :deserialize buf ptr-) (incf ptr- (send _position :serialization-length))
   ;; geometry_msgs/Point _velocity
     (send _velocity :deserialize buf ptr-) (incf ptr- (send _velocity :serialization-length))
   ;; geometry_msgs/Quaternion _orientation
     (send _orientation :deserialize buf ptr-) (incf ptr- (send _orientation :serialization-length))
   ;; float64[100] _covariance
   (dotimes (i (length _covariance))
     (setf (elt _covariance i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     )
   ;; geometry_msgs/Point _angVelocity
     (send _angVelocity :deserialize buf ptr-) (incf ptr- (send _angVelocity :serialization-length))
   ;; float64 _thrust
     (setq _thrust (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; int32 _flightmode
     (setq _flightmode (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; geometry_msgs/Point _POI
     (send _POI :deserialize buf ptr-) (incf ptr- (send _POI :serialization-length))
   ;;
   self)
  )

(setf (get uav_msgs::uav_pose :md5sum-) "fd14362fea18a862170f6b52a4253b6e")
(setf (get uav_msgs::uav_pose :datatype-) "uav_msgs/uav_pose")
(setf (get uav_msgs::uav_pose :definition-)
      "# A representation of 3D position, 3D orientation and 3D velocity and in free space, composed of position and orientation.
# Point position (north,east,down)
# Point velocity (north,east,down)
# Quaternion orientation (x,y,z,w -- 0,0,0,1 = X(front)-> north, Y(right)-> east, Z(bottom))
# float64[100] covariance diagonal 10x10 matrix, column order: posN,posE,posD,velN,velE,velD,Qx,Qy,Qz,Qw
# Point rotation (roll,pitch,yaw)
# float64 thrust (power setting -1 <= thrust <= +1 , negative thrust=engine off)
# int32 flightmode (TODO: to be defined later)
# NOTE: To include complete covariance information, a float32[100] Covariance (10x10 matrix) would be needed as well. Transferring that with every update might limit bandwidth significantly.


Header header
geometry_msgs/Point position
geometry_msgs/Point velocity
geometry_msgs/Quaternion orientation  
float64[100] covariance
geometry_msgs/Point angVelocity
float64 thrust
int32 flightmode
geometry_msgs/Point POI
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
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w

")



(provide :uav_msgs/uav_pose "fd14362fea18a862170f6b52a4253b6e")


