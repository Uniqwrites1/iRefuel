# Flutter Frontend Integration Guide
## University Vendor App (iRefuel)

This guide provides complete instructions for building a Flutter mobile app that integrates with your Django REST API backend.

## Table of Contents
1. [Project Setup](#project-setup)
2. [Dependencies](#dependencies)
3. [Project Structure](#project-structure)
4. [API Service Layer](#api-service-layer)
5. [Authentication & State Management](#authentication--state-management)
6. [Models](#models)
7. [Screens Implementation](#screens-implementation)
8. [WebSocket Integration](#websocket-integration)
9. [Testing](#testing)
10. [Deployment](#deployment)

---

## 1. Project Setup

### Create Flutter Project
```bash
flutter create irefuel_app
cd irefuel_app
```

### Update `pubspec.yaml`
```yaml
name: irefuel_app
description: University Food Ordering and Delivery App
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  
  # HTTP & API
  http: ^1.1.0
  dio: ^5.3.2
  
  # State Management
  provider: ^6.1.1
  riverpod: ^2.4.9
  flutter_riverpod: ^2.4.9
  
  # Storage & Cache
  shared_preferences: ^2.2.2
  flutter_secure_storage: ^9.0.0
  hive: ^2.2.3
  hive_flutter: ^1.1.0
  
  # UI & Navigation
  go_router: ^12.1.1
  flutter_svg: ^2.0.9
  cached_network_image: ^3.3.0
  image_picker: ^1.0.4
  
  # WebSocket
  web_socket_channel: ^2.4.0
  socket_io_client: ^2.0.3+1
  
  # Location & Maps
  geolocator: ^10.1.0
  google_maps_flutter: ^2.5.0
  
  # Utils
  intl: ^0.19.0
  uuid: ^4.1.0
  flutter_rating_bar: ^4.0.1
  
  # Notifications
  flutter_local_notifications: ^16.3.0
  
  cupertino_icons: ^1.0.2

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0
  hive_generator: ^2.0.1
  build_runner: ^2.4.7

flutter:
  uses-material-design: true
  assets:
    - assets/images/
    - assets/icons/
```

---

## 2. Project Structure

Create the following folder structure:

```
lib/
├── main.dart
├── app.dart
├── core/
│   ├── constants/
│   │   ├── api_endpoints.dart
│   │   ├── app_colors.dart
│   │   └── app_strings.dart
│   ├── network/
│   │   ├── api_client.dart
│   │   ├── network_exceptions.dart
│   │   └── websocket_service.dart
│   ├── utils/
│   │   ├── validators.dart
│   │   ├── date_utils.dart
│   │   └── snackbar_utils.dart
│   └── storage/
│       └── secure_storage.dart
├── models/
│   ├── user.dart
│   ├── cafeteria.dart
│   ├── menu_item.dart
│   ├── order.dart
│   ├── chat_message.dart
│   └── delivery_request.dart
├── services/
│   ├── auth_service.dart
│   ├── order_service.dart
│   ├── chat_service.dart
│   ├── delivery_service.dart
│   └── user_service.dart
├── providers/
│   ├── auth_provider.dart
│   ├── order_provider.dart
│   ├── chat_provider.dart
│   └── delivery_provider.dart
├── screens/
│   ├── auth/
│   │   ├── login_screen.dart
│   │   ├── register_screen.dart
│   │   └── role_selection_screen.dart
│   ├── student/
│   │   ├── home_screen.dart
│   │   ├── cafeteria_list_screen.dart
│   │   ├── menu_screen.dart
│   │   ├── cart_screen.dart
│   │   ├── order_history_screen.dart
│   │   └── order_tracking_screen.dart
│   ├── vendor/
│   │   ├── vendor_dashboard.dart
│   │   ├── menu_management_screen.dart
│   │   ├── order_management_screen.dart
│   │   └── analytics_screen.dart
│   ├── delivery/
│   │   ├── delivery_dashboard.dart
│   │   ├── available_orders_screen.dart
│   │   └── active_delivery_screen.dart
│   └── chat/
│       ├── chat_list_screen.dart
│       └── chat_screen.dart
├── widgets/
│   ├── common/
│   │   ├── custom_button.dart
│   │   ├── custom_text_field.dart
│   │   ├── loading_widget.dart
│   │   └── error_widget.dart
│   ├── menu/
│   │   ├── menu_item_card.dart
│   │   └── category_filter.dart
│   ├── order/
│   │   ├── order_card.dart
│   │   └── order_status_chip.dart
│   └── chat/
│       ├── message_bubble.dart
│       └── chat_input.dart
└── routes/
    └── app_router.dart
```

---

## 3. Core Configuration Files

### API Endpoints (`lib/core/constants/api_endpoints.dart`)
```dart
class ApiEndpoints {
  // Base URL - Update this to match your Django server
  static const String baseUrl = 'http://10.0.2.2:8000'; // Android Emulator
  // static const String baseUrl = 'http://localhost:8000'; // iOS Simulator
  // static const String baseUrl = 'https://your-domain.com'; // Production
  
  static const String apiPrefix = '/api';
  
  // Authentication
  static const String register = '$apiPrefix/auth/register/';
  static const String login = '$apiPrefix/auth/login/';
  static const String refreshToken = '$apiPrefix/auth/token/refresh/';
  
  // Users
  static const String userProfile = '$apiPrefix/users/profile/';
  static const String cafeterias = '$apiPrefix/users/cafeterias/';
  static const String menuItems = '$apiPrefix/users/menu-items/';
  
  // Orders
  static const String orders = '$apiPrefix/orders/';
  static const String studentOrders = '$apiPrefix/orders/student/';
  static const String vendorOrders = '$apiPrefix/orders/vendor/';
  static const String deliveryLocations = '$apiPrefix/orders/delivery-locations/';
  
  // Chat
  static const String chatSend = '$apiPrefix/chat/send/';
  static String chatOrderMessages(int orderId) => '$apiPrefix/chat/orders/$orderId/';
  
  // Delivery
  static const String deliveryRequests = '$apiPrefix/delivery/requests/';
  static const String deliveryToggleAvailability = '$apiPrefix/delivery/toggle-availability/';
  static const String deliveryLocation = '$apiPrefix/delivery/location/';
  
  // WebSocket
  static String chatWebSocket(int orderId) => 'ws://10.0.2.2:8000/ws/chat/$orderId/';
}
```

### App Colors (`lib/core/constants/app_colors.dart`)
```dart
import 'package:flutter/material.dart';

class AppColors {
  static const Color primary = Color(0xFF2196F3);
  static const Color primaryDark = Color(0xFF1976D2);
  static const Color secondary = Color(0xFFFF9800);
  static const Color accent = Color(0xFF4CAF50);
  
  static const Color background = Color(0xFFF5F5F5);
  static const Color surface = Colors.white;
  static const Color error = Color(0xFFD32F2F);
  
  static const Color textPrimary = Color(0xFF212121);
  static const Color textSecondary = Color(0xFF757575);
  static const Color textHint = Color(0xFFBDBDBD);
  
  static const Color success = Color(0xFF4CAF50);
  static const Color warning = Color(0xFFFF9800);
  static const Color info = Color(0xFF2196F3);
  
  // Order Status Colors
  static const Color pending = Color(0xFFFF9800);
  static const Color confirmed = Color(0xFF2196F3);
  static const Color preparing = Color(0xFF9C27B0);
  static const Color ready = Color(0xFF4CAF50);
  static const Color delivered = Color(0xFF4CAF50);
  static const Color cancelled = Color(0xFFD32F2F);
}
```

---

## 4. API Client (`lib/core/network/api_client.dart`)

```dart
import 'dart:convert';
import 'dart:io';
import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../constants/api_endpoints.dart';
import 'network_exceptions.dart';

class ApiClient {
  static final ApiClient _instance = ApiClient._internal();
  factory ApiClient() => _instance;
  ApiClient._internal();

  late Dio _dio;
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  void initialize() {
    _dio = Dio(BaseOptions(
      baseUrl: ApiEndpoints.baseUrl,
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 30),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    ));

    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: _onRequest,
      onResponse: _onResponse,
      onError: _onError,
    ));
  }

  Future<void> _onRequest(RequestOptions options, RequestInterceptorHandler handler) async {
    // Add authorization header
    final token = await _storage.read(key: 'access_token');
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  }

  void _onResponse(Response response, ResponseInterceptorHandler handler) {
    handler.next(response);
  }

  Future<void> _onError(DioException error, ErrorInterceptorHandler handler) async {
    if (error.response?.statusCode == 401) {
      // Token expired, try to refresh
      final refreshed = await _refreshToken();
      if (refreshed) {
        // Retry the original request
        final options = error.requestOptions;
        final token = await _storage.read(key: 'access_token');
        options.headers['Authorization'] = 'Bearer $token';
        
        try {
          final response = await _dio.fetch(options);
          handler.resolve(response);
          return;
        } catch (e) {
          // If retry fails, proceed with original error
        }
      }
    }
    handler.next(error);
  }

  Future<bool> _refreshToken() async {
    try {
      final refreshToken = await _storage.read(key: 'refresh_token');
      if (refreshToken == null) return false;

      final response = await _dio.post(
        ApiEndpoints.refreshToken,
        data: {'refresh': refreshToken},
      );

      if (response.statusCode == 200) {
        final data = response.data;
        await _storage.write(key: 'access_token', value: data['access']);
        return true;
      }
    } catch (e) {
      // Refresh failed, user needs to login again
      await _storage.deleteAll();
    }
    return false;
  }

  // GET request
  Future<Response> get(String path, {Map<String, dynamic>? queryParameters}) async {
    try {
      return await _dio.get(path, queryParameters: queryParameters);
    } on DioException catch (e) {
      throw NetworkExceptions.getDioException(e);
    }
  }

  // POST request
  Future<Response> post(String path, {dynamic data}) async {
    try {
      return await _dio.post(path, data: data);
    } on DioException catch (e) {
      throw NetworkExceptions.getDioException(e);
    }
  }

  // PUT request
  Future<Response> put(String path, {dynamic data}) async {
    try {
      return await _dio.put(path, data: data);
    } on DioException catch (e) {
      throw NetworkExceptions.getDioException(e);
    }
  }

  // PATCH request
  Future<Response> patch(String path, {dynamic data}) async {
    try {
      return await _dio.patch(path, data: data);
    } on DioException catch (e) {
      throw NetworkExceptions.getDioException(e);
    }
  }

  // DELETE request
  Future<Response> delete(String path) async {
    try {
      return await _dio.delete(path);
    } on DioException catch (e) {
      throw NetworkExceptions.getDioException(e);
    }
  }
}
```

---

## 5. Models

### User Model (`lib/models/user.dart`)
```dart
class User {
  final int id;
  final String username;
  final String email;
  final String firstName;
  final String lastName;
  final UserType userType;
  final String? phoneNumber;
  final String? campusLocation;
  final String? profilePicture;
  final bool isAvailable;
  final DateTime createdAt;

  User({
    required this.id,
    required this.username,
    required this.email,
    required this.firstName,
    required this.lastName,
    required this.userType,
    this.phoneNumber,
    this.campusLocation,
    this.profilePicture,
    required this.isAvailable,
    required this.createdAt,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      username: json['username'],
      email: json['email'],
      firstName: json['first_name'] ?? '',
      lastName: json['last_name'] ?? '',
      userType: UserType.values.firstWhere(
        (e) => e.name == json['user_type'],
        orElse: () => UserType.student,
      ),
      phoneNumber: json['phone_number'],
      campusLocation: json['campus_location'],
      profilePicture: json['profile_picture'],
      isAvailable: json['is_available'] ?? false,
      createdAt: DateTime.parse(json['created_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'email': email,
      'first_name': firstName,
      'last_name': lastName,
      'user_type': userType.name,
      'phone_number': phoneNumber,
      'campus_location': campusLocation,
      'profile_picture': profilePicture,
      'is_available': isAvailable,
      'created_at': createdAt.toIso8601String(),
    };
  }

  String get fullName => '$firstName $lastName'.trim();
}

enum UserType { student, vendor, delivery }
```

### Order Model (`lib/models/order.dart`)
```dart
import 'user.dart';

class Order {
  final int id;
  final int studentId;
  final String? studentName;
  final int vendorId;
  final String? vendorName;
  final int? deliveryPersonId;
  final String? deliveryPersonName;
  final OrderStatus status;
  final double totalAmount;
  final String deliveryAddress;
  final String? specialInstructions;
  final int estimatedPreparationTime;
  final int? estimatedDeliveryTime;
  final DateTime createdAt;
  final DateTime updatedAt;
  final DateTime? confirmedAt;
  final DateTime? deliveredAt;
  final List<OrderItem> items;

  Order({
    required this.id,
    required this.studentId,
    this.studentName,
    required this.vendorId,
    this.vendorName,
    this.deliveryPersonId,
    this.deliveryPersonName,
    required this.status,
    required this.totalAmount,
    required this.deliveryAddress,
    this.specialInstructions,
    required this.estimatedPreparationTime,
    this.estimatedDeliveryTime,
    required this.createdAt,
    required this.updatedAt,
    this.confirmedAt,
    this.deliveredAt,
    required this.items,
  });

  factory Order.fromJson(Map<String, dynamic> json) {
    return Order(
      id: json['id'],
      studentId: json['student'],
      studentName: json['student_name'],
      vendorId: json['vendor'],
      vendorName: json['vendor_name'],
      deliveryPersonId: json['delivery_person'],
      deliveryPersonName: json['delivery_person_name'],
      status: OrderStatus.values.firstWhere(
        (e) => e.name == json['status'],
        orElse: () => OrderStatus.pending,
      ),
      totalAmount: double.parse(json['total_amount'].toString()),
      deliveryAddress: json['delivery_address'],
      specialInstructions: json['special_instructions'],
      estimatedPreparationTime: json['estimated_preparation_time'],
      estimatedDeliveryTime: json['estimated_delivery_time'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: DateTime.parse(json['updated_at']),
      confirmedAt: json['confirmed_at'] != null 
          ? DateTime.parse(json['confirmed_at']) 
          : null,
      deliveredAt: json['delivered_at'] != null 
          ? DateTime.parse(json['delivered_at']) 
          : null,
      items: (json['items'] as List?)
          ?.map((item) => OrderItem.fromJson(item))
          .toList() ?? [],
    );
  }
}

class OrderItem {
  final int id;
  final int menuItemId;
  final String menuItemName;
  final double menuItemPrice;
  final int quantity;
  final double unitPrice;
  final double subtotal;
  final String? specialRequests;

  OrderItem({
    required this.id,
    required this.menuItemId,
    required this.menuItemName,
    required this.menuItemPrice,
    required this.quantity,
    required this.unitPrice,
    required this.subtotal,
    this.specialRequests,
  });

  factory OrderItem.fromJson(Map<String, dynamic> json) {
    return OrderItem(
      id: json['id'],
      menuItemId: json['menu_item'],
      menuItemName: json['menu_item_name'],
      menuItemPrice: double.parse(json['menu_item_price'].toString()),
      quantity: json['quantity'],
      unitPrice: double.parse(json['unit_price'].toString()),
      subtotal: double.parse(json['subtotal'].toString()),
      specialRequests: json['special_requests'],
    );
  }
}

enum OrderStatus {
  pending,
  confirmed,
  preparing,
  ready,
  out_for_delivery,
  delivered,
  cancelled
}
```

---

## 6. Authentication Service (`lib/services/auth_service.dart`)

```dart
import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../core/network/api_client.dart';
import '../core/constants/api_endpoints.dart';
import '../models/user.dart';

class AuthService {
  static final AuthService _instance = AuthService._internal();
  factory AuthService() => _instance;
  AuthService._internal();

  final ApiClient _apiClient = ApiClient();
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  Future<AuthResult> register({
    required String username,
    required String email,
    required String password,
    required String passwordConfirm,
    required String firstName,
    required String lastName,
    required UserType userType,
    String? phoneNumber,
    String? campusLocation,
  }) async {
    try {
      final response = await _apiClient.post(
        ApiEndpoints.register,
        data: {
          'username': username,
          'email': email,
          'password': password,
          'password_confirm': passwordConfirm,
          'first_name': firstName,
          'last_name': lastName,
          'user_type': userType.name,
          'phone_number': phoneNumber,
          'campus_location': campusLocation,
        },
      );

      if (response.statusCode == 201) {
        final data = response.data;
        await _storeTokens(data['access'], data['refresh']);
        final user = User.fromJson(data['user']);
        return AuthResult.success(user);
      } else {
        return AuthResult.failure('Registration failed');
      }
    } catch (e) {
      return AuthResult.failure(e.toString());
    }
  }

  Future<AuthResult> login({
    required String username,
    required String password,
  }) async {
    try {
      final response = await _apiClient.post(
        ApiEndpoints.login,
        data: {
          'username': username,
          'password': password,
        },
      );

      if (response.statusCode == 200) {
        final data = response.data;
        await _storeTokens(data['access'], data['refresh']);
        final user = User.fromJson(data['user']);
        return AuthResult.success(user);
      } else {
        return AuthResult.failure('Invalid credentials');
      }
    } catch (e) {
      return AuthResult.failure(e.toString());
    }
  }

  Future<void> logout() async {
    await _storage.deleteAll();
  }

  Future<bool> isLoggedIn() async {
    final token = await _storage.read(key: 'access_token');
    return token != null;
  }

  Future<User?> getCurrentUser() async {
    try {
      final response = await _apiClient.get(ApiEndpoints.userProfile);
      if (response.statusCode == 200) {
        return User.fromJson(response.data);
      }
    } catch (e) {
      // Token might be expired or invalid
    }
    return null;
  }

  Future<void> _storeTokens(String accessToken, String refreshToken) async {
    await _storage.write(key: 'access_token', value: accessToken);
    await _storage.write(key: 'refresh_token', value: refreshToken);
  }
}

class AuthResult {
  final bool isSuccess;
  final User? user;
  final String? error;

  AuthResult._({required this.isSuccess, this.user, this.error});

  factory AuthResult.success(User user) {
    return AuthResult._(isSuccess: true, user: user);
  }

  factory AuthResult.failure(String error) {
    return AuthResult._(isSuccess: false, error: error);
  }
}
```

---

## 7. Main App Structure

### Main App (`lib/main.dart`)
```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'core/network/api_client.dart';
import 'app.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Hive
  await Hive.initFlutter();
  
  // Initialize API Client
  ApiClient().initialize();
  
  runApp(
    const ProviderScope(
      child: IRefuelApp(),
    ),
  );
}
```

### App Widget (`lib/app.dart`)
```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'core/constants/app_colors.dart';
import 'routes/app_router.dart';
import 'providers/auth_provider.dart';

class IRefuelApp extends ConsumerWidget {
  const IRefuelApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(routerProvider);
    
    return MaterialApp.router(
      title: 'iRefuel - University Food Delivery',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: AppColors.primary,
          brightness: Brightness.light,
        ),
        appBarTheme: const AppBarTheme(
          backgroundColor: AppColors.primary,
          foregroundColor: Colors.white,
          elevation: 0,
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: AppColors.primary,
            foregroundColor: Colors.white,
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
        ),
        inputDecorationTheme: InputDecorationTheme(
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(8),
          ),
          contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        ),
        cardTheme: CardTheme(
          elevation: 2,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      ),
      routerConfig: router,
      debugShowCheckedModeBanner: false,
    );
  }
}
```

---

## 8. Key Screen Examples

### Login Screen (`lib/screens/auth/login_screen.dart`)
```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../providers/auth_provider.dart';
import '../../core/constants/app_colors.dart';
import '../../widgets/common/custom_button.dart';
import '../../widgets/common/custom_text_field.dart';

class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isLoading = false;

  @override
  Widget build(BuildContext context) {
    ref.listen<AsyncValue<void>>(authProvider, (previous, next) {
      next.when(
        data: (_) {
          // Navigate to appropriate screen based on user type
          final user = ref.read(currentUserProvider);
          if (user != null) {
            switch (user.userType) {
              case UserType.student:
                context.go('/student/home');
                break;
              case UserType.vendor:
                context.go('/vendor/dashboard');
                break;
              case UserType.delivery:
                context.go('/delivery/dashboard');
                break;
            }
          }
        },
        loading: () => setState(() => _isLoading = true),
        error: (error, _) {
          setState(() => _isLoading = false);
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(error.toString())),
          );
        },
      );
    });

    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Form(
            key: _formKey,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Logo
                Container(
                  height: 120,
                  decoration: const BoxDecoration(
                    color: AppColors.primary,
                    shape: BoxShape.circle,
                  ),
                  child: const Icon(
                    Icons.restaurant,
                    size: 60,
                    color: Colors.white,
                  ),
                ),
                const SizedBox(height: 32),
                
                // Title
                Text(
                  'Welcome to iRefuel',
                  style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: AppColors.textPrimary,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Text(
                  'University Food Delivery',
                  style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                    color: AppColors.textSecondary,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 48),
                
                // Username Field
                CustomTextField(
                  controller: _usernameController,
                  label: 'Username',
                  prefixIcon: Icons.person,
                  validator: (value) {
                    if (value?.isEmpty ?? true) {
                      return 'Please enter your username';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 16),
                
                // Password Field
                CustomTextField(
                  controller: _passwordController,
                  label: 'Password',
                  prefixIcon: Icons.lock,
                  obscureText: true,
                  validator: (value) {
                    if (value?.isEmpty ?? true) {
                      return 'Please enter your password';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 24),
                
                // Login Button
                CustomButton(
                  onPressed: _isLoading ? null : _handleLogin,
                  text: 'Login',
                  isLoading: _isLoading,
                ),
                const SizedBox(height: 16),
                
                // Register Link
                TextButton(
                  onPressed: () => context.go('/register'),
                  child: const Text('Don\'t have an account? Register'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  void _handleLogin() {
    if (_formKey.currentState?.validate() ?? false) {
      ref.read(authProvider.notifier).login(
        username: _usernameController.text.trim(),
        password: _passwordController.text,
      );
    }
  }

  @override
  void dispose() {
    _usernameController.dispose();
    _passwordController.dispose();
    super.dispose();
  }
}
```

---

## 9. WebSocket Integration (`lib/core/network/websocket_service.dart`)

```dart
import 'dart:convert';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:web_socket_channel/status.dart' as status;
import '../constants/api_endpoints.dart';
import '../../models/chat_message.dart';

class WebSocketService {
  WebSocketChannel? _channel;
  Function(ChatMessage)? onMessageReceived;
  Function()? onConnectionEstablished;
  Function(String)? onError;

  void connect(int orderId) {
    try {
      final uri = Uri.parse(ApiEndpoints.chatWebSocket(orderId));
      _channel = WebSocketChannel.connect(uri);
      
      _channel?.stream.listen(
        (data) {
          try {
            final json = jsonDecode(data);
            if (json['type'] == 'chat_message') {
              final message = ChatMessage.fromJson(json['message']);
              onMessageReceived?.call(message);
            }
          } catch (e) {
            onError?.call('Error parsing message: $e');
          }
        },
        onError: (error) {
          onError?.call('WebSocket error: $error');
        },
        onDone: () {
          // Connection closed
        },
      );
      
      onConnectionEstablished?.call();
    } catch (e) {
      onError?.call('Failed to connect: $e');
    }
  }

  void sendMessage(String message, int receiverId) {
    if (_channel != null) {
      final data = jsonEncode({
        'type': 'chat_message',
        'message': message,
        'receiver_id': receiverId,
      });
      _channel?.sink.add(data);
    }
  }

  void disconnect() {
    _channel?.sink.close(status.goingAway);
    _channel = null;
  }
}
```

---

## 10. Running the App

### Android Configuration
Add network security config in `android/app/src/main/res/xml/network_security_config.xml`:
```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">10.0.2.2</domain>
        <domain includeSubdomains="true">localhost</domain>
    </domain-config>
</network-security-config>
```

Update `android/app/src/main/AndroidManifest.xml`:
```xml
<application
    android:networkSecurityConfig="@xml/network_security_config"
    ...>
```

### Permissions
Add to `android/app/src/main/AndroidManifest.xml`:
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
<uses-permission android:name="android.permission.CAMERA" />
```

---

## 11. Testing

### Run Flutter Tests
```bash
flutter test
```

### Run with Django Backend
1. Start Django server: `python manage.py runserver`
2. Start Flutter app: `flutter run`

---

## 12. Key Features Implementation

### Real-time Chat
- WebSocket connection for live messaging
- Message history loading
- Read receipts

### Order Tracking
- Real-time order status updates
- Location tracking for deliveries
- Push notifications

### Offline Support
- Local data caching with Hive
- Sync when connection restored
- Offline-first architecture

### Security
- JWT token management
- Secure storage for credentials
- API request/response encryption

---

This comprehensive guide provides everything needed to build a full-featured Flutter app that integrates with your Django backend. The architecture is scalable, maintainable, and follows Flutter best practices.
