import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../../../../core/constants/app_constants.dart';
import '../../../../core/errors/exceptions.dart';
import '../models/user_model.dart';

/// Auth local data source
abstract class AuthLocalDataSource {
  Future<void> saveTokens({
    required String accessToken,
    required String refreshToken,
  });

  Future<String?> getAccessToken();

  Future<String?> getRefreshToken();

  Future<void> saveUser(UserModel user);

  Future<UserModel?> getCachedUser();

  Future<void> clearAuthData();

  Future<bool> hasToken();
}

class AuthLocalDataSourceImpl implements AuthLocalDataSource {
  final SharedPreferences prefs;

  AuthLocalDataSourceImpl(this.prefs);

  @override
  Future<void> saveTokens({
    required String accessToken,
    required String refreshToken,
  }) async {
    try {
      await prefs.setString(AppConstants.accessTokenKey, accessToken);
      await prefs.setString(AppConstants.refreshTokenKey, refreshToken);
    } catch (e) {
      throw CacheException('Failed to save tokens');
    }
  }

  @override
  Future<String?> getAccessToken() async {
    try {
      return prefs.getString(AppConstants.accessTokenKey);
    } catch (e) {
      throw CacheException('Failed to get access token');
    }
  }

  @override
  Future<String?> getRefreshToken() async {
    try {
      return prefs.getString(AppConstants.refreshTokenKey);
    } catch (e) {
      throw CacheException('Failed to get refresh token');
    }
  }

  @override
  Future<void> saveUser(UserModel user) async {
    try {
      final userJson = jsonEncode(user.toJson());
      await prefs.setString(AppConstants.userDataKey, userJson);
    } catch (e) {
      throw CacheException('Failed to save user data');
    }
  }

  @override
  Future<UserModel?> getCachedUser() async {
    try {
      final userJson = prefs.getString(AppConstants.userDataKey);
      if (userJson != null) {
        return UserModel.fromJson(jsonDecode(userJson));
      }
      return null;
    } catch (e) {
      throw CacheException('Failed to get cached user');
    }
  }

  @override
  Future<void> clearAuthData() async {
    try {
      await Future.wait([
        prefs.remove(AppConstants.accessTokenKey),
        prefs.remove(AppConstants.refreshTokenKey),
        prefs.remove(AppConstants.userDataKey),
      ]);
    } catch (e) {
      throw CacheException('Failed to clear auth data');
    }
  }

  @override
  Future<bool> hasToken() async {
    final accessToken = await getAccessToken();
    return accessToken != null && accessToken.isNotEmpty;
  }
}
