# Streamy Video Streaming Backend Platform
## Project Inception and Structural System Abstract

**Author:** Ali Asgarov | **Neptun:** KXVFXM

### 1. Architectural Core Objectives
Streamy is an object-oriented backend media management catalog designed to serve as the core engine for an enterprise digital video streaming marketplace. The application tracks, structures, and processes relationships between media formats, classification taxonomies, and user metric collections.

### 2. Primary System Boundaries
The Python backend manages catalog metadata, genres, domain relationships, reviews and consumption metrics. Browser interfaces, video storage and delivery through a CDN are external. These labs specify and model the system; implementation of a working streaming service is outside their scope.

```mermaid
---
title: Streamy Application System Boundaries
---
flowchart LR
    subgraph OutsideSystemBoundary [External Infrastructure]
        UI[User Browser / Client App]
        CDN[Content Delivery Network / Video Files]
    end
    subgraph InsideSystemBoundary [Streamy Python Backend]
        Core[Media Catalog Core Engine]
        Tax[Genre Taxonomy Index]
        Calc[Business Logic & Metrics Tracker]
    end
    UI -- Requests Metadata --> Core
    Core -- Queries --> Tax
    Core -- Computes Metrics --> Calc
    UI -- Streams Video --> CDN
```

### 3. Core Structural Domain Entities
1. **Title:** The central media class holding names, release dates and shared metadata for films, short films and television series.
2. **Genre:** A classification category such as Sci-Fi, Drama or Documentary. Titles and genres form a many-to-many relationship.

## Lab 2 Extra: Enhanced Domain Model
The model adds inheritance, relationship labels, multiplicities and a clickable example link. `--|>` denotes inheritance; `-->` denotes a navigable association. The example link is a placeholder, not an implemented service.

```mermaid
---
title: Streamy Domain Model
---
classDiagram
    direction TB
    class Title {
        +string name
        +int releaseYear
    }
    link Title "https://example.com/titles" _blank
    Title "1..*" -- "1..*" Genre: is associated with
    Title "1" *-- "0..*" Season: has
    Title "1" *-- "0..*" Review: has
    Title "0..*" o-- "1..*" Actor: features
    TVShow --|> Title: specializes
    Short --|> Title: specializes
    Film --|> Title: specializes
    Viewer "0..*" --> "0..*" Title: watches
    Season "1" *-- "0..*" Review: has
    Season "1" *-- "1..*" Episode: contains
    Episode "1" *-- "0..*" Review: has
```

**Model constraints:** Only TVShow instances may own seasons; Film and Short have none. Each Review belongs to exactly one reviewed object (a Title, Season, or Episode), never all three simultaneously. Deleting an owner deletes its composed children; associated genres and aggregated actors remain independent. Title attributes and top-down direction provide spacing instead of artificial blank attributes.
