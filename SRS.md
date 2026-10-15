# Software Requirements Specification (SRS)
## Project Baseline: Streamy Video Streaming Core Engine

**Author:** Ali Asgarov | **Neptun:** KXVFXM | **Course:** GEIAL314-B2a

### 1. Functional Requirements (FR)
- **FR-1:** The system must maintain a media catalog searchable by Genre.
- **FR-2:** The system must support multi-season episodic indexing for TVShow entities.
- **FR-3:** The system must allow users to record numerical ratings and text reviews against media elements.
- **FR-4:** The system must track viewer consumption metrics for metadata analytics.
- **FR-5:** The system must support serialization of media-item state, including inherited subtype information.

### 2. Non-Functional Requirements (NFR)
- **NFR-1 (Runtime environment):** The application must run in Python 3.x.
- **NFR-2 (Maintainability):** Design diagrams, relationship maps and entity models must be stored as plain text and rendered inline.
- **NFR-3 (Data integrity):** Deletion must cascade through composed child entities. Independent genres and actors must survive deletion of an associated title.

### 3. Functional System Boundary Diagram
The backend processes metadata and domain operations. A client requests actual video content from external delivery infrastructure. The FR identifiers below match Section 1.

```mermaid
---
title: Streamy System Boundary & Functional Use Cases
---
flowchart LR
    ViewerActor(("External Actor:<br>Platform Viewer"))
    subgraph ExternalApp [Client Application Interface]
        UI[Web Dashboard UI]
    end
    subgraph SystemPerimeter [Streamy Core System Perimeter]
        FR1[FR-1: Browse Catalog by Genre]
        FR2[FR-2: Browse Seasons and Episodes]
        FR3[FR-3: Record Ratings and Reviews]
        FR4[FR-4: Track Consumption Metrics]
        FR5[FR-5: Serialize Media State]
    end
    CDN[External Video Delivery / CDN]
    ViewerActor --> UI
    UI -- Genre Query --> FR1
    UI -- Series Selection --> FR2
    UI -- Review Payload --> FR3
    UI -- Viewing Activity --> FR4
    FR1 -- Export Media State --> FR5
    FR2 -- Export Media State --> FR5
    UI -- Playback Request --> CDN
```

### 4. Acceptance Criteria
| Requirement | Observable completion condition |
| --- | --- |
| FR-1 | A genre query returns matching titles; a genre with no matches returns an empty collection. |
| FR-2 | A television show exposes its ordered seasons and each season's episodes. |
| FR-3 | A review stores a numeric rating and text with exactly one media owner. |
| FR-4 | A viewing event can be attributed to a viewer and a media item for later aggregation. |
| FR-5 | Serialized data preserves the media type and both shared and subtype fields. |
| NFR-1 | The implemented application runs under Python 3.x. |
| NFR-2 | Repository Markdown renders all Mermaid diagrams. |
| NFR-3 | Removing a title removes its composed descendants, while actors and genres remain. |

These are future implementation acceptance criteria, not claims that application tests have already passed. Rating bounds, persistence technology and metric retention remain design decisions for later implementation.

## Lab 4 Extra: C4 System Context
A premium member uses the Listings Service, which depends on title, review and search services. This is a conceptual service-level context view; these labs do not deploy those services.

```mermaid
---
title: "Listing Service C4 Model: System Context"
---
flowchart TD
    User["Premium Member<br>[Person]<br><br>A subscriber using the website"]
    LS["Listings Service<br>[Software System]<br><br>Serves title listing pages"]
    TS["Title Service<br>[Software System]<br><br>Provides title information through an API"]
    RS["Review Service<br>[Software System]<br><br>Retrieves and submits reviews through an API"]
    SS["Search Service<br>[Software System]<br><br>Searches for titles through an API"]
    User -- Views, searches and reviews titles using --> LS
    LS -- Retrieves title information from --> TS
    LS -- Retrieves from and submits reviews to --> RS
    LS -- Searches for titles using --> SS
    classDef person fill:#08427b,stroke:#052e56,color:#ffffff
    classDef focusSystem fill:#1168bd,stroke:#0b4884,color:#ffffff
    classDef supportingSystem fill:#666666,stroke:#0b4884,color:#ffffff
    class User person
    class LS focusSystem
    class TS,RS,SS supportingSystem
```
