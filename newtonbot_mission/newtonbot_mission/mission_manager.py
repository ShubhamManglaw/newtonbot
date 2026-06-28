import rclpy
from rclpy.node import Node
from newtonbot_interfaces.msg import (MissionCommand,MissionProgress,MotionStatus,SafetyStatus,)
from newtonbot_interfaces.srv import (StartMission,StopMission,ResetMission,)

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

        # -------------------------------------------------
        # Internal State
        # -------------------------------------------------

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
        self.mission_command_publisher=self.create_publisher(
            MissionCommand,"mission_command",10
        )
        self.motionstatus_subscriber=self.create_subscription(
            MotionStatus,"motion_status",self.motion_status_callback,10
        )
        self.safetyStatus_subscriber=self.create_subscription(
            SafetyStatus,"safety_status",self.safety_status_callback,10
        )
        self.start_service=self.create_service(
            StartMission,"start_mission",self.start_mission_callback
        )
        self.stop_service=self.create_service(
            StopMission,"stop_mission",self.stop_mission_callback
        )
        self.reset_service=self.create_service(
            ResetMission,"reset_mission",self.reset_mission_callback
        )
    def start_mission_callback(self,request,response):
        self.get_logger().info("Start Mission Requestion")
        response.success = True
        response.message = "Mission started."
        return response
    
    def stop_mission_callback(self,request,response):
        self.get_logger().info("Stop Mission Requestion")
        return response
    
    def reset_mission_callback(self,request,response):
        self.get_logger().info("Reset Mission Requestion")
        return response
    def motion_status_callback(self,msg):
        self.get_logger().debug(f"Motion State : {msg.motion_state}")
        
    def safety_status_callback(self,msg):
        self.get_logger().debug(f"Safety Status : {msg.safety_state}")
        
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