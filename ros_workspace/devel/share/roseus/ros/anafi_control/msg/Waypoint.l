;; Auto-generated. Do not edit!


(when (boundp 'anafi_control::Waypoint)
  (if (not (find-package "ANAFI_CONTROL"))
    (make-package "ANAFI_CONTROL"))
  (shadow 'Waypoint (find-package "ANAFI_CONTROL")))
(unless (find-package "ANAFI_CONTROL::WAYPOINT")
  (make-package "ANAFI_CONTROL::WAYPOINT"))

(in-package "ROS")
;;//! \htmlinclude Waypoint.msg.html


(defclass anafi_control::Waypoint
  :super ros::object
  :slots (_x _y _z _v_x _v_y _v_z _yaw ))

(defmethod anafi_control::Waypoint
  (:init
   (&key
    ((:x __x) 0.0)
    ((:y __y) 0.0)
    ((:z __z) 0.0)
    ((:v_x __v_x) 0.0)
    ((:v_y __v_y) 0.0)
    ((:v_z __v_z) 0.0)
    ((:yaw __yaw) 0.0)
    )
   (send-super :init)
   (setq _x (float __x))
   (setq _y (float __y))
   (setq _z (float __z))
   (setq _v_x (float __v_x))
   (setq _v_y (float __v_y))
   (setq _v_z (float __v_z))
   (setq _yaw (float __yaw))
   self)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:z
   (&optional __z)
   (if __z (setq _z __z)) _z)
  (:v_x
   (&optional __v_x)
   (if __v_x (setq _v_x __v_x)) _v_x)
  (:v_y
   (&optional __v_y)
   (if __v_y (setq _v_y __v_y)) _v_y)
  (:v_z
   (&optional __v_z)
   (if __v_z (setq _v_z __v_z)) _v_z)
  (:yaw
   (&optional __yaw)
   (if __yaw (setq _yaw __yaw)) _yaw)
  (:serialization-length
   ()
   (+
    ;; float64 _x
    8
    ;; float64 _y
    8
    ;; float64 _z
    8
    ;; float64 _v_x
    8
    ;; float64 _v_y
    8
    ;; float64 _v_z
    8
    ;; float64 _yaw
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _x
       (sys::poke _x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _y
       (sys::poke _y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _z
       (sys::poke _z (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _v_x
       (sys::poke _v_x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _v_y
       (sys::poke _v_y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _v_z
       (sys::poke _v_z (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _yaw
       (sys::poke _yaw (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _x
     (setq _x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _y
     (setq _y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _z
     (setq _z (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _v_x
     (setq _v_x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _v_y
     (setq _v_y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _v_z
     (setq _v_z (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _yaw
     (setq _yaw (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get anafi_control::Waypoint :md5sum-) "c72c4e4d66b8cdce8f9bcb0dbae36dca")
(setf (get anafi_control::Waypoint :datatype-) "anafi_control/Waypoint")
(setf (get anafi_control::Waypoint :definition-)
      "float64 x                      # x-position [m] in world frame
float64 y                      # y-position [m] in world frame
float64 z                      # z-position [m] in world frame
float64 v_x                   # x-velocity [m/s] in world frame
float64 v_y                   # y-velocity [m/s] in world frame
float64 v_z                   # z-velocity [m/s] in world frame
float64 yaw                   # yaw angle [deg] in world frame

")



(provide :anafi_control/Waypoint "c72c4e4d66b8cdce8f9bcb0dbae36dca")


