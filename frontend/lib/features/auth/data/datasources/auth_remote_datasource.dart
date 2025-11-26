import 'package:dio/dio.dart';
import '../../../../core/constants/api_endpoints.dart';
import '../../../../core/errors/exceptions.dart';
import '../../../../core/network/dio_client.dart';
import '../../../../core/network/error_handler.dart';
import '../models/auth_response.dart';
import '../models/user_model.dart';

/// Auth remote data source
abstract class AuthRemoteDataSource {
  Future<AuthResponse> register({
    required String email,
    required String password,
    required String username,
    String? fullName,
  });

  Future<AuthResponse> login({
    required String email,
    required String password,
  });

  Future<UserModel> getCurrentUser();

  Future<AuthResponse> refreshToken(String refreshToken);
}

class AuthRemoteDataSourceImpl implements AuthRemoteDataSource {
  final DioClient dioClient;

  AuthRemoteDataSourceImpl(this.dioClient);

  @override
  Future<AuthResponse> register({
    required String email,
    required String password,
    required String username,
    String? fullName,
  }) async {
    try {
      final response = await dioClient.post(
        ApiEndpoints.register,
        data: {
          'email': email,
          'password': password,
          'full_name': fullName ?? username, // full_name is required by backend
          'display_name': username,
        },
      );
      
      // Check if response is successful (200-299)
      if (response.statusCode == null || response.statusCode! < 200 || response.statusCode! >= 300) {
        // Manually create DioException for error responses
        throw DioException(
          requestOptions: response.requestOptions,
          response: response,
          type: DioExceptionType.badResponse,
        );
      }
      
      return AuthResponse.fromJson(response.data);
    } on DioException catch (e) {
      throw ErrorHandler.handleDioError(e);
    }
  }

  @override
  Future<AuthResponse> login({
    required String email,
    required String password,
  }) async {
    try {
      final response = await dioClient.post(
        ApiEndpoints.login,
        data: {
          'email': email,
          'password': password,
        },
      );
      
      // Check if response is successful (200-299)
      if (response.statusCode == null || response.statusCode! < 200 || response.statusCode! >= 300) {
        // Manually create DioException for error responses
        throw DioException(
          requestOptions: response.requestOptions,
          response: response,
          type: DioExceptionType.badResponse,
        );
      }
      
      return AuthResponse.fromJson(response.data);
    } on DioException catch (e) {
      throw ErrorHandler.handleDioError(e);
    }
  }

  @override
  Future<UserModel> getCurrentUser() async {
    try {
      final response = await dioClient.get(ApiEndpoints.me);
      
      // Check if response is successful (200-299)
      if (response.statusCode == null || response.statusCode! < 200 || response.statusCode! >= 300) {
        throw DioException(
          requestOptions: response.requestOptions,
          response: response,
          type: DioExceptionType.badResponse,
        );
      }
      
      return UserModel.fromJson(response.data);
    } on DioException catch (e) {
      throw ErrorHandler.handleDioError(e);
    }
  }

  @override
  Future<AuthResponse> refreshToken(String refreshToken) async {
    try {
      final response = await dioClient.post(
        ApiEndpoints.refreshToken,
        data: {'refresh_token': refreshToken},
      );
      
      // Check if response is successful (200-299)
      if (response.statusCode == null || response.statusCode! < 200 || response.statusCode! >= 300) {
        throw DioException(
          requestOptions: response.requestOptions,
          response: response,
          type: DioExceptionType.badResponse,
        );
      }
      
      return AuthResponse.fromJson(response.data);
    } on DioException catch (e) {
      throw ErrorHandler.handleDioError(e);
    }
  }
}
