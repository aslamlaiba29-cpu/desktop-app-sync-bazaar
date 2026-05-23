```mermaid
flowchart LR
    subgraph LocalDev["Local Development"]
        direction TB
        A[Flask dev server (Werkzeug)]
        B[FlaskWebGUI (optional)]
    end

    subgraph Desktop["Desktop (Bundled)"]
        direction TB
        C[FlaskWebGUI container]
        D[Embedded Chromium UI]
    end

    subgraph Remote["Remote (GitHub)"]
        direction TB
        R[Git repository]
    end

    A -->|run| UI[http://127.0.0.1:5000]
    B -->|launch| UI
    C -->|embeds| UI
    D -->|renders| UI
    UI -->|source code| R
    R -->|clone| LocalDev
    R -->|clone| Desktop
```
```
