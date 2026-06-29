import rclpy
from rclpy.node import Node
from newtonbot_interfaces.msg import (MissionCommand,MotionStatus,SafetyStatus,)
from newtonbot_interfaces.srv import (StartMission,StopMission,ResetMission,)
# =====================================================
# Mission States
# =====================================================
IDLE = 0
PATROL = 1
STOPPED = 2
COMPLETE = 3
# =====================================================
# Mission Commands
# =====================================================
STOP = 0
START_PATROL = 1
class MissionManager(Node):
    """
    Mission Manager for NewtonBot.

    Responsibilities:
    - Manage mission lifecycle
    - Maintain mission state
    """
    def __init__(self):
        super().__init__("mission_manager")
        # -------------------------------------------------
        # Parameters
        # -------------------------------------------------
        self.declare_parameter("patrol_length", 2.0)
        self.declare_parameter("patrol_loops", 3)
        self.declare_parameter("mission_name", "square_patrol")
        self.patrol_length = self.get_parameter(
            "patrol_length"
        ).get_parameter_value().double_value
        self.patrol_loops = self.get_parameter(
            "patrol_loops"
        ).get_parameter_value().integer_value
        self.mission_name = self.get_parameter(
            "mission_name"
        ).get_parameter_value().string_value
        self.mission_command_publisher=self.create_publisher(
            MissionCommand,"/mission/command",10
        )
        self.motion_status_subscriber=self.create_subscription(
            MotionStatus,"/motion/status",self.motion_status_callback,10
        )
        self.safety_status_subscriber=self.create_subscription(
            SafetyStatus,"/safety/status",self.safety_status_callback,10
        )
        self.start_service=self.create_service(
            StartMission,"/mission/start",self.start_mission_callback
        )
        self.stop_service=self.create_service(
            StopMission,"/mission/stop",self.stop_mission_callback
        )
        self.reset_service=self.create_service(
            ResetMission,"/mission/reset",self.reset_mission_callback
        )
        # -------------------------------------------------
        # Timer
        # -------------------------------------------------
        self.timer = self.create_timer(
            1.0,
            self.mission_timer_callback,
        )
        # -------------------------------------------------
        # Internal State
        # -------------------------------------------------
        self.mission_state = IDLE
        self.mission_active = False
        self.current_segment = 0
        self.current_loop = 0
        # -------------------------------------------------
        # Startup Logs
        # -------------------------------------------------
        self.get_logger().info("===== Mission Manager Started =====")
        self.get_logger().info(f"Mission : {self.mission_name}")
        self.get_logger().info(f"Patrol Length : {self.patrol_length} m")
        self.get_logger().info(f"Patrol Loops : {self.patrol_loops}")
    def start_mission_callback(self,request,response):
        if self.mission_active:
            response.success=False
            response.message="Mission already running."
            return response
        self.mission_active=True
        self.mission_state=PATROL
        self.publish_mission_command(START_PATROL)
        self.get_logger().info("Mission started.")
        response.success=True
        response.message="Mission started"
        return response

    
    def stop_mission_callback(self, request, response):
        self.mission_active = False
        self.mission_state = STOPPED
        self.publish_mission_command(STOP)
        self.get_logger().info("Mission stopped.")
        response.success = True
        response.message = "Mission stopped."
        return response


    
    def reset_mission_callback(self, request, response):
        self.mission_active = False
        self.mission_state = IDLE
        self.current_segment = 0
        self.current_loop = 0
        self.get_logger().info("Mission reset.")
        response.success = True
        response.message = "Mission reset."
        return response
    
    def motion_status_callback(self,msg):
        self.get_logger().debug(f"Motion State : {msg.motion_state}")
        
    def safety_status_callback(self,msg):
        self.get_logger().debug(f"Safety Status : {msg.safety_state}")
    # =====================================================
    # Timer Callback
    # =====================================================
    def mission_timer_callback(self):
        if not self.mission_active:
            return
        self.get_logger().info(
            f"State: {self.mission_state} | "
            f"Loop: {self.current_loop} | "
            f"Segment: {self.current_segment}"
        )
        
    def publish_mission_command(self,command:int):
        msg=MissionCommand()
        msg.command=command
        msg.stamp = self.get_clock().now().to_msg()
        self.mission_command_publisher.publish(msg)
        self.get_logger().info(f"Mission Command : {command}")
        
def main(args=None):
    rclpy.init(args=args)
    node = MissionManager()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.get_logger().info("Mission Manager shutting down...")
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
if __name__ == "__main__":
    main()