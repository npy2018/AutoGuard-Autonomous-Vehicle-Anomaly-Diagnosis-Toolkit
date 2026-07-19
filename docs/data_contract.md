# Data Contract

## OTA passport

Every release must contain:

- release and previous version
- vehicle and ODD scope
- code/model/parameter/calibration changes
- immutable change ID
- old and new value
- human-readable description

## Event packet

Every diagnostic event must include:

- event and version ID
- timestamp
- scene context
- vehicle telemetry
- sensor health
- hardware health

## Replay trace

The MVP uses a compact common schema:

- timestamp
- object class and confidence
- crossing probability
- planner risk cost
- acceleration command
- optional latent signature for end-to-end comparison

Production adapters should map proprietary logs into this canonical schema without altering source evidence.
