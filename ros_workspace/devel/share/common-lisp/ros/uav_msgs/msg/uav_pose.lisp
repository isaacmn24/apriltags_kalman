; Auto-generated. Do not edit!


(cl:in-package uav_msgs-msg)


;//! \htmlinclude uav_pose.msg.html

(cl:defclass <uav_pose> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (position
    :reader position
    :initarg :position
    :type geometry_msgs-msg:Point
    :initform (cl:make-instance 'geometry_msgs-msg:Point))
   (velocity
    :reader velocity
    :initarg :velocity
    :type geometry_msgs-msg:Point
    :initform (cl:make-instance 'geometry_msgs-msg:Point))
   (orientation
    :reader orientation
    :initarg :orientation
    :type geometry_msgs-msg:Quaternion
    :initform (cl:make-instance 'geometry_msgs-msg:Quaternion))
   (covariance
    :reader covariance
    :initarg :covariance
    :type (cl:vector cl:float)
   :initform (cl:make-array 100 :element-type 'cl:float :initial-element 0.0))
   (angVelocity
    :reader angVelocity
    :initarg :angVelocity
    :type geometry_msgs-msg:Point
    :initform (cl:make-instance 'geometry_msgs-msg:Point))
   (thrust
    :reader thrust
    :initarg :thrust
    :type cl:float
    :initform 0.0)
   (flightmode
    :reader flightmode
    :initarg :flightmode
    :type cl:integer
    :initform 0)
   (POI
    :reader POI
    :initarg :POI
    :type geometry_msgs-msg:Point
    :initform (cl:make-instance 'geometry_msgs-msg:Point)))
)

(cl:defclass uav_pose (<uav_pose>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <uav_pose>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'uav_pose)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name uav_msgs-msg:<uav_pose> is deprecated: use uav_msgs-msg:uav_pose instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <uav_pose>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader uav_msgs-msg:header-val is deprecated.  Use uav_msgs-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'position-val :lambda-list '(m))
(cl:defmethod position-val ((m <uav_pose>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader uav_msgs-msg:position-val is deprecated.  Use uav_msgs-msg:position instead.")
  (position m))

(cl:ensure-generic-function 'velocity-val :lambda-list '(m))
(cl:defmethod velocity-val ((m <uav_pose>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader uav_msgs-msg:velocity-val is deprecated.  Use uav_msgs-msg:velocity instead.")
  (velocity m))

(cl:ensure-generic-function 'orientation-val :lambda-list '(m))
(cl:defmethod orientation-val ((m <uav_pose>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader uav_msgs-msg:orientation-val is deprecated.  Use uav_msgs-msg:orientation instead.")
  (orientation m))

(cl:ensure-generic-function 'covariance-val :lambda-list '(m))
(cl:defmethod covariance-val ((m <uav_pose>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader uav_msgs-msg:covariance-val is deprecated.  Use uav_msgs-msg:covariance instead.")
  (covariance m))

(cl:ensure-generic-function 'angVelocity-val :lambda-list '(m))
(cl:defmethod angVelocity-val ((m <uav_pose>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader uav_msgs-msg:angVelocity-val is deprecated.  Use uav_msgs-msg:angVelocity instead.")
  (angVelocity m))

(cl:ensure-generic-function 'thrust-val :lambda-list '(m))
(cl:defmethod thrust-val ((m <uav_pose>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader uav_msgs-msg:thrust-val is deprecated.  Use uav_msgs-msg:thrust instead.")
  (thrust m))

(cl:ensure-generic-function 'flightmode-val :lambda-list '(m))
(cl:defmethod flightmode-val ((m <uav_pose>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader uav_msgs-msg:flightmode-val is deprecated.  Use uav_msgs-msg:flightmode instead.")
  (flightmode m))

(cl:ensure-generic-function 'POI-val :lambda-list '(m))
(cl:defmethod POI-val ((m <uav_pose>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader uav_msgs-msg:POI-val is deprecated.  Use uav_msgs-msg:POI instead.")
  (POI m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <uav_pose>) ostream)
  "Serializes a message object of type '<uav_pose>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'position) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'velocity) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'orientation) ostream)
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-double-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream)))
   (cl:slot-value msg 'covariance))
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'angVelocity) ostream)
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'thrust))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let* ((signed (cl:slot-value msg 'flightmode)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'POI) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <uav_pose>) istream)
  "Deserializes a message object of type '<uav_pose>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'position) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'velocity) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'orientation) istream)
  (cl:setf (cl:slot-value msg 'covariance) (cl:make-array 100))
  (cl:let ((vals (cl:slot-value msg 'covariance)))
    (cl:dotimes (i 100)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-double-float-bits bits)))))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'angVelocity) istream)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'thrust) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'flightmode) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'POI) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<uav_pose>)))
  "Returns string type for a message object of type '<uav_pose>"
  "uav_msgs/uav_pose")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'uav_pose)))
  "Returns string type for a message object of type 'uav_pose"
  "uav_msgs/uav_pose")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<uav_pose>)))
  "Returns md5sum for a message object of type '<uav_pose>"
  "fd14362fea18a862170f6b52a4253b6e")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'uav_pose)))
  "Returns md5sum for a message object of type 'uav_pose"
  "fd14362fea18a862170f6b52a4253b6e")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<uav_pose>)))
  "Returns full string definition for message of type '<uav_pose>"
  (cl:format cl:nil "# A representation of 3D position, 3D orientation and 3D velocity and in free space, composed of position and orientation.~%# Point position (north,east,down)~%# Point velocity (north,east,down)~%# Quaternion orientation (x,y,z,w -- 0,0,0,1 = X(front)-> north, Y(right)-> east, Z(bottom))~%# float64[100] covariance diagonal 10x10 matrix, column order: posN,posE,posD,velN,velE,velD,Qx,Qy,Qz,Qw~%# Point rotation (roll,pitch,yaw)~%# float64 thrust (power setting -1 <= thrust <= +1 , negative thrust=engine off)~%# int32 flightmode (TODO: to be defined later)~%# NOTE: To include complete covariance information, a float32[100] Covariance (10x10 matrix) would be needed as well. Transferring that with every update might limit bandwidth significantly.~%~%~%Header header~%geometry_msgs/Point position~%geometry_msgs/Point velocity~%geometry_msgs/Quaternion orientation  ~%float64[100] covariance~%geometry_msgs/Point angVelocity~%float64 thrust~%int32 flightmode~%geometry_msgs/Point POI~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'uav_pose)))
  "Returns full string definition for message of type 'uav_pose"
  (cl:format cl:nil "# A representation of 3D position, 3D orientation and 3D velocity and in free space, composed of position and orientation.~%# Point position (north,east,down)~%# Point velocity (north,east,down)~%# Quaternion orientation (x,y,z,w -- 0,0,0,1 = X(front)-> north, Y(right)-> east, Z(bottom))~%# float64[100] covariance diagonal 10x10 matrix, column order: posN,posE,posD,velN,velE,velD,Qx,Qy,Qz,Qw~%# Point rotation (roll,pitch,yaw)~%# float64 thrust (power setting -1 <= thrust <= +1 , negative thrust=engine off)~%# int32 flightmode (TODO: to be defined later)~%# NOTE: To include complete covariance information, a float32[100] Covariance (10x10 matrix) would be needed as well. Transferring that with every update might limit bandwidth significantly.~%~%~%Header header~%geometry_msgs/Point position~%geometry_msgs/Point velocity~%geometry_msgs/Quaternion orientation  ~%float64[100] covariance~%geometry_msgs/Point angVelocity~%float64 thrust~%int32 flightmode~%geometry_msgs/Point POI~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <uav_pose>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'position))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'velocity))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'orientation))
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'covariance) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'angVelocity))
     8
     4
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'POI))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <uav_pose>))
  "Converts a ROS message object to a list"
  (cl:list 'uav_pose
    (cl:cons ':header (header msg))
    (cl:cons ':position (position msg))
    (cl:cons ':velocity (velocity msg))
    (cl:cons ':orientation (orientation msg))
    (cl:cons ':covariance (covariance msg))
    (cl:cons ':angVelocity (angVelocity msg))
    (cl:cons ':thrust (thrust msg))
    (cl:cons ':flightmode (flightmode msg))
    (cl:cons ':POI (POI msg))
))
