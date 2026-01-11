---
description: "Shortcut: Autonomous video editing via the video-editor agent."
argument-hint: "<request> (e.g. 'Make this cinematic')"
allowed-tools: [Task]
disable-model-invocation: true
---

Spawn the `video-editor` agent to handle the following request: "$ARGUMENTS"

Ensure the agent utilizes `multimodal-understanding` for analysis and `intent-translation` for parameter mapping.
