# 🧱 Microservices Auction Platform

This project is a microservices-based auction platform built with FastAPI. It includes the following components:

- ✅ **User Service** — User registration and authentication
- 📦 **Auction Service** — Create and manage auctions
- 💰 **Bid Service** — Place and track bids
- 🛡️ **Auth Gateway** — Validate JWT tokens and route requests securely

---

## 🔧 Technologies Used

- FastAPI
- Python 3.11
- Uvicorn
- JWT (with `python-jose`)
- HTTP communication between services (no Docker used)

---

## 🧩 Microservice Architecture
<svg aria-roledescription="flowchart-v2" role="graphics-document document" viewBox="-8 -7.999998092651367 440.3541564941406 170.6666717529297" style="max-width: 440.3541564941406px;" xmlns="http://www.w3.org/2000/svg" width="100%" id="mermaid-svg-1750854171804-vf9wzrpc3"><style>#mermaid-svg-1750854171804-vf9wzrpc3{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:rgba(204, 204, 204, 0.87);}#mermaid-svg-1750854171804-vf9wzrpc3 .error-icon{fill:#bf616a;}#mermaid-svg-1750854171804-vf9wzrpc3 .error-text{fill:#bf616a;stroke:#bf616a;}#mermaid-svg-1750854171804-vf9wzrpc3 .edge-thickness-normal{stroke-width:2px;}#mermaid-svg-1750854171804-vf9wzrpc3 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-svg-1750854171804-vf9wzrpc3 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-svg-1750854171804-vf9wzrpc3 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-svg-1750854171804-vf9wzrpc3 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-svg-1750854171804-vf9wzrpc3 .marker{fill:rgba(204, 204, 204, 0.87);stroke:rgba(204, 204, 204, 0.87);}#mermaid-svg-1750854171804-vf9wzrpc3 .marker.cross{stroke:rgba(204, 204, 204, 0.87);}#mermaid-svg-1750854171804-vf9wzrpc3 svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#mermaid-svg-1750854171804-vf9wzrpc3 .label{font-family:"trebuchet ms",verdana,arial,sans-serif;color:rgba(204, 204, 204, 0.87);}#mermaid-svg-1750854171804-vf9wzrpc3 .cluster-label text{fill:#ffffff;}#mermaid-svg-1750854171804-vf9wzrpc3 .cluster-label span,#mermaid-svg-1750854171804-vf9wzrpc3 p{color:#ffffff;}#mermaid-svg-1750854171804-vf9wzrpc3 .label text,#mermaid-svg-1750854171804-vf9wzrpc3 span,#mermaid-svg-1750854171804-vf9wzrpc3 p{fill:rgba(204, 204, 204, 0.87);color:rgba(204, 204, 204, 0.87);}#mermaid-svg-1750854171804-vf9wzrpc3 .node rect,#mermaid-svg-1750854171804-vf9wzrpc3 .node circle,#mermaid-svg-1750854171804-vf9wzrpc3 .node ellipse,#mermaid-svg-1750854171804-vf9wzrpc3 .node polygon,#mermaid-svg-1750854171804-vf9wzrpc3 .node path{fill:#1a1a1a;stroke:#2a2a2a;stroke-width:1px;}#mermaid-svg-1750854171804-vf9wzrpc3 .flowchart-label text{text-anchor:middle;}#mermaid-svg-1750854171804-vf9wzrpc3 .node .label{text-align:center;}#mermaid-svg-1750854171804-vf9wzrpc3 .node.clickable{cursor:pointer;}#mermaid-svg-1750854171804-vf9wzrpc3 .arrowheadPath{fill:#e5e5e5;}#mermaid-svg-1750854171804-vf9wzrpc3 .edgePath .path{stroke:rgba(204, 204, 204, 0.87);stroke-width:2.0px;}#mermaid-svg-1750854171804-vf9wzrpc3 .flowchart-link{stroke:rgba(204, 204, 204, 0.87);fill:none;}#mermaid-svg-1750854171804-vf9wzrpc3 .edgeLabel{background-color:#1a1a1a99;text-align:center;}#mermaid-svg-1750854171804-vf9wzrpc3 .edgeLabel rect{opacity:0.5;background-color:#1a1a1a99;fill:#1a1a1a99;}#mermaid-svg-1750854171804-vf9wzrpc3 .labelBkg{background-color:rgba(26, 26, 26, 0.5);}#mermaid-svg-1750854171804-vf9wzrpc3 .cluster rect{fill:rgba(64, 64, 64, 0.47);stroke:#30373a;stroke-width:1px;}#mermaid-svg-1750854171804-vf9wzrpc3 .cluster text{fill:#ffffff;}#mermaid-svg-1750854171804-vf9wzrpc3 .cluster span,#mermaid-svg-1750854171804-vf9wzrpc3 p{color:#ffffff;}#mermaid-svg-1750854171804-vf9wzrpc3 div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:12px;background:#88c0d0;border:1px solid #30373a;border-radius:2px;pointer-events:none;z-index:100;}#mermaid-svg-1750854171804-vf9wzrpc3 .flowchartTitleText{text-anchor:middle;font-size:18px;fill:rgba(204, 204, 204, 0.87);}#mermaid-svg-1750854171804-vf9wzrpc3 :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}</style><g><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="6" viewBox="0 0 10 10" class="marker flowchart" id="mermaid-svg-1750854171804-vf9wzrpc3_flowchart-pointEnd"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 0 L 10 5 L 0 10 z"/></marker><marker orient="auto" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="4.5" viewBox="0 0 10 10" class="marker flowchart" id="mermaid-svg-1750854171804-vf9wzrpc3_flowchart-pointStart"><path style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 0 5 L 10 10 L 10 0 z"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="11" viewBox="0 0 10 10" class="marker flowchart" id="mermaid-svg-1750854171804-vf9wzrpc3_flowchart-circleEnd"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5" refX="-1" viewBox="0 0 10 10" class="marker flowchart" id="mermaid-svg-1750854171804-vf9wzrpc3_flowchart-circleStart"><circle style="stroke-width: 1; stroke-dasharray: 1, 0;" class="arrowMarkerPath" r="5" cy="5" cx="5"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="12" viewBox="0 0 11 11" class="marker cross flowchart" id="mermaid-svg-1750854171804-vf9wzrpc3_flowchart-crossEnd"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><marker orient="auto" markerHeight="11" markerWidth="11" markerUnits="userSpaceOnUse" refY="5.2" refX="-1" viewBox="0 0 11 11" class="marker cross flowchart" id="mermaid-svg-1750854171804-vf9wzrpc3_flowchart-crossStart"><path style="stroke-width: 2; stroke-dasharray: 1, 0;" class="arrowMarkerPath" d="M 1,1 l 9,9 M 10,1 l -9,9"/></marker><g class="root"><g class="clusters"/><g class="edgePaths"><path marker-end="url(#mermaid-svg-1750854171804-vf9wzrpc3_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-AGW LE-US" id="L-AGW-US-0" d="M158.438,44.135L140.641,49.668C122.844,55.201,87.25,66.267,69.453,75.084C51.656,83.9,51.656,90.467,51.656,93.75L51.656,97.033"/><path marker-end="url(#mermaid-svg-1750854171804-vf9wzrpc3_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-AGW LE-AS" id="L-AGW-AS-0" d="M216.234,52.333L216.234,56.5C216.234,60.667,216.234,69,216.234,76.45C216.234,83.9,216.234,90.467,216.234,93.75L216.234,97.033"/><path marker-end="url(#mermaid-svg-1750854171804-vf9wzrpc3_flowchart-pointEnd)" style="fill:none;" class="edge-thickness-normal edge-pattern-solid flowchart-link LS-AGW LE-BS" id="L-AGW-BS-0" d="M274.031,44.59L291.152,50.047C308.273,55.504,342.514,66.419,359.635,75.159C376.755,83.9,376.755,90.467,376.755,93.75L376.755,97.033"/></g><g class="edgeLabels"><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g><g class="edgeLabel"><g transform="translate(0, 0)" class="label"><foreignObject height="0" width="0"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="edgeLabel"></span></div></foreignObject></g></g></g><g class="nodes"><g transform="translate(216.234375, 26.16666603088379)" id="flowchart-AGW-28" class="node default default flowchart-label"><rect height="52.333335876464844" width="115.59375" y="-26.166667938232422" x="-57.796875" ry="0" rx="0" style="stroke-width:2px;" class="basic label-container"/><g transform="translate(-50.296875, -18.666667938232422)" style="" class="label"><rect/><foreignObject height="37.333335876464844" width="100.59375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Auth Gateway<br />(port 8000)</span></div></foreignObject></g></g><g transform="translate(51.65625, 128.49999809265137)" id="flowchart-US-29" class="node default default flowchart-label"><rect height="52.333335876464844" width="103.3125" y="-26.166667938232422" x="-51.65625" ry="0" rx="0" style="stroke-width:2px;" class="basic label-container"/><g transform="translate(-44.15625, -18.666667938232422)" style="" class="label"><rect/><foreignObject height="37.333335876464844" width="88.3125"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">User Service<br />(port 5000)</span></div></foreignObject></g></g><g transform="translate(216.234375, 128.49999809265137)" id="flowchart-AS-30" class="node default default flowchart-label"><rect height="52.333335876464844" width="125.84375" y="-26.166667938232422" x="-62.921875" ry="0" rx="0" style="stroke-width:2px;" class="basic label-container"/><g transform="translate(-55.421875, -18.666667938232422)" style="" class="label"><rect/><foreignObject height="37.333335876464844" width="110.84375"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Auction Service<br />(port 5001)</span></div></foreignObject></g></g><g transform="translate(376.7552070617676, 128.49999809265137)" id="flowchart-BS-31" class="node default default flowchart-label"><rect height="52.333335876464844" width="95.19792175292969" y="-26.166667938232422" x="-47.598960876464844" ry="0" rx="0" style="stroke-width:2px;" class="basic label-container"/><g transform="translate(-40.098960876464844, -18.666667938232422)" style="" class="label"><rect/><foreignObject height="37.333335876464844" width="80.19792175292969"><div style="display: inline-block; white-space: nowrap;" xmlns="http://www.w3.org/1999/xhtml"><span class="nodeLabel">Bid Service<br />(port 5002)</span></div></foreignObject></g></g></g></g></g></svg>
---

## 🚀 How to Run

Open **four terminals** (or VSCode terminals) and start each service:

```bash
# 1. User Service
cd user-service
uvicorn main:app --reload --port 5000

# 2. Auction Service
cd auction-service
uvicorn main:app --reload --port 5001

# 3. Bid Service
cd bid-service
uvicorn main:app --reload --port 5002

# 4. Auth Gateway
cd auth-gateway
uvicorn main:app --reload --port 8000

## 🔐 JWT Token Generation

Use the helper script to generate a token:

```bash
cd auth-gateway
python generate_token.py

Copy the token and include it in your requests:
Authorization: Bearer <your_token>
