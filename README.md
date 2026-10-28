# Streamy Video Streaming Backend Platform

## Software Technology Course Laboratory Node
* **Student Identity:** Ali Asgarov
* **Neptun System Code:** KXVFXM
* **Course Section Reference:** GEIAL314-B2a

---

## Workspace Environment Architecture
The diagram below maps out how our development environment connects local code
authoring to remote version tracking, using a **Diagrams-as-Code** design pipeline.

```mermaid
---
title: Streamy Production Architecture Proof
---
flowchart TD
    %% Base Diagram Configurations and Properties

    UserNode["💻 Workstation Client <br> (Terminal CLI / Web Browser)"]
    LiveSandbox{"🌐 Cloud Sandbox <br> (mermaid.live)"}
    LocalIDE["⚙️ VS Code IDE <br> (Markdown Preview Extension)"]
    GitStage["📦 Local Git Index <br> (Staging Ledger)"]
    RemoteHub["☁️ GitHub Remote Cloud <br> (Streamy Repository Workspace)"]

    UserNode -- 1. Sandbox Syntax --> LiveSandbox
    LiveSandbox -- 2. Verified Block Migration --> LocalIDE
    LocalIDE -- 3. git add CLI Operations --> GitStage
    GitStage -- 4. git push Pipeline Push --> RemoteHub
```

## Lab 1 Extra Mermaid: Document Your Domain (UML Class Diagrams)

```mermaid
classDiagram
    Title -- Genre

    Title *-- Season
    Title *-- Review
    Title o-- Actor

    Season *-- Episode
```

## Streamy Application Engineering Development Lifecycle
To guarantee systematic software tracking across the implementation lifespan of
**Streamy**, our individual developer pipeline follows the structured iterative gate
review framework illustrated below.

```mermaid
---
title: Streamy Iterative SDLC Blueprint
---
flowchart TD
subgraph SpecPhase [1. Requirements Specification Block]
A[Inception Abstract Created] --> B[SRS Requirements Compiling]
end
subgraph DesignPhase [2. UML Architectural Modeling]
B --> C[Draft System Border Graphs]
C --> D[Construct Advanced Class Models]
end
subgraph ValidationGate [3. Verification Gatekeeper Loop]
D --> E{Does Architecture Match Code Specs?}
E -- No: Refactor Blueprint --> B
end
subgraph ProductionPhase [4. Python Construction Layer]
E -- Yes: Pass Gate --> F[Compile Python Class Skeletons]
F --> G[Implement Internal Class Logic]
end
E:::decisionStyle
classDef decisionStyle fill:#f9f,stroke:#333,stroke-width:2px;
```

## Lab 3 Extra: Visualize Application and User Flows (Sequence Diagrams)

```mermaid
---
title: User Sign Up Flow
---
sequenceDiagram
autonumber
actor Browser
participant Sign Up Service
participant User Service
participant Kafka
links User Service: {"Repository": "https://example.com/user-service"}
Browser->>+Sign Up Service: GET /sign_up
Sign Up Service-->>-Browser: 200 OK (HTML page)
Browser->>+Sign Up Service: POST /sign_up
Sign Up Service->>Sign Up Service: Validate input
alt invalid input
Sign Up Service-->>Browser: Error
else valid input
Sign Up Service->>+User Service: POST /users
User Service--) Kafka: User Created Event Published
Note left of Kafka: other services take action based on this event
User Service-->>-Sign Up Service: 201 Created (User)
Sign Up Service-->>-Browser: 301 Redirect (Login page)
end
```
