# Flutter Project Quick Start Commands

## Initial Setup Commands

```bash
# Create Flutter project
flutter create irefuel_app
cd irefuel_app

# Add all dependencies at once
flutter pub add http dio provider riverpod flutter_riverpod shared_preferences flutter_secure_storage hive hive_flutter go_router flutter_svg cached_network_image image_picker web_socket_channel socket_io_client geolocator google_maps_flutter intl uuid flutter_rating_bar flutter_local_notifications

# Add dev dependencies
flutter pub add --dev flutter_lints hive_generator build_runner

# Get dependencies
flutter pub get

# Generate code (if using Hive)
flutter packages pub run build_runner build
```

## Django Backend API Endpoints Reference

### Authentication Endpoints
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/token/refresh/` - Refresh JWT token

### User Management
- `GET /api/users/profile/` - Get current user profile
- `GET /api/users/cafeterias/` - List cafeterias
- `GET /api/users/menu-items/` - List menu items
- `POST /api/users/vendor/menu-items/` - Create menu item (vendor)

### Order Management
- `GET /api/orders/student/` - Student's orders
- `GET /api/orders/vendor/` - Vendor's orders
- `POST /api/orders/` - Create new order
- `PATCH /api/orders/{id}/status/` - Update order status

### Chat System
- `POST /api/chat/send/` - Send message
- `GET /api/chat/orders/{order_id}/` - Get order messages
- `WS /ws/chat/{order_id}/` - WebSocket for real-time chat

### Delivery Management
- `GET /api/delivery/requests/` - List delivery requests
- `POST /api/delivery/requests/{id}/accept/` - Accept delivery
- `POST /api/delivery/toggle-availability/` - Toggle delivery availability

## Flutter App Structure Commands

```bash
# Create directory structure
mkdir -p lib/core/constants
mkdir -p lib/core/network
mkdir -p lib/core/utils
mkdir -p lib/core/storage
mkdir -p lib/models
mkdir -p lib/services
mkdir -p lib/providers
mkdir -p lib/screens/auth
mkdir -p lib/screens/student
mkdir -p lib/screens/vendor
mkdir -p lib/screens/delivery
mkdir -p lib/screens/chat
mkdir -p lib/widgets/common
mkdir -p lib/widgets/menu
mkdir -p lib/widgets/order
mkdir -p lib/widgets/chat
mkdir -p lib/routes
mkdir -p assets/images
mkdir -p assets/icons
```

## Running Commands

```bash
# Run on Android emulator
flutter run

# Run on iOS simulator  
flutter run

# Run with specific device
flutter devices
flutter run -d <device_id>

# Build APK
flutter build apk

# Build iOS
flutter build ios

# Run tests
flutter test

# Analyze code
flutter analyze

# Format code
flutter format .
```

## Common Development Commands

```bash
# Clean build
flutter clean
flutter pub get

# Check dependencies
flutter pub deps

# Upgrade dependencies
flutter pub upgrade

# Generate code
flutter packages pub run build_runner build --delete-conflicting-outputs

# Watch for changes (code generation)
flutter packages pub run build_runner watch
```

## Network Configuration for Development

### Android Emulator
- Use `10.0.2.2:8000` to access Django running on `localhost:8000`
- Add network security config for HTTP traffic

### iOS Simulator
- Use `localhost:8000` directly
- Update Info.plist for HTTP traffic if needed

### Physical Device
- Use your computer's IP address (e.g., `192.168.1.100:8000`)
- Ensure Django ALLOWED_HOSTS includes your IP
- Make sure firewall allows connections

## Debugging Tips

```bash
# Enable Flutter inspector
flutter run --dart-define=flutter.inspector.enabled=true

# Run with verbose logging
flutter run -v

# Profile performance
flutter run --profile

# Debug network issues
flutter run --enable-network-logging

# Check Flutter doctor
flutter doctor -v
```

## Useful VS Code Extensions
- Flutter
- Dart
- Flutter Widget Inspector
- Flutter Tree
- Bracket Pair Colorizer
- Material Icon Theme

## Git Commands for Flutter

```bash
# Initial commit
git init
git add .
git commit -m "Initial Flutter project setup"

# Add .gitignore entries for Flutter
echo "# Flutter specific
*.log
*.pyc
*.swp
.DS_Store
.atom/
.buildlog/
.history
.svn/

# Flutter/Dart/Pub related
**/doc/api/
.dart_tool/
.flutter-plugins
.flutter-plugins-dependencies
.packages
.pub-cache/
.pub/
build/

# Android related
**/android/**/gradle-wrapper.jar
**/android/.gradle
**/android/captures/
**/android/gradlew
**/android/gradlew.bat
**/android/local.properties
**/android/**/GeneratedPluginRegistrant.java

# iOS/XCode related
**/ios/**/*.mode1v3
**/ios/**/*.mode2v3
**/ios/**/*.moved-aside
**/ios/**/*.pbxuser
**/ios/**/*.perspectivev3
**/ios/**/*sync/
**/ios/**/.sconsign.dblite
**/ios/**/.tags*
**/ios/**/.vagrant/
**/ios/**/DerivedData/
**/ios/**/Icon?
**/ios/**/Pods/
**/ios/**/.symlinks/
**/ios/**/profile
**/ios/**/xcuserdata
**/ios/.generated/
**/ios/Flutter/App.framework
**/ios/Flutter/Flutter.framework
**/ios/Flutter/Flutter.podspec
**/ios/Flutter/Generated.xcconfig
**/ios/Flutter/ephemeral/
**/ios/Flutter/app.flx
**/ios/Flutter/app.zip
**/ios/Flutter/flutter_assets/
**/ios/Flutter/flutter_export_environment.sh
**/ios/ServiceDefinitions.json
**/ios/Runner/GeneratedPluginRegistrant.*

# Exceptions to above rules.
!**/ios/**/default.mode1v3
!**/ios/**/default.mode2v3
!**/ios/**/default.pbxuser
!**/ios/**/default.perspectivev3
!/packages/flutter_tools/test/data/dart_dependencies_test/**/.packages" >> .gitignore
```

## Environment Variables for Flutter

Create `lib/env/env.dart`:
```dart
class Environment {
  static const String apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://10.0.2.2:8000',
  );
  
  static const bool isProduction = bool.fromEnvironment(
    'PRODUCTION',
    defaultValue: false,
  );
  
  static const String websocketUrl = String.fromEnvironment(
    'WEBSOCKET_URL',
    defaultValue: 'ws://10.0.2.2:8000/ws',
  );
}
```

Run with environment variables:
```bash
flutter run --dart-define=API_BASE_URL=https://your-api.com --dart-define=PRODUCTION=true
```
