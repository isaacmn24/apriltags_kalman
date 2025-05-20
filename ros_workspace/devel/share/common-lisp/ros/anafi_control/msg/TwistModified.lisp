; Auto-generated. Do not edit!


(cl:in-package anafi_control-msg)


;//! \htmlinclude TwistModified.msg.html

(cl:defclass <TwistModified> (roslisp-msg-protocol:ros-message)
  ((linear
    :reader linear
    :initarg :linear
    :type geometry_msgs-msg:Vector3Stamped
    :initform (cl:make-instance 'geometry_msgs-msg:Vector3Stamped))
   (angular
    :reader angular
    :initarg :angular
    :type geometry_msgs-msg:Vector3Stamped
    :initform (cl:make-instance 'geometry_msgs-msg:Vector3Stamped)))
)

(cl:defclass TwistModified (<TwistModified>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <TwistModified>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'TwistModified)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name anafi_control-msg:<TwistModified> is deprecated: use anafi_control-msg:TwistModified instead.")))

(cl:ensure-generic-function 'linear-val :lambda-list '(m))
(cl:defmethod linear-val ((m <TwistModified>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader anafi_control-msg:linear-val is deprecated.  Use anafi_control-msg:linear instead.")
  (linear m))

(cl:ensure-generic-function 'angular-val :lambda-list '(m))
(cl:defmethod angular-val ((m <TwistModified>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader anafi_control-msg:angular-val is deprecated.  Use anafi_control-msg:angular instead.")
  (angular m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <TwistModified>) ostream)
  "Serializes a message object of type '<TwistModified>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'linear) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'angular) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <TwistModified>) istream)
  "Deserializes a message object of type '<TwistModified>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'linear) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'angular) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<TwistModified>)))
  "Returns string type for a message object of type '<TwistModified>"
  "anafi_control/TwistModified")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'TwistModified)))
  "Returns string type for a message object of type 'TwistModified"
  "anafi_control/TwistModified")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<TwistModified>)))
  "Returns md5sum for a message object of type '<TwistModified>"
  "2d3ab5e2b924162f6809bed7c278f6b8")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'TwistModified)))
  "Returns md5sum for a message object of type 'TwistModified"
  "2d3ab5e2b924162f6809bed7c278f6b8")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<TwistModified>)))
  "Returns full string definition for message of type '<TwistModified>"
  (cl:format cl:nil "geometry_msgs/Vector3Stamped linear~%geometry_msgs/Vector3Stamped angular~%================================================================================~%MSG: geometry_msgs/Vector3Stamped~%# This represents a Vector3 with reference coordinate frame and timestamp~%Header header~%Vector3 vector~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'TwistModified)))
  "Returns full string definition for message of type 'TwistModified"
  (cl:format cl:nil "geometry_msgs/Vector3Stamped linear~%geometry_msgs/Vector3Stamped angular~%================================================================================~%MSG: geometry_msgs/Vector3Stamped~%# This represents a Vector3 with reference coordinate frame and timestamp~%Header header~%Vector3 vector~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <TwistModified>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'linear))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'angular))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <TwistModified>))
  "Converts a ROS message object to a list"
  (cl:list 'TwistModified
    (cl:cons ':linear (linear msg))
    (cl:cons ':angular (angular msg))
))
