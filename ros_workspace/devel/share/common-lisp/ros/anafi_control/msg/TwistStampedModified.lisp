; Auto-generated. Do not edit!


(cl:in-package anafi_control-msg)


;//! \htmlinclude TwistStampedModified.msg.html

(cl:defclass <TwistStampedModified> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (twist
    :reader twist
    :initarg :twist
    :type anafi_control-msg:TwistModified
    :initform (cl:make-instance 'anafi_control-msg:TwistModified)))
)

(cl:defclass TwistStampedModified (<TwistStampedModified>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <TwistStampedModified>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'TwistStampedModified)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name anafi_control-msg:<TwistStampedModified> is deprecated: use anafi_control-msg:TwistStampedModified instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <TwistStampedModified>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader anafi_control-msg:header-val is deprecated.  Use anafi_control-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'twist-val :lambda-list '(m))
(cl:defmethod twist-val ((m <TwistStampedModified>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader anafi_control-msg:twist-val is deprecated.  Use anafi_control-msg:twist instead.")
  (twist m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <TwistStampedModified>) ostream)
  "Serializes a message object of type '<TwistStampedModified>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'twist) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <TwistStampedModified>) istream)
  "Deserializes a message object of type '<TwistStampedModified>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'twist) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<TwistStampedModified>)))
  "Returns string type for a message object of type '<TwistStampedModified>"
  "anafi_control/TwistStampedModified")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'TwistStampedModified)))
  "Returns string type for a message object of type 'TwistStampedModified"
  "anafi_control/TwistStampedModified")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<TwistStampedModified>)))
  "Returns md5sum for a message object of type '<TwistStampedModified>"
  "953cf8d869ec497d6eb74723a9307a2e")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'TwistStampedModified)))
  "Returns md5sum for a message object of type 'TwistStampedModified"
  "953cf8d869ec497d6eb74723a9307a2e")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<TwistStampedModified>)))
  "Returns full string definition for message of type '<TwistStampedModified>"
  (cl:format cl:nil "Header header~%anafi_control/TwistModified twist~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: anafi_control/TwistModified~%geometry_msgs/Vector3Stamped linear~%geometry_msgs/Vector3Stamped angular~%================================================================================~%MSG: geometry_msgs/Vector3Stamped~%# This represents a Vector3 with reference coordinate frame and timestamp~%Header header~%Vector3 vector~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'TwistStampedModified)))
  "Returns full string definition for message of type 'TwistStampedModified"
  (cl:format cl:nil "Header header~%anafi_control/TwistModified twist~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: anafi_control/TwistModified~%geometry_msgs/Vector3Stamped linear~%geometry_msgs/Vector3Stamped angular~%================================================================================~%MSG: geometry_msgs/Vector3Stamped~%# This represents a Vector3 with reference coordinate frame and timestamp~%Header header~%Vector3 vector~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <TwistStampedModified>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'twist))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <TwistStampedModified>))
  "Converts a ROS message object to a list"
  (cl:list 'TwistStampedModified
    (cl:cons ':header (header msg))
    (cl:cons ':twist (twist msg))
))
