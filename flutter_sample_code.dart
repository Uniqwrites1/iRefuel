// Sample Flutter implementation files to get you started

// lib/core/constants/api_endpoints.dart
class ApiEndpoints {
  static const String baseUrl = 'http://10.0.2.2:8000'; // Android Emulator
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
  
  // Chat
  static const String chatSend = '$apiPrefix/chat/send/';
  static String chatOrderMessages(int orderId) => '$apiPrefix/chat/orders/$orderId/';
  
  // WebSocket
  static String chatWebSocket(int orderId) => 'ws://10.0.2.2:8000/ws/chat/$orderId/';
}

// lib/models/user.dart
class User {
  final int id;
  final String username;
  final String email;
  final String firstName;
  final String lastName;
  final UserType userType;
  final String? phoneNumber;
  final String? campusLocation;
  
  User({
    required this.id,
    required this.username,
    required this.email,
    required this.firstName,
    required this.lastName,
    required this.userType,
    this.phoneNumber,
    this.campusLocation,
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
    );
  }

  String get fullName => '$firstName $lastName'.trim();
}

enum UserType { student, vendor, delivery }

// lib/services/auth_service.dart
import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;

class AuthService {
  static const FlutterSecureStorage _storage = FlutterSecureStorage();
  static const String baseUrl = 'http://10.0.2.2:8000/api';

  static Future<AuthResult> login(String username, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/login/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'username': username,
          'password': password,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
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

  static Future<void> _storeTokens(String accessToken, String refreshToken) async {
    await _storage.write(key: 'access_token', value: accessToken);
    await _storage.write(key: 'refresh_token', value: refreshToken);
  }

  static Future<String?> getAccessToken() async {
    return await _storage.read(key: 'access_token');
  }

  static Future<void> logout() async {
    await _storage.deleteAll();
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

// lib/screens/auth/login_screen.dart
import 'package:flutter/material.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isLoading = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Form(
            key: _formKey,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Logo
                Container(
                  height: 120,
                  width: 120,
                  decoration: const BoxDecoration(
                    color: Colors.blue,
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
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 48),
                
                // Username Field
                TextFormField(
                  controller: _usernameController,
                  decoration: const InputDecoration(
                    labelText: 'Username',
                    prefixIcon: Icon(Icons.person),
                    border: OutlineInputBorder(),
                  ),
                  validator: (value) {
                    if (value?.isEmpty ?? true) {
                      return 'Please enter your username';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 16),
                
                // Password Field
                TextFormField(
                  controller: _passwordController,
                  obscureText: true,
                  decoration: const InputDecoration(
                    labelText: 'Password',
                    prefixIcon: Icon(Icons.lock),
                    border: OutlineInputBorder(),
                  ),
                  validator: (value) {
                    if (value?.isEmpty ?? true) {
                      return 'Please enter your password';
                    }
                    return null;
                  },
                ),
                const SizedBox(height: 24),
                
                // Login Button
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: _isLoading ? null : _handleLogin,
                    child: _isLoading
                        ? const CircularProgressIndicator(color: Colors.white)
                        : const Text('Login'),
                  ),
                ),
                const SizedBox(height: 16),
                
                // Register Link
                TextButton(
                  onPressed: () {
                    // Navigate to register screen
                  },
                  child: const Text('Don\'t have an account? Register'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  void _handleLogin() async {
    if (_formKey.currentState?.validate() ?? false) {
      setState(() => _isLoading = true);
      
      final result = await AuthService.login(
        _usernameController.text.trim(),
        _passwordController.text,
      );

      setState(() => _isLoading = false);

      if (result.isSuccess && result.user != null) {
        // Navigate based on user type
        switch (result.user!.userType) {
          case UserType.student:
            // Navigate to student home
            break;
          case UserType.vendor:
            // Navigate to vendor dashboard
            break;
          case UserType.delivery:
            // Navigate to delivery dashboard
            break;
        }
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(result.error ?? 'Login failed')),
        );
      }
    }
  }

  @override
  void dispose() {
    _usernameController.dispose();
    _passwordController.dispose();
    super.dispose();
  }
}

// lib/main.dart
import 'package:flutter/material.dart';

void main() {
  runApp(const IRefuelApp());
}

class IRefuelApp extends StatelessWidget {
  const IRefuelApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'iRefuel - University Food Delivery',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const LoginScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}
