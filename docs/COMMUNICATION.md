NewtonBot v1.0 — Communication Architecture

Purpose

This document defines how all software components within NewtonBot communicate.

The objective is to establish a predictable, maintainable and scalable communication architecture before implementation begins.

NewtonBot follows standard ROS 2 communication patterns.

* Topics for continuous data streams
* Services for synchronous requests
* Parameters for runtime configuration

Each communication channel has a single owner.

⸻

Communication Philosophy

NewtonBot follows four communication principles.

1. Single Source of Truth

Every piece of information has exactly one owner.

Example

Mission State

Owner:

Mission Manager

No other node is allowed to modify mission state.

⸻

2. Publish Only What You Own

Nodes publish only the information they are responsible for.

Example

Motion Controller

Publishes:

* Velocity Commands

Never publishes:

* Mission Status
* Safety Status

⸻

3. Interface-Based Communication

Nodes never communicate directly.

All communication occurs through ROS interfaces.

Mission Manager
      │
      ▼
Mission Topic
      │
      ▼
Motion Controller

Nodes remain independent and replaceable.

⸻

4. Loose Coupling

Every subsystem should be replaceable without affecting the rest of the system.

Examples

Replace

Square Patrol

with

Navigation2

without changing Motion Controller.

Replace

URDF

with

Xacro

without changing Mission Manager.

⸻

Communication Overview

                    Mission Manager
                           │
                  /mission_command
                           │
                           ▼
                  Motion Controller
                           │
                        /cmd_vel
                           │
                           ▼
                     Robot Platform
Safety Monitor
      │
      ├────────► /safety_state
      │
      ▼
Mission Manager
Status Manager
      │
      ├────────► /robot_status
      │
      └────────► /mission_progress

⸻

Topic Architecture

Topics are used for continuous asynchronous communication.

⸻

/mission_command

Publisher

Mission Manager

Subscribers

Motion Controller

Purpose

Send high-level robot commands.

Examples

* START_PATROL
* MOVE_FORWARD
* TURN_LEFT
* STOP
* COMPLETE

Ownership

Mission Manager

⸻

/cmd_vel

Publisher

Motion Controller

Subscribers

Robot Base

Purpose

Publish velocity commands.

Message Type

geometry_msgs/Twist

Ownership

Motion Controller

⸻

/safety_state

Publisher

Safety Monitor

Subscribers

Mission Manager

Motion Controller

Purpose

Report safety conditions.

Possible States

* SAFE
* WARNING
* OBSTACLE_DETECTED
* EMERGENCY_STOP

Ownership

Safety Monitor

⸻

/robot_status

Publisher

Status Manager

Subscribers

RViz

Dashboard

Monitoring Tools

Purpose

Provide complete robot status.

Example Data

* Current State
* Active Mission
* Robot Mode
* Safety State

Ownership

Status Manager

⸻

/mission_progress

Publisher

Status Manager

Subscribers

Dashboard

RViz

Purpose

Publish mission progress.

Example

* Current Side
* Completed Turns
* Completion Percentage
* Mission Time

Ownership

Status Manager

⸻

Service Architecture

Services are used for synchronous request-response communication.

⸻

/start_mission

Server

Mission Manager

Purpose

Begin patrol mission.

Request

Mission Type

Response

Mission Accepted

⸻

/stop_mission

Server

Mission Manager

Purpose

Stop robot gracefully.

Response

Mission Stopped

⸻

/reset_mission

Server

Mission Manager

Purpose

Reset mission state.

Response

Mission Reset

⸻

/get_robot_status

Server

Status Manager

Purpose

Return current robot information.

Example Response

* Robot State
* Mission Progress
* Safety Status
* Active Mission

⸻

Parameter Architecture

Parameters configure runtime behavior.

Parameters should never represent robot state.

Changing a parameter should modify behaviour, not internal state.

⸻

Mission Manager Parameters

Parameter	Description
patrol_length	Length of one patrol side
patrol_loops	Number of patrol loops
mission_name	Active mission

⸻

Motion Controller Parameters

Parameter	Description
linear_speed	Forward speed
angular_speed	Turning speed
turn_angle	Angle per turn

⸻

Safety Monitor Parameters

Parameter	Description
stop_distance	Minimum safe obstacle distance
warning_distance	Warning threshold

⸻

Status Manager Parameters

Parameter	Description
publish_rate	Status publishing frequency

⸻

Data Ownership

Data	Owner
Mission State	Mission Manager
Velocity Commands	Motion Controller
Safety State	Safety Monitor
Robot Status	Status Manager
Mission Progress	Status Manager

Only the owner is allowed to modify the data.

Other nodes may only subscribe.

⸻

Node Communication Matrix

Node	Publishes	Subscribes	Services
Mission Manager	/mission_command	/safety_state	start, stop, reset mission
Motion Controller	/cmd_vel	/mission_command, /safety_state	None
Safety Monitor	/safety_state	Sensor Topics	None
Status Manager	/robot_status, /mission_progress	Mission, Motion, Safety	get_robot_status

⸻

Communication Flow

Normal Mission

Mission Manager

↓

Publish Mission Command

↓

Motion Controller

↓

Publish Velocity

↓

Robot Moves

↓

Status Manager Publishes Status

⸻

Obstacle Detected

Safety Monitor

↓

Publish Emergency State

↓

Mission Manager Receives Emergency

↓

Mission State Changes

↓

Motion Controller Stops Robot

↓

Status Manager Updates Robot Status

⸻

Design Rules

The following rules must always be followed.

Rule 1

One publisher owns each topic.

⸻

Rule 2

Robot state is never duplicated.

⸻

Rule 3

Mission logic never generates velocity commands.

⸻

Rule 4

Motion Controller never decides the mission.

⸻

Rule 5

Safety decisions remain independent from motion generation.

⸻

Rule 6

Status Manager never changes robot behaviour.

It only reports system information.

⸻

Future Communication Extensions

The communication architecture is designed to support future roadmap modules.

Upcoming integrations include

* Xacro
* Robot State Publisher
* Gazebo
* Navigation2
* Camera Drivers
* LiDAR Drivers
* Perception
* AI Decision Systems

These modules should integrate by subscribing to or publishing existing interfaces whenever possible.

⸻

Success Criteria

The communication architecture is considered successful when:

* Every topic has a single publisher.
* Every node has clearly defined responsibilities.
* Robot state has one owner.
* Communication is modular and loosely coupled.
* Future modules can be integrated without redesigning the communication layer.