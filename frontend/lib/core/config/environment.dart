/// Environment configuration for different build flavors
enum Environment {
  development,
  staging,
  production,
}

class EnvironmentConfig {
  static Environment _currentEnvironment = Environment.development;
  
  static void setEnvironment(Environment env) {
    _currentEnvironment = env;
  }
  
  static Environment get currentEnvironment => _currentEnvironment;
  
  /// Get API base URL based on current environment
  static String get apiBaseUrl {
    switch (_currentEnvironment) {
      case Environment.development:
        return 'http://localhost:8000/api/v1';
      case Environment.staging:
        return 'https://staging-api.cookingassistant.com/api/v1';
      case Environment.production:
        return 'https://api.cookingassistant.com/api/v1';
    }
  }
  
  /// Whether to enable debug logging
  static bool get isDebugMode {
    return _currentEnvironment == Environment.development;
  }
  
  /// Whether to enable analytics
  static bool get enableAnalytics {
    return _currentEnvironment == Environment.production;
  }
  
  /// Get environment name as string
  static String get environmentName {
    switch (_currentEnvironment) {
      case Environment.development:
        return 'Development';
      case Environment.staging:
        return 'Staging';
      case Environment.production:
        return 'Production';
    }
  }
}
