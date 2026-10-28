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

## Streamy Application Engineering Development Lifecycle
The project follows an iterative review process: specification, UML design, validation and Python implementation. A failed validation returns to the requirements stage. The implementation stages describe future work.

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

## Lab 3 Extra: User Sign Up Sequence
This illustrative service interaction covers numbered messages, activation lifelines, validation branches, synchronous responses and an asynchronous Kafka event. The repository menu link is an example placeholder. The sign-up service remains active through both branches and deactivates after the alternative block.

```mermaid
---
title: User Sign Up Flow
---
sequenceDiagram
    autonumber
    actor Browser
    participant Signup as Sign Up Service
    participant Users as User Service
    participant Kafka
    links Users: {"Repository": "https://example.com/user-service"}
    Browser->>+Signup: GET /sign_up
    Signup-->>-Browser: 200 OK (HTML page)
    Browser->>+Signup: POST /sign_up
    Signup->>Signup: Validate input
    alt invalid input
        Signup-->>Browser: 400 Bad Request (validation error)
    else valid input
        Signup->>+Users: POST /users
        Users--)Kafka: User Created Event Published
        Note left of Kafka: Other services take action based on this event
        Users-->>-Signup: 201 Created (User)
        Signup-->>Browser: 303 See Other (login page)
    end
    deactivate Signup
```

## Lab Deliverables
- [Project inception and enhanced UML domain model](abstract.md) — Lab 2.
- [Software requirements and C4 context](SRS.md) — Lab 4.
- [Sprint workflow, task tracing and C4 containers](sprint_architecture.md) — Lab 5.
- This README contains the Lab 1 environment and domain model plus the Lab 3 lifecycle and sequence diagram.

## Technical Clarifications
- Git stores snapshots in a commit graph. Author identity is metadata; it is not a cryptographic signature.
- Mermaid inheritance uses `--|>`; directional associations use `-->`.
- Subgraph identifiers cannot contain unquoted spaces; display labels may contain spaces.
- The sequence example uses a temporary `303` redirect after POST and balances activations across both branches.
- Mermaid links may be disabled by a renderer's security configuration.
- Lab 4's boundary example labels playback as FR-2, but its written FR-2 specifies seasons. SRS.md uses the written FR-1 through FR-5 consistently; actual video delivery stays outside the Python backend.
