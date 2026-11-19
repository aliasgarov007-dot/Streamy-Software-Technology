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

# Project Overview

This repository uses Mermaid for architecture and domain documentation.

```mermaid
flowchart LR
    Client[Web Client] -->|HTTPS| API[API Gateway]
    API --> Service[Listing Service]
    Service --> DB[(Database)]
```

```mermaid
classDiagram
    direction LR
    class Order {
        +int OrderId
        +string Status
    }
    class Customer {
        +int CustomerId
        +string Name
    }
    Customer "1" --> "0..*" Order : places
```
![Architecture Diagram](./images/architecture.png)

<!--
Editable Diagram Source:
```mermaid
flowchart TD
    A[Service A] --&gt; B[Service B]
```
-->
## C4 Model: System Context

```mermaid
---
title: "Listing Service C4 Model: System Context"
---
flowchart TD
    User["Premium Member\n[Person]\n\nA user of the website who has\npurchased a subscription"]
    LS["Listings Service\n[Software System]\n\nServes web pages displaying title\nlistings to the end user"]
    TS["Title Service\n[Software System]\n\nProvides an API to retrieve\ntitle information"]
    RS["Review Service\n[Software System]\n\nProvides an API to retrieve\nand submit reviews"]
    SS["Search Service\n[Software System]\n\nProvides an API to search\nfor titles"]

    User-- "Views titles, searches titles\nand reviews titles using" -->LS
    LS-- "Retrieves title information from" -->TS
    LS-- "Retrieves from and submits reviews to" -->RS
    LS-- "Searches for titles using" -->SS

    classDef person fill:#08427b,stroke:#052e56,color:#ffffff
    classDef focusSystem fill:#1168bd,stroke:#0b4884,color:#ffffff
    classDef supportingSystem fill:#666666,stroke:#0b4884,color:#ffffff

    class User person
    class LS focusSystem
    class TS,RS,SS supportingSystem
```