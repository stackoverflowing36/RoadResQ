# RoadResQ Frontend (Flutter)

## Setup

This folder has the Dart source only — you still need to run `flutter create .`
inside it once (with the Flutter SDK installed locally) to generate the
platform folders (`android/`, `ios/`, etc.) before it will build:

```bash
cd frontend
flutter create . --project-name roadresq --org com.motherhacker
flutter pub get
flutter run
```

`flutter create .` will not overwrite the `lib/` or `pubspec.yaml` files
already here — it only fills in the missing platform scaffolding.

## Before you run it

1. In `lib/services/api_service.dart`, set `baseUrl` to your deployed
   backend URL (or `http://10.0.2.2:8000/api/v1` for the Android emulator
   talking to a local backend).
2. Get a Google Maps API key and add it to:
   - `android/app/src/main/AndroidManifest.xml`
   - `ios/Runner/AppDelegate.swift`
   (the standard `google_maps_flutter` setup — see its README).
3. Add Bluetooth + location permissions to the Android manifest / iOS
   Info.plist for `flutter_blue_plus` and `geolocator`.

## Structure

```
lib/
  main.dart              # app entrypoint
  theme/                 # colors & ThemeData
  models/                # Incident, RouteOption, LatLngPoint
  services/
    api_service.dart             # talks to the FastAPI backend
    offline_storage_service.dart # local SQLite cache (offline-first)
    bluetooth_service.dart       # store-carry-forward peer sync (skeleton)
  screens/
    home_screen.dart      # bottom nav shell + report FAB
    route_screen.dart     # alternate routes / navigation
    alerts_screen.dart    # incident & weather alerts feed
  widgets/
    alert_card.dart
```

## What's stubbed vs. real

- **Real**: API calls, offline SQLite cache, screen navigation, theming.
- **Stubbed (marked with `// TODO`)**: Google Map rendering with route
  polylines, camera-based incident reporting + on-device Edge AI check,
  Bluetooth GATT read/write for peer sync, destination search/picker.
