import 'package:dio/dio.dart';
import '../../../../core/network/dio_client.dart';

class CategoryRemoteDataSource {
  final DioClient _dioClient;

  CategoryRemoteDataSource(this._dioClient);

  /// Get all categories
  Future<List<dynamic>> getCategories() async {
    final response = await _dioClient.dio.get('/categories');

    if (response.statusCode == null || response.statusCode! < 200 || response.statusCode! >= 300) {
      throw DioException(
        requestOptions: response.requestOptions,
        response: response,
        type: DioExceptionType.badResponse,
      );
    }

    return (response.data['items'] as List?) ?? [];
  }

  /// Get category details
  Future<Map<String, dynamic>> getCategoryDetails(String categoryId) async {
    final response = await _dioClient.dio.get('/categories/$categoryId');

    if (response.statusCode == null || response.statusCode! < 200 || response.statusCode! >= 300) {
      throw DioException(
        requestOptions: response.requestOptions,
        response: response,
        type: DioExceptionType.badResponse,
      );
    }

    return response.data as Map<String, dynamic>;
  }
}
