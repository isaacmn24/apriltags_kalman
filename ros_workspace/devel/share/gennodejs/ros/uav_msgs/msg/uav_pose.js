// Auto-generated. Do not edit!

// (in-package uav_msgs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let std_msgs = _finder('std_msgs');
let geometry_msgs = _finder('geometry_msgs');

//-----------------------------------------------------------

class uav_pose {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.position = null;
      this.velocity = null;
      this.orientation = null;
      this.covariance = null;
      this.angVelocity = null;
      this.thrust = null;
      this.flightmode = null;
      this.POI = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('position')) {
        this.position = initObj.position
      }
      else {
        this.position = new geometry_msgs.msg.Point();
      }
      if (initObj.hasOwnProperty('velocity')) {
        this.velocity = initObj.velocity
      }
      else {
        this.velocity = new geometry_msgs.msg.Point();
      }
      if (initObj.hasOwnProperty('orientation')) {
        this.orientation = initObj.orientation
      }
      else {
        this.orientation = new geometry_msgs.msg.Quaternion();
      }
      if (initObj.hasOwnProperty('covariance')) {
        this.covariance = initObj.covariance
      }
      else {
        this.covariance = new Array(100).fill(0);
      }
      if (initObj.hasOwnProperty('angVelocity')) {
        this.angVelocity = initObj.angVelocity
      }
      else {
        this.angVelocity = new geometry_msgs.msg.Point();
      }
      if (initObj.hasOwnProperty('thrust')) {
        this.thrust = initObj.thrust
      }
      else {
        this.thrust = 0.0;
      }
      if (initObj.hasOwnProperty('flightmode')) {
        this.flightmode = initObj.flightmode
      }
      else {
        this.flightmode = 0;
      }
      if (initObj.hasOwnProperty('POI')) {
        this.POI = initObj.POI
      }
      else {
        this.POI = new geometry_msgs.msg.Point();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type uav_pose
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [position]
    bufferOffset = geometry_msgs.msg.Point.serialize(obj.position, buffer, bufferOffset);
    // Serialize message field [velocity]
    bufferOffset = geometry_msgs.msg.Point.serialize(obj.velocity, buffer, bufferOffset);
    // Serialize message field [orientation]
    bufferOffset = geometry_msgs.msg.Quaternion.serialize(obj.orientation, buffer, bufferOffset);
    // Check that the constant length array field [covariance] has the right length
    if (obj.covariance.length !== 100) {
      throw new Error('Unable to serialize array field covariance - length must be 100')
    }
    // Serialize message field [covariance]
    bufferOffset = _arraySerializer.float64(obj.covariance, buffer, bufferOffset, 100);
    // Serialize message field [angVelocity]
    bufferOffset = geometry_msgs.msg.Point.serialize(obj.angVelocity, buffer, bufferOffset);
    // Serialize message field [thrust]
    bufferOffset = _serializer.float64(obj.thrust, buffer, bufferOffset);
    // Serialize message field [flightmode]
    bufferOffset = _serializer.int32(obj.flightmode, buffer, bufferOffset);
    // Serialize message field [POI]
    bufferOffset = geometry_msgs.msg.Point.serialize(obj.POI, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type uav_pose
    let len;
    let data = new uav_pose(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [position]
    data.position = geometry_msgs.msg.Point.deserialize(buffer, bufferOffset);
    // Deserialize message field [velocity]
    data.velocity = geometry_msgs.msg.Point.deserialize(buffer, bufferOffset);
    // Deserialize message field [orientation]
    data.orientation = geometry_msgs.msg.Quaternion.deserialize(buffer, bufferOffset);
    // Deserialize message field [covariance]
    data.covariance = _arrayDeserializer.float64(buffer, bufferOffset, 100)
    // Deserialize message field [angVelocity]
    data.angVelocity = geometry_msgs.msg.Point.deserialize(buffer, bufferOffset);
    // Deserialize message field [thrust]
    data.thrust = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [flightmode]
    data.flightmode = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [POI]
    data.POI = geometry_msgs.msg.Point.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    return length + 940;
  }

  static datatype() {
    // Returns string type for a message object
    return 'uav_msgs/uav_pose';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'fd14362fea18a862170f6b52a4253b6e';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # A representation of 3D position, 3D orientation and 3D velocity and in free space, composed of position and orientation.
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new uav_pose(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.position !== undefined) {
      resolved.position = geometry_msgs.msg.Point.Resolve(msg.position)
    }
    else {
      resolved.position = new geometry_msgs.msg.Point()
    }

    if (msg.velocity !== undefined) {
      resolved.velocity = geometry_msgs.msg.Point.Resolve(msg.velocity)
    }
    else {
      resolved.velocity = new geometry_msgs.msg.Point()
    }

    if (msg.orientation !== undefined) {
      resolved.orientation = geometry_msgs.msg.Quaternion.Resolve(msg.orientation)
    }
    else {
      resolved.orientation = new geometry_msgs.msg.Quaternion()
    }

    if (msg.covariance !== undefined) {
      resolved.covariance = msg.covariance;
    }
    else {
      resolved.covariance = new Array(100).fill(0)
    }

    if (msg.angVelocity !== undefined) {
      resolved.angVelocity = geometry_msgs.msg.Point.Resolve(msg.angVelocity)
    }
    else {
      resolved.angVelocity = new geometry_msgs.msg.Point()
    }

    if (msg.thrust !== undefined) {
      resolved.thrust = msg.thrust;
    }
    else {
      resolved.thrust = 0.0
    }

    if (msg.flightmode !== undefined) {
      resolved.flightmode = msg.flightmode;
    }
    else {
      resolved.flightmode = 0
    }

    if (msg.POI !== undefined) {
      resolved.POI = geometry_msgs.msg.Point.Resolve(msg.POI)
    }
    else {
      resolved.POI = new geometry_msgs.msg.Point()
    }

    return resolved;
    }
};

module.exports = uav_pose;
