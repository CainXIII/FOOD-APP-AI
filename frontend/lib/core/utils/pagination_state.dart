/// Pagination state for managing paginated lists
class PaginationState<T> {
  final List<T> items;
  final int currentPage;
  final int totalPages;
  final int totalItems;
  final bool hasMore;
  final bool isLoading;
  final bool isLoadingMore;
  final String? error;

  const PaginationState({
    this.items = const [],
    this.currentPage = 1,
    this.totalPages = 1,
    this.totalItems = 0,
    this.hasMore = false,
    this.isLoading = false,
    this.isLoadingMore = false,
    this.error,
  });

  PaginationState<T> copyWith({
    List<T>? items,
    int? currentPage,
    int? totalPages,
    int? totalItems,
    bool? hasMore,
    bool? isLoading,
    bool? isLoadingMore,
    String? error,
  }) {
    return PaginationState<T>(
      items: items ?? this.items,
      currentPage: currentPage ?? this.currentPage,
      totalPages: totalPages ?? this.totalPages,
      totalItems: totalItems ?? this.totalItems,
      hasMore: hasMore ?? this.hasMore,
      isLoading: isLoading ?? this.isLoading,
      isLoadingMore: isLoadingMore ?? this.isLoadingMore,
      error: error,
    );
  }

  /// Reset to initial state
  PaginationState<T> reset() {
    return const PaginationState();
  }

  /// Set loading state
  PaginationState<T> setLoading() {
    return copyWith(isLoading: true, error: null);
  }

  /// Set loading more state
  PaginationState<T> setLoadingMore() {
    return copyWith(isLoadingMore: true, error: null);
  }

  /// Update with new page data
  PaginationState<T> updateWithData({
    required List<T> newItems,
    required int page,
    required int totalPages,
    required int totalItems,
    bool append = false,
  }) {
    return copyWith(
      items: append ? [...items, ...newItems] : newItems,
      currentPage: page,
      totalPages: totalPages,
      totalItems: totalItems,
      hasMore: page < totalPages,
      isLoading: false,
      isLoadingMore: false,
      error: null,
    );
  }

  /// Set error state
  PaginationState<T> setError(String error) {
    return copyWith(
      isLoading: false,
      isLoadingMore: false,
      error: error,
    );
  }
}
