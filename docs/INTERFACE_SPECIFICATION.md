NewtonBot v1.0 — Interface Specification

Purpose

This document defines all custom ROS 2 interfaces used by NewtonBot.

Interfaces represent the communication contract between software components.

Before implementation, every message and service must be documented here.

This document acts as the API specification for the NewtonBot software platform.

⸻

Design Principles

Every interface should satisfy the following principles:

* Single Responsibility
* Self Descriptive
* Strongly Typed
* Reusable
* Extensible
* Independent of implementation

Interfaces should describe what is being communicated rather than how it is processed.

⸻

Message Interfaces

⸻

MissionCommand.msg

Purpose

Represents a high-level command issued by the Mission Manager.

This message tells the Motion Controller what action should be executed.

Publisher

Mission Manager

Subscriber

Motion Controller

Proposed Fields

string command
float32 target_distance
float32 target_angle
int32 mission_step
builtin_interfaces/Time timestamp

Example

command = "MOVE_FORWARD"
target_distance = 2.0
mission_step = 3

⸻

MissionProgress.msg

Purpose

Represents the current execution progress of an active mission.

Publisher

Status Manager

Subscribers

Dashboard

RViz

Monitoring tools

Proposed Fields

int32 current_side
int32 completed_loops
float32 completion_percentage
float32 elapsed_time

Example

Side 2
Loop 1
50% Complete

⸻

RobotStatus.msg

Purpose

Provides a snapshot of the robot’s operational state.

Publisher

Status Manager

Subscribers

Dashboard

RViz

Monitoring tools

Proposed Fields

string robot_state
bool mission_active
bool emergency_stop
float32 obstacle_distance
float32 linear_velocity
float32 angular_velocity
builtin_interfaces/Time timestamp

Example

State = MOVING_FORWARD
Mission Active = true
Emergency Stop = false

⸻

SafetyState.msg

Purpose

Represents the robot’s current safety condition.

Publisher

Safety Monitor

Subscribers

Mission Manager

Motion Controller

Status Manager

Proposed Fields

bool obstacle_detected
bool emergency_stop
float32 obstacle_distance
string safety_level

Example

Obstacle Detected = true
Distance = 0.35m
Safety Level = WARNING

⸻

Service Interfaces

⸻

StartMission.srv

Purpose

Request the robot to start executing a mission.

Server

Mission Manager

Request

string mission_name

Response

bool accepted
string message

⸻

StopMission.srv

Purpose

Gracefully terminate the current mission.

Server

Mission Manager

Request

Empty

Response

bool success

⸻

ResetMission.srv

Purpose

Reset mission execution and return the robot to the Idle state.

Server

Mission Manager

Request

Empty

Response

bool success

⸻

GetRobotStatus.srv

Purpose

Provide the latest robot status on demand.

Server

Status Manager

Request

Empty

Response

RobotStatus status

⸻

Topic Mapping

Topic	Message	Publisher	Subscribers
/mission_command	MissionCommand	Mission Manager	Motion Controller
/cmd_vel	geometry_msgs/Twist	Motion Controller	Robot
/robot_status	RobotStatus	Status Manager	Dashboard, RViz
/mission_progress	MissionProgress	Status Manager	Dashboard
/safety_state	SafetyState	Safety Monitor	Mission Manager, Motion Controller, Status Manager

⸻

Service Mapping

Service	Server
/start_mission	Mission Manager
/stop_mission	Mission Manager
/reset_mission	Mission Manager
/get_robot_status	Status Manager

⸻

Interface Ownership

Each interface has a single owner.

Interface	Owner
MissionCommand	Mission Manager
MissionProgress	Status Manager
RobotStatus	Status Manager
SafetyState	Safety Monitor

Only the owner is responsible for publishing or modifying the interface.

⸻

Future Extensions

The interfaces are intentionally designed to support future roadmap modules.

Future additions may include:

* Navigation Goals
* Battery Status
* Localization Status
* Camera Information
* LiDAR Diagnostics
* Docking Commands
* AI Decision Messages

These additions should extend the existing communication layer without breaking compatibility.

⸻

Success Criteria

The interface specification is considered complete when:

* Every message has a clearly defined purpose.
* Every service has a single responsibility.
* Every topic has exactly one publisher.
* Every interface has one owner.
* Interfaces remain independent of implementation details.
* Future roadmap modules can reuse or extend the existing interfaces.