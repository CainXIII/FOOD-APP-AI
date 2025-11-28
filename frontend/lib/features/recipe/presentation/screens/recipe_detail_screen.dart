import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../../../../core/theme/app_theme.dart';
import '../../domain/entities/recipe.dart';
import '../providers/recipe_providers.dart';
import '../../../home/presentation/providers/favorites_notifier.dart';
import '../widgets/recipe_info_section.dart';
import '../widgets/ingredients_section.dart';
import '../widgets/steps_section.dart';
import '../widgets/nutrition_section.dart';

class RecipeDetailScreen extends ConsumerStatefulWidget {
  final String recipeId;

  const RecipeDetailScreen({
    super.key,
    required this.recipeId,
  });

  @override
  ConsumerState<RecipeDetailScreen> createState() => _RecipeDetailScreenState();
}

class _RecipeDetailScreenState extends ConsumerState<RecipeDetailScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final recipeAsync = ref.watch(recipeDetailProvider(widget.recipeId));

    return Scaffold(
      body: recipeAsync.when(
        data: (recipe) => _buildRecipeDetail(context, recipe),
        loading: () => _buildLoading(),
        error: (error, stack) => _buildError(error),
      ),
    );
  }

  Widget _buildRecipeDetail(BuildContext context, Recipe recipe) {
    final favoritesState = ref.watch(favoritesProvider);
    final isFavorite = favoritesState.isFavorite(recipe.id);

    return CustomScrollView(
      slivers: [
        // App Bar with Image
        SliverAppBar(
          expandedHeight: 300,
          pinned: true,
          flexibleSpace: FlexibleSpaceBar(
            background: Stack(
              fit: StackFit.expand,
              children: [
                // Recipe Image
                CachedNetworkImage(
                  imageUrl: recipe.thumbnail ?? '',
                  fit: BoxFit.cover,
                  placeholder: (context, url) => Container(
                    color: Colors.grey[300],
                    child: const Center(child: CircularProgressIndicator()),
                  ),
                  errorWidget: (context, url, error) => Container(
                    color: Colors.grey[300],
                    child: const Icon(Icons.restaurant, size: 80),
                  ),
                ),
                // Gradient Overlay
                Container(
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      begin: Alignment.topCenter,
                      end: Alignment.bottomCenter,
                      colors: [
                        Colors.transparent,
                        Colors.black.withOpacity(0.7),
                      ],
                    ),
                  ),
                ),
                // Title at Bottom
                Positioned(
                  left: 16,
                  right: 16,
                  bottom: 16,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        recipe.titleVi,
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      if (recipe.titleEn != null) ...[
                        const SizedBox(height: 4),
                        Text(
                          recipe.titleEn!,
                          style: TextStyle(
                            color: Colors.white.withOpacity(0.9),
                            fontSize: 16,
                          ),
                        ),
                      ],
                    ],
                  ),
                ),
              ],
            ),
          ),
          actions: [
            // Favorite Button
            IconButton(
              icon: Icon(
                isFavorite ? Icons.favorite : Icons.favorite_border,
                color: isFavorite ? Colors.red : Colors.white,
              ),
              onPressed: () {
                ref.read(favoritesProvider.notifier).toggleFavorite(recipe.id);
              },
            ),
            // Share Button
            IconButton(
              icon: const Icon(Icons.share, color: Colors.white),
              onPressed: () {
                // TODO: Implement share
              },
            ),
          ],
        ),

        // Recipe Info Section
        SliverToBoxAdapter(
          child: RecipeInfoSection(recipe: recipe),
        ),

        // Tab Bar
        SliverPersistentHeader(
          pinned: true,
          delegate: _SliverTabBarDelegate(
            TabBar(
              controller: _tabController,
              labelColor: Theme.of(context).primaryColor,
              unselectedLabelColor: Colors.grey,
              indicatorColor: Theme.of(context).primaryColor,
              tabs: const [
                Tab(text: 'Nguyên liệu'),
                Tab(text: 'Các bước'),
                Tab(text: 'Dinh dưỡng'),
              ],
            ),
          ),
        ),

        // Tab Content
        SliverFillRemaining(
          child: TabBarView(
            controller: _tabController,
            children: [
              IngredientsSection(
                ingredients: recipe.ingredients ?? [],
                servings: recipe.servings,
              ),
              StepsSection(steps: recipe.steps ?? []),
              NutritionSection(
                nutrition: recipe.nutrition,
                servings: recipe.servings,
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildLoading() {
    return const Center(
      child: CircularProgressIndicator(),
    );
  }

  Widget _buildError(Object error) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(
              Icons.error_outline,
              size: 64,
              color: Colors.red,
            ),
            const SizedBox(height: 16),
            Text(
              'Không thể tải công thức',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 8),
            Text(
              error.toString(),
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: () {
                ref.invalidate(recipeDetailProvider(widget.recipeId));
              },
              icon: const Icon(Icons.refresh),
              label: const Text('Thử lại'),
            ),
          ],
        ),
      ),
    );
  }
}

// Custom SliverPersistentHeaderDelegate for TabBar
class _SliverTabBarDelegate extends SliverPersistentHeaderDelegate {
  final TabBar _tabBar;

  _SliverTabBarDelegate(this._tabBar);

  @override
  double get minExtent => _tabBar.preferredSize.height;
  @override
  double get maxExtent => _tabBar.preferredSize.height;

  @override
  Widget build(
      BuildContext context, double shrinkOffset, bool overlapsContent) {
    return Container(
      color: Theme.of(context).scaffoldBackgroundColor,
      child: _tabBar,
    );
  }

  @override
  bool shouldRebuild(_SliverTabBarDelegate oldDelegate) {
    return false;
  }
}
