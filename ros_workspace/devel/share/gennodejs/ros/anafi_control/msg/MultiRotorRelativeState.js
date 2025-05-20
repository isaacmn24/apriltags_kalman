// Auto-generated. Do not edit!

// (in-package anafi_control.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class MultiRotorRelativeState {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.rel_p_x = null;
      this.rel_p_y = null;
      this.rel_p_z = null;
      this.rel_v_x = null;
      this.rel_v_y = null;
      this.rel_v_z = null;
      this.rel_yaw = null;
      this.roll = null;
      this.pitch = null;
      this.yaw = null;
      this.v_z = null;
      this.roll_rate = null;
      this.pitch_rate = null;
      this.yaw_rate = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('rel_p_x')) {
        this.rel_p_x = initObj.rel_p_x
      }
      else {
        this.rel_p_x = 0.0;
      }
      if (initObj.hasOwnProperty('rel_p_y')) {
        this.rel_p_y = initObj.rel_p_y
      }
      else {
        this.rel_p_y = 0.0;
      }
      if (initObj.hasOwnProperty('rel_p_z')) {
        this.rel_p_z = initObj.rel_p_z
      }
      else {
        this.rel_p_z = 0.0;
      }
      if (initObj.hasOwnProperty('rel_v_x')) {
        this.rel_v_x = initObj.rel_v_x
      }
      else {
        this.rel_v_x = 0.0;
      }
      if (initObj.hasOwnProperty('rel_v_y')) {
        this.rel_v_y = initObj.rel_v_y
      }
      else {
        this.rel_v_y = 0.0;
      }
      if (initObj.hasOwnProperty('rel_v_z')) {
        this.rel_v_z = initObj.rel_v_z
      }
      else {
        this.rel_v_z = 0.0;
      }
      if (initObj.hasOwnProperty('rel_yaw')) {
        this.rel_yaw = initObj.rel_yaw
      }
      else {
        this.rel_yaw = 0.0;
      }
      if (initObj.hasOwnProperty('roll')) {
        this.roll = initObj.roll
      }
      else {
        this.roll = 0.0;
      }
      if (initObj.hasOwnProperty('pitch')) {
        this.pitch = initObj.pitch
      }
      else {
        this.pitch = 0.0;
      }
      if (initObj.hasOwnProperty('yaw')) {
        this.yaw = initObj.yaw
      }
      else {
        this.yaw = 0.0;
      }
      if (initObj.hasOwnProperty('v_z')) {
        this.v_z = initObj.v_z
      }
      else {
        this.v_z = 0.0;
      }
      if (initObj.hasOwnProperty('roll_rate')) {
        this.roll_rate = initObj.roll_rate
      }
      else {
        this.roll_rate = 0.0;
      }
      if (initObj.hasOwnProperty('pitch_rate')) {
        this.pitch_rate = initObj.pitch_rate
      }
      else {
        this.pitch_rate = 0.0;
      }
      if (initObj.hasOwnProperty('yaw_rate')) {
        this.yaw_rate = initObj.yaw_rate
      }
      else {
        this.yaw_rate = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type MultiRotorRelativeState
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [rel_p_x]
    bufferOffset = _serializer.float64(obj.rel_p_x, buffer, bufferOffset);
    // Serialize message field [rel_p_y]
    bufferOffset = _serializer.float64(obj.rel_p_y, buffer, bufferOffset);
    // Serialize message field [rel_p_z]
    bufferOffset = _serializer.float64(obj.rel_p_z, buffer, bufferOffset);
    // Serialize message field [rel_v_x]
    bufferOffset = _serializer.float64(obj.rel_v_x, buffer, bufferOffset);
    // Serialize message field [rel_v_y]
    bufferOffset = _serializer.float64(obj.rel_v_y, buffer, bufferOffset);
    // Serialize message field [rel_v_z]
    bufferOffset = _serializer.float64(obj.rel_v_z, buffer, bufferOffset);
    // Serialize message field [rel_yaw]
    bufferOffset = _serializer.float64(obj.rel_yaw, buffer, bufferOffset);
    // Serialize message field [roll]
    bufferOffset = _serializer.float64(obj.roll, buffer, bufferOffset);
    // Serialize message field [pitch]
    bufferOffset = _serializer.float64(obj.pitch, buffer, bufferOffset);
    // Serialize message field [yaw]
    bufferOffset = _serializer.float64(obj.yaw, buffer, bufferOffset);
    // Serialize message field [v_z]
    bufferOffset = _serializer.float64(obj.v_z, buffer, bufferOffset);
    // Serialize message field [roll_rate]
    bufferOffset = _serializer.float64(obj.roll_rate, buffer, bufferOffset);
    // Serialize message field [pitch_rate]
    bufferOffset = _serializer.float64(obj.pitch_rate, buffer, bufferOffset);
    // Serialize message field [yaw_rate]
    bufferOffset = _serializer.float64(obj.yaw_rate, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type MultiRotorRelativeState
    let len;
    let data = new MultiRotorRelativeState(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [rel_p_x]
    data.rel_p_x = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [rel_p_y]
    data.rel_p_y = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [rel_p_z]
    data.rel_p_z = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [rel_v_x]
    data.rel_v_x = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [rel_v_y]
    data.rel_v_y = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [rel_v_z]
    data.rel_v_z = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [rel_yaw]
    data.rel_yaw = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [roll]
    data.roll = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [pitch]
    data.pitch = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [yaw]
    data.yaw = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [v_z]
    data.v_z = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [roll_rate]
    data.roll_rate = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [pitch_rate]
    data.pitch_rate = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [yaw_rate]
    data.yaw_rate = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    return length + 112;
  }

  static datatype() {
    // Returns string type for a message object
    return 'anafi_control/MultiRotorRelativeState';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '992f417326c3849f951a20961ff27171';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    Header header
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new MultiRotorRelativeState(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.rel_p_x !== undefined) {
      resolved.rel_p_x = msg.rel_p_x;
    }
    else {
      resolved.rel_p_x = 0.0
    }

    if (msg.rel_p_y !== undefined) {
      resolved.rel_p_y = msg.rel_p_y;
    }
    else {
      resolved.rel_p_y = 0.0
    }

    if (msg.rel_p_z !== undefined) {
      resolved.rel_p_z = msg.rel_p_z;
    }
    else {
      resolved.rel_p_z = 0.0
    }

    if (msg.rel_v_x !== undefined) {
      resolved.rel_v_x = msg.rel_v_x;
    }
    else {
      resolved.rel_v_x = 0.0
    }

    if (msg.rel_v_y !== undefined) {
      resolved.rel_v_y = msg.rel_v_y;
    }
    else {
      resolved.rel_v_y = 0.0
    }

    if (msg.rel_v_z !== undefined) {
      resolved.rel_v_z = msg.rel_v_z;
    }
    else {
      resolved.rel_v_z = 0.0
    }

    if (msg.rel_yaw !== undefined) {
      resolved.rel_yaw = msg.rel_yaw;
    }
    else {
      resolved.rel_yaw = 0.0
    }

    if (msg.roll !== undefined) {
      resolved.roll = msg.roll;
    }
    else {
      resolved.roll = 0.0
    }

    if (msg.pitch !== undefined) {
      resolved.pitch = msg.pitch;
    }
    else {
      resolved.pitch = 0.0
    }

    if (msg.yaw !== undefined) {
      resolved.yaw = msg.yaw;
    }
    else {
      resolved.yaw = 0.0
    }

    if (msg.v_z !== undefined) {
      resolved.v_z = msg.v_z;
    }
    else {
      resolved.v_z = 0.0
    }

    if (msg.roll_rate !== undefined) {
      resolved.roll_rate = msg.roll_rate;
    }
    else {
      resolved.roll_rate = 0.0
    }

    if (msg.pitch_rate !== undefined) {
      resolved.pitch_rate = msg.pitch_rate;
    }
    else {
      resolved.pitch_rate = 0.0
    }

    if (msg.yaw_rate !== undefined) {
      resolved.yaw_rate = msg.yaw_rate;
    }
    else {
      resolved.yaw_rate = 0.0
    }

    return resolved;
    }
};

module.exports = MultiRotorRelativeState;
