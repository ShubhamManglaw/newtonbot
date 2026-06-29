import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from newtonbot_interfaces.msg import(MissionCommand,MotionStatus)
import time
IDLE = 0
MOVING = 1
TURNING = 2
STOPPED = 3


STOP = 0
START_PATROL = 1
class MotionController(Node):
    """
    Motion Controller for NewtonBot.

    Responsibilities:
    - Execute mission commands
    - Generate robot velocity
    - Publish motion status
    """
    def __init__(self):
        super().__init__("motion_controller")

        self.declare_parameter("linear_speed", 0.20)
        self.declare_parameter("angular_speed", 0.50)
        self.declare_parameter("publish_rate", 10.0)
        self.linear_speed = (
            self.get_parameter("linear_speed")
            .get_parameter_value()
            .double_value
        )
        self.angular_speed = (
            self.get_parameter("angular_speed")
            .get_parameter_value()
            .double_value
        )
        self.publish_rate = (
            self.get_parameter("publish_rate")
            .get_parameter_value()
            .double_value
        )

        self.cmd_vel_publisher = self.create_publisher(
            Twist,
            "/cmd_vel",
            10,
        )
        self.motion_status_publisher = self.create_publisher(
            MotionStatus,
            "/motion/status",
            10,
        )

        self.mission_command_subscriber = self.create_subscription(
            MissionCommand,
            "/mission/command",
            self.mission_command_callback,
            10,
        )

        self.timer = self.create_timer(
            1.0 / self.publish_rate,
            self.control_loop,
        )

        self.motion_state = IDLE
        self.current_command = STOP
        self.motion_start_time=None
        self.motion_duration=5.0
        self.movement_finished=False

        self.get_logger().info("===== Motion Controller Started =====")
        self.get_logger().info(
            f"Linear Speed : {self.linear_speed} m/s"
        )
        self.get_logger().info(
            f"Angular Speed : {self.angular_speed} rad/s"
        )
        self.get_logger().info(
            f"Publish Rate : {self.publish_rate} Hz"
        )
    def mission_command_callback(self, msg):
        self.current_command = msg.command
        if msg.command == START_PATROL:
                self.current_command = START_PATROL
                self.motion_state = MOVING
                self.motion_start_time = time.time()
                self.movement_finished = False
        elif msg.command == STOP:
            self.current_command = STOP
            self.motion_state = STOPPED
            self.motion_start_time = None
        self.get_logger().info(
            f"Received Mission Command: {msg.command}"
        )
    def publish_motion_status(self):
        msg = MotionStatus()
        msg.motion_state = self.motion_state
        msg.movement_finished = self.movement_finished
        msg.stamp = self.get_clock().now().to_msg()
        self.motion_status_publisher.publish(msg)
    def control_loop(self):
        if self.current_command == STOP:
            self.publish_cmd_vel(0.0, 0.0)
        elif self.current_command == START_PATROL:
            elapsed = time.time() - self.motion_start_time
            if elapsed >= self.motion_duration:
                self.publish_cmd_vel(0.0, 0.0)
                self.motion_state = STOPPED
                self.current_command = STOP
                self.movement_finished = True
                self.get_logger().info(
                    "Forward movement completed."
                )
            else:
                self.publish_cmd_vel(
                    self.linear_speed,
                    0.0
                )
        self.publish_motion_status()
    def publish_cmd_vel(self, linear: float, angular: float):
        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular
        self.cmd_vel_publisher.publish(msg)
        self.get_logger().debug(
            f"cmd_vel -> linear={linear:.2f}, angular={angular:.2f}"
        )

def main(args=None):
    rclpy.init(args=args)
    node = MotionController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
if __name__ == "__main__":
    main()