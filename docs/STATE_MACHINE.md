NewtonBot v1.0 — State Machine Design

Purpose

This document defines the operational behaviour of NewtonBot.

The robot behaves as a Finite State Machine (FSM), where only one state can be active at any given time.

Every subsystem reacts according to the current robot state.

The state machine is the central behavioural model of NewtonBot.

⸻

Why a State Machine?

Without a state machine:

* Robot behaviour becomes unpredictable.
* Nodes begin making conflicting decisions.
* Safety logic becomes difficult to maintain.
* Debugging becomes significantly harder.

Using a finite state machine provides:

* Predictable behaviour
* Controlled transitions
* Easier debugging
* Better scalability
* Professional robotics architecture

⸻

Design Principles

One Active State

The robot may occupy only one operational state at any given time.

⸻

Explicit Transitions

State changes must occur only through defined transition rules.

⸻

Safety Overrides Everything

Safety events always have higher priority than mission execution.

⸻

Mission Independence

The state machine manages robot behaviour.

It does not depend on the current mission implementation.

Changing the mission should not require redesigning the state machine.

⸻

State Overview

                 IDLE
                   │
           Start Mission
                   │
                   ▼
            INITIALIZING
                   │
                   ▼
            EXECUTING_MISSION
             ┌──────┴──────┐
             │             │
             ▼             ▼
     MOVING_FORWARD    TURNING
             │             │
             └──────┬──────┘
                    ▼
            CHECK_PROGRESS
             │            │
             │            │
        Continue      Mission Complete
             │            │
             ▼            ▼
      EXECUTING_MISSION  COMPLETE
Any State
    │
Obstacle Detected
    ▼
EMERGENCY_STOP
    │
Obstacle Cleared
    ▼
Resume Previous State

⸻

State Definitions

IDLE

Purpose

Default startup state.

Robot behaviour

* Waiting for commands
* Motors stopped
* No active mission

Allowed transitions

* INITIALIZING

⸻

INITIALIZING

Purpose

Prepare robot for mission execution.

Tasks

* Reset counters
* Reset timers
* Load parameters
* Verify system readiness

Allowed transitions

* EXECUTING_MISSION
* EMERGENCY_STOP

⸻

EXECUTING_MISSION

Purpose

High-level mission execution state.

Responsibilities

* Manage mission workflow
* Decide next action
* Track mission progress

Substates

* MOVING_FORWARD
* TURNING
* CHECK_PROGRESS

⸻

MOVING_FORWARD

Purpose

Move along the current patrol segment.

Entry Actions

* Generate velocity command
* Start distance tracking

Exit Conditions

* Target distance reached
* Obstacle detected

Transitions

* TURNING
* EMERGENCY_STOP

⸻

TURNING

Purpose

Rotate robot to the next heading.

Entry Actions

* Publish angular velocity
* Monitor heading

Exit Conditions

* Target angle reached
* Obstacle detected

Transitions

* CHECK_PROGRESS
* EMERGENCY_STOP

⸻

CHECK_PROGRESS

Purpose

Determine whether the mission has completed.

Checks

* Current side
* Completed turns
* Remaining loops

Transitions

Continue Mission

↓

MOVING_FORWARD

Mission Finished

↓

MISSION_COMPLETE

⸻

MISSION_COMPLETE

Purpose

Mission finished successfully.

Actions

* Stop robot
* Publish completion status
* Wait for new mission

Transitions

* IDLE

⸻

EMERGENCY_STOP

Purpose

Protect robot from unsafe conditions.

Possible Triggers

* Obstacle detected
* Manual emergency stop
* Critical fault

Actions

* Publish zero velocity
* Freeze mission
* Report emergency state

Allowed transitions

Obstacle cleared

↓

Resume previous state

Manual reset

↓

IDLE

⸻

Transition Table

Current State	Event	Next State
IDLE	Start Mission	INITIALIZING
INITIALIZING	Initialization Complete	EXECUTING_MISSION
EXECUTING_MISSION	Begin Movement	MOVING_FORWARD
MOVING_FORWARD	Target Distance Reached	TURNING
TURNING	Target Rotation Reached	CHECK_PROGRESS
CHECK_PROGRESS	Mission Continues	MOVING_FORWARD
CHECK_PROGRESS	Mission Finished	MISSION_COMPLETE
MISSION_COMPLETE	Reset	IDLE
Any State	Obstacle Detected	EMERGENCY_STOP
EMERGENCY_STOP	Obstacle Cleared	Previous State
EMERGENCY_STOP	Manual Reset	IDLE

⸻

Safety Rules

Rule 1

The robot must never continue moving after entering EMERGENCY_STOP.

⸻

Rule 2

Only Safety Monitor may trigger EMERGENCY_STOP.

⸻

Rule 3

Mission Manager controls state transitions.

No other node may modify the mission state.

⸻

Rule 4

Motion Controller executes commands.

It never decides which state should be active.

⸻

Future Expansion

The state machine has been designed for future roadmap modules.

Future versions may introduce:

* PAUSED
* LOCALIZING
* NAVIGATING
* DOCKING
* CHARGING
* MAPPING
* TELEOPERATION
* AUTONOMOUS_NAVIGATION

These additions should extend the state machine without requiring redesign of the existing states.

⸻

Success Criteria

The state machine is considered complete when:

* Every state has a single responsibility.
* Every transition is explicitly defined.
* Safety overrides all mission states.
* Only Mission Manager owns mission state.
* Motion Controller remains independent of mission logic.
* Future roadmap modules can extend the state machine without breaking existing behaviour.