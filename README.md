# Streamy Video Streaming Backend Platform

## Software Technology Course Laboratory Node
- **Student Identity:** Ali Asgarov
- **Neptun System Code:** KXVFXM
- **Course Section Reference:** GEIAL314-B2a
- **Instructor:** Dr. Jawad Alshboul

## Workspace Environment Architecture
The diagram maps local authoring, syntax validation and remote version control using a Diagrams-as-Code workflow.

```mermaid
---
title: Streamy Production Architecture Proof
---
flowchart TD
    UserNode["Workstation Client<br>(Terminal CLI / Web Browser)"]
    LiveSandbox{"Cloud Sandbox<br>(mermaid.live)"}
    LocalIDE["VS Code IDE<br>(Markdown Preview Extension)"]
    GitStage["Local Git Index<br>(Staging Area)"]
    RemoteHub["GitHub Remote<br>(Streamy Repository)"]
    UserNode -- 1. Sandbox Syntax --> LiveSandbox
    LiveSandbox -- 2. Verified Block Migration --> LocalIDE
    LocalIDE -- 3. git add --> GitStage
    GitStage -- 4. Commit and git push --> RemoteHub
```

## Lab 1 Extra: Domain Relationships
Association connects independently existing entities. Composition represents exclusive ownership and a dependent lifecycle. Aggregation groups independent entities.

```mermaid
classDiagram
    Title -- Genre
    Title *-- Season
    Title *-- Review
    Title o-- Actor
    Season *-- Episode
```
