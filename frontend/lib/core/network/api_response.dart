/// Generic API Response wrapper for handling success/error states
class ApiResponse<T> {
  final T? data;
  final String? message;
  final int? statusCode;
  final bool success;

  ApiResponse({
    this.data,
    this.message,
    this.statusCode,
    required this.success,
  });

  factory ApiResponse.success(T data, {String? message, int? statusCode}) {
    return ApiResponse(
      data: data,
      message: message,
      statusCode: statusCode ?? 200,
      success: true,
    );
  }

  factory ApiResponse.error(String message, {int? statusCode}) {
    return ApiResponse(
      message: message,
      statusCode: statusCode,
      success: false,
    );
  }

  factory ApiResponse.fromJson(
    Map<String, dynamic> json,
    T Function(dynamic) fromJsonT,
  ) {
    return ApiResponse(
      data: json['data'] != null ? fromJsonT(json['data']) : null,
      message: json['message'] as String?,
      statusCode: json['status'] as int?,
      success: json['success'] as bool? ?? true,
    );
  }

  Map<String, dynamic> toJson(Object? Function(T) toJsonT) {
    return {
      'data': data != null ? toJsonT(data as T) : null,
      'message': message,
      'status': statusCode,
      'success': success,
    };
  }
}
