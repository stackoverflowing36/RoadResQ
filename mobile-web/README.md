# RoadResQ — Mobile Field Responder Web Application

This directory contains the **mobile-optimized field responder application**, built for disaster response teams, convoy drivers, and on-ground personnel operating in low or zero-connectivity environments.

## Directory Contents

| File | Description | Target Viewport |
|:---|:---|:---|
| [`index.html`](file:///c:/Users/User/OneDrive/Documents/RoadResQ/mobile-web/index.html) | Interactive mobile web application simulating on-device edge AI hazard detection, BLE peer-to-peer packet relays, offline map caching, and emergency SOS broadcast. | Mobile (360px–480px) & Desktop Simulator Frame |

## Key Features
- **Offline-First Resilience:** Functional offline caching with simulated Store-Carry-Forward BLE packet propagation.
- **Edge AI Vision Triage:** Simulated camera capture with on-device neural triage for landslide and mudslide volume estimation.
- **One-Touch SOS Broadcast:** Emergency beaconing with GPS coordinates and priority packet tagging.
- **Mobile Responsive Design:** Mobile device frame with status bar, bottom navigation, and touch-optimized controls.

## Companion Native Mobile App
For the native Flutter implementation with real BLE hardware support (`flutter_blue_plus` and SQLite local cache), see [`RoadResQ/RoadResQ/frontend/`](file:///c:/Users/User/OneDrive/Documents/RoadResQ/RoadResQ/RoadResQ/frontend/).
