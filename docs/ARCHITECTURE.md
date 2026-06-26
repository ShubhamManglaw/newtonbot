NewtonBot v1.0 — System Architecture

Purpose

This document defines the software architecture of NewtonBot v1.0.

Its purpose is to establish clear responsibilities for each package, node, and subsystem before implementation begins.

The architecture prioritizes modularity, maintainability, and scalability over quick implementation.

⸻

Architecture Philosophy

NewtonBot follows a layered robotics software architecture.

Each layer has a single responsibility and communicates only through well-defined ROS 2 interfaces.

Core design principles:

* Single Responsibility Principle
* Loose Coupling
* High Cohesion
* Interface-Based Communication
* Modular Package Design
* Extensibility for Future Roadmap Modules

⸻

System Layers

                 NewtonBot v1.0
              Application Layer
      Mission Manager
                     │
              Control Layer
      Motion Controller
                     ▲
                     │
              Safety Layer
      Safety Monitor
                     │
              System Layer
      Status Manager
                     │
          Robot Description Layer
      URDF • TF2 • Robot State Publisher
                     │
              Visualization Layer
                  RViz

⸻

Package Responsibilities

newtonbot_interfaces

Purpose

Define all communication contracts used throughout the system.

Responsibilities

* Custom Messages
* Custom Services

Rules

* No robot logic
* No publishers
* No subscribers

⸻

newtonbot_controller

Purpose

Implement the robot’s operational behavior.

Responsibilities

* Mission execution
* Motion generation
* Safety monitoring
* Robot status management

This package contains all runtime intelligence.

⸻

newtonbot_description

Purpose

Represent the physical robot.

Responsibilities

* URDF
* Robot model
* RViz configuration
* Robot assets

Future versions will migrate to Xacro.

⸻

newtonbot_bringup

Purpose

Deploy the complete robot system.

Responsibilities

* Launch files
* Configuration
* Parameter loading

This package contains no application logic.

⸻

Node Responsibilities

Mission Manager

Purpose

Manage the robot’s mission.

Responsibilities

* Execute patrol mission
* Track mission progress
* Control mission state
* Coordinate subsystem behavior

The Mission Manager decides what the robot should do.

It does not directly control robot movement.

⸻

Motion Controller

Purpose

Generate robot motion.

Responsibilities

* Convert mission commands into velocity commands
* Publish motion commands
* Execute movement primitives

The Motion Controller decides how the robot moves.

It does not make mission decisions.

⸻

Safety Monitor

Purpose

Ensure safe robot operation.

Responsibilities

* Monitor obstacle distance
* Detect unsafe conditions
* Trigger emergency stop
* Notify Mission Manager

Safety decisions remain isolated from motion generation.

⸻

Status Manager

Purpose

Maintain system visibility.

Responsibilities

* Publish robot status
* Report mission progress
* Respond to status requests
* Aggregate system information

Status Manager never controls robot behavior.

It only reports it.

⸻

Data Ownership

Each piece of information has exactly one owner.

Information	Owner
Mission State	Mission Manager
Velocity Commands	Motion Controller
Safety State	Safety Monitor
Robot Status	Status Manager

This prevents conflicting updates and simplifies debugging.

⸻

Runtime Workflow

Robot Startup

↓

Mission Manager initializes mission

↓

Motion Controller executes movement

↓

Safety Monitor continuously observes environment

↓

Status Manager publishes system status

↓

Mission completes or safety intervention occurs

⸻

Design Principles

Separation of Responsibilities

Each node has one primary responsibility.

Mission logic must never be mixed with motion generation.

⸻

Interface-Based Communication

Nodes communicate only through ROS 2 topics, services, and parameters.

Direct dependencies between nodes should be minimized.

⸻

Scalability

Every subsystem should be replaceable without redesigning the entire architecture.

Examples:

* Replace square patrol with Navigation2
* Replace simulated sensors with real hardware
* Upgrade URDF to Xacro

The remaining system should continue functioning with minimal modification.

⸻

Future Architecture Evolution

NewtonBot is designed to evolve during the robotics roadmap.

Planned evolution:

NewtonBot v1.0

↓

Xacro Integration

↓

Robot State Publisher Enhancements

↓

Gazebo Simulation

↓

Navigation2

↓

Perception

↓

AI Integration

The architecture should support these upgrades without major restructuring.

⸻

Success Criteria

The architecture is considered successful if:

* Every package has a single responsibility.
* Every node has a clearly defined purpose.
* Communication occurs only through ROS interfaces.
* The system remains modular and extensible.
* New roadmap modules can be integrated without redesigning the project.