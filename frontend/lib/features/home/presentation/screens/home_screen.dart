import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../providers/home_providers.dart';
import '../widgets/featured_recipes_section.dart';
import '../widgets/categories_section.dart';
import '../widgets/recent_recipes_section.dart';
import '../widgets/popular_recipes_section.dart';
import '../widgets/home_app_bar.dart';

class HomeScreen extends ConsumerStatefulWidget {
  const HomeScreen({super.key});

  @override
  ConsumerState<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends ConsumerState<HomeScreen> {
  final ScrollController _scrollController = ScrollController();
  bool _showSearchButton = false;

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(_onScroll);
  }

  @override
  void dispose() {
    _scrollController.removeListener(_onScroll);
    _scrollController.dispose();
    super.dispose();
  }

  void _onScroll() {
    if (_scrollController.offset > 200 && !_showSearchButton) {
      setState(() => _showSearchButton = true);
    } else if (_scrollController.offset <= 200 && _showSearchButton) {
      setState(() => _showSearchButton = false);
    }
  }

  void _showSearchDialog(BuildContext context) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => Container(
        height: MediaQuery.of(context).size.height * 0.9,
        decoration: BoxDecoration(
          color: Theme.of(context).scaffoldBackgroundColor,
          borderRadius: const BorderRadius.vertical(top: Radius.circular(20)),
        ),
        child: Column(
          children: [
            // Handle bar
            Container(
              margin: const EdgeInsets.symmetric(vertical: 12),
              width: 40,
              height: 4,
              decoration: BoxDecoration(
                color: Colors.grey[300],
                borderRadius: BorderRadius.circular(2),
              ),
            ),
            // Search header
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      autofocus: true,
                      decoration: InputDecoration(
                        hintText: 'Tìm kiếm công thức...',
                        prefixIcon: const Icon(Icons.search),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  IconButton(
                    icon: const Icon(Icons.close),
                    onPressed: () => Navigator.pop(context),
                  ),
                ],
              ),
            ),
            // Search filters
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: Wrap(
                spacing: 8,
                children: [
                  FilterChip(
                    label: const Text('Món chính'),
                    onSelected: (selected) {},
                  ),
                  FilterChip(
                    label: const Text('Dễ làm'),
                    onSelected: (selected) {},
                  ),
                  FilterChip(
                    label: const Text('< 30 phút'),
                    onSelected: (selected) {},
                  ),
                  FilterChip(
                    label: const Text('Đánh giá cao'),
                    onSelected: (selected) {},
                  ),
                ],
              ),
            ),
            const Divider(),
            // Search results placeholder
            Expanded(
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.search, size: 64, color: Colors.grey[400]),
                    const SizedBox(height: 16),
                    Text(
                      'Nhập từ khóa để tìm kiếm',
                      style: TextStyle(color: Colors.grey[600]),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _refreshData() async {
    // Invalidate all providers to refresh data
    ref.invalidate(featuredRecipesProvider);
    ref.invalidate(popularRecipesProvider);
    ref.invalidate(recentRecipesProvider);
    ref.invalidate(categoriesProvider);
    
    // Wait for data to reload
    await Future.delayed(const Duration(milliseconds: 500));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: RefreshIndicator(
        onRefresh: _refreshData,
        child: CustomScrollView(
          controller: _scrollController,
          slivers: [
          // App Bar
          const HomeAppBar(),

          // Main Content
          SliverToBoxAdapter(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Featured Recipes
                const FeaturedRecipesSection(),
                const SizedBox(height: 24),

                // Categories
                const CategoriesSection(),
                const SizedBox(height: 24),

                // Popular Recipes
                const PopularRecipesSection(),
                const SizedBox(height: 24),

                // Recent Recipes
                const RecentRecipesSection(),
                const SizedBox(height: 24),
              ],
            ),
          ),
          ],
        ),
      ),

      // Floating Search Button
      floatingActionButton: AnimatedOpacity(
        opacity: _showSearchButton ? 1.0 : 0.0,
        duration: const Duration(milliseconds: 300),
        child: FloatingActionButton.extended(
          onPressed: () {
            // TODO: Navigate to search screen
            // context.go('/search');
            _showSearchDialog(context);
          },
          icon: const Icon(Icons.search),
          label: const Text('Tìm kiếm'),
        ),
      ),
    );
  }
}
