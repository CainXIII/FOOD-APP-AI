import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../features/auth/presentation/providers/auth_notifier.dart';
import '../../features/auth/presentation/providers/auth_providers.dart';
import '../../features/auth/presentation/providers/auth_state.dart';
import '../../features/auth/presentation/screens/login_screen.dart';
import '../../features/auth/presentation/screens/register_screen.dart';
import '../../features/home/presentation/screens/home_screen.dart';
import '../../features/chat/presentation/screens/chat_screen.dart';
import '../../features/chat/presentation/screens/chat_history_screen.dart';
import '../../features/recipe/presentation/screens/recipe_detail_screen.dart';

/// Router refresh stream - notifies GoRouter when to refresh
class RouterRefreshStream extends ChangeNotifier {
  RouterRefreshStream(Ref ref) {
    // Listen to auth state changes
    ref.listen<AuthState>(
      authNotifierProvider,
      (previous, next) {
        if (previous?.isAuthenticated != next.isAuthenticated) {
          notifyListeners();
        }
      },
    );
  }
}

/// Go Router configuration
final goRouterProvider = Provider<GoRouter>((ref) {
  // CRITICAL: DO NOT use ref.watch() on auth providers here!
  // Using ref.watch() creates dependency and rebuilds router on every auth state change
  // This causes unwanted redirects during error states
  // Use ref.read() inside redirect callback instead

  return GoRouter(
    initialLocation: '/',
    // DISABLED RouterRefreshStream - navigation is now purely manual in success dialogs
    // This prevents unwanted redirects on error states
    // refreshListenable: RouterRefreshStream(ref),
    redirect: (context, state) {
      final location = state.matchedLocation;
      
      // Public routes - no auth required
      final publicRoutes = ['/login', '/register'];
      if (publicRoutes.contains(location)) {
        return null; // Allow access to auth screens without checking auth
      }

      // Protected routes - require authentication
      final currentAuthState = ref.read(authNotifierProvider);
      final hasValidSession = currentAuthState.user != null && currentAuthState.isAuthenticated;
      
      if (!hasValidSession) {
        // Not authenticated, redirect to login
        return '/login';
      }

      // User is authenticated, allow access
      return null;
    },
    routes: [
      // Auth routes
      GoRoute(
        path: '/login',
        name: 'login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: '/register',
        name: 'register',
        builder: (context, state) => const RegisterScreen(),
      ),

      // Main shell with bottom navigation
      ShellRoute(
        builder: (context, state, child) {
          return MainShell(child: child);
        },
        routes: [
          GoRoute(
            path: '/',
            name: 'home',
            pageBuilder: (context, state) => NoTransitionPage(
              key: state.pageKey,
              child: const HomeScreen(),
            ),
          ),
          GoRoute(
            path: '/chat',
            name: 'chat',
            pageBuilder: (context, state) => NoTransitionPage(
              key: state.pageKey,
              child: const ChatScreen(),
            ),
          ),
          GoRoute(
            path: '/chat-history',
            name: 'chat-history',
            pageBuilder: (context, state) => NoTransitionPage(
              key: state.pageKey,
              child: const ChatHistoryScreen(),
            ),
          ),
          GoRoute(
            path: '/camera',
            name: 'camera',
            pageBuilder: (context, state) => NoTransitionPage(
              key: state.pageKey,
              child: const Scaffold(
                body: Center(
                  child: Text('Camera Screen - Coming Soon'),
                ),
              ),
            ),
          ),
          GoRoute(
            path: '/profile',
            name: 'profile',
            pageBuilder: (context, state) => NoTransitionPage(
              key: state.pageKey,
              child: const Scaffold(
                body: Center(
                  child: Text('Profile Screen - Coming Soon'),
                ),
              ),
            ),
          ),
        ],
      ),

      // Recipe detail route
      GoRoute(
        path: '/recipe/:id',
        name: 'recipe-detail',
        builder: (context, state) {
          final recipeId = state.pathParameters['id']!;
          return RecipeDetailScreen(recipeId: recipeId);
        },
      ),

      // Search route
      GoRoute(
        path: '/search',
        name: 'search',
        builder: (context, state) {
          return const Scaffold(
            appBar: null,
            body: Center(
              child: Text('Search Screen - Coming Soon'),
            ),
          );
        },
      ),

      // Categories route
      GoRoute(
        path: '/categories',
        name: 'categories',
        builder: (context, state) {
          return Scaffold(
            appBar: AppBar(title: const Text('Categories')),
            body: const Center(
              child: Text('Categories Screen - Coming Soon'),
            ),
          );
        },
      ),
    ],
    errorBuilder: (context, state) => Scaffold(
      body: Center(
        child: Text('Error: ${state.error}'),
      ),
    ),
  );
});

/// Main shell with bottom navigation
class MainShell extends StatelessWidget {
  final Widget child;

  const MainShell({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: child,
      bottomNavigationBar: const BottomNavBar(),
    );
  }
}

/// Bottom navigation bar
class BottomNavBar extends StatelessWidget {
  const BottomNavBar({super.key});

  int _getCurrentIndex(BuildContext context) {
    final location = GoRouterState.of(context).matchedLocation;
    switch (location) {
      case '/':
        return 0;
      case '/chat':
        return 2;
      case '/camera':
        return 3;
      case '/profile':
        return 4;
      default:
        return 0;
    }
  }

  void _onTap(BuildContext context, int index) {
    switch (index) {
      case 0:
        context.go('/');
        break;
      case 1:
        // Show explore bottom sheet
        _showExploreBottomSheet(context);
        break;
      case 2:
        context.go('/chat');
        break;
      case 3:
        context.go('/camera');
        break;
      case 4:
        context.go('/profile');
        break;
    }
  }

  void _showExploreBottomSheet(BuildContext context) {
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.white,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (context) => Container(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              leading: const Icon(Icons.search, size: 24),
              title: const Text('Recipes', style: TextStyle(fontSize: 16)),
              trailing: const Icon(Icons.chevron_right),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              tileColor: Colors.grey[100],
              onTap: () {
                Navigator.pop(context);
                context.go('/search');
              },
            ),
            const SizedBox(height: 8),
            ListTile(
              leading: const Icon(Icons.folder, size: 24),
              title: const Text('Categories', style: TextStyle(fontSize: 16)),
              trailing: const Icon(Icons.chevron_right),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              tileColor: Colors.grey[100],
              onTap: () {
                Navigator.pop(context);
                context.go('/categories');
              },
            ),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final currentIndex = _getCurrentIndex(context);
    final theme = Theme.of(context);

    return Container(
      decoration: BoxDecoration(
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 8,
            offset: const Offset(0, -2),
          ),
        ],
      ),
      child: BottomNavigationBar(
        currentIndex: currentIndex == 1 ? 0 : currentIndex > 1 ? currentIndex - 1 : currentIndex,
        onTap: (index) {
          final actualIndex = index >= 1 ? index + 1 : index;
          _onTap(context, actualIndex);
        },
        type: BottomNavigationBarType.fixed,
        selectedItemColor: theme.colorScheme.primary,
        unselectedItemColor: Colors.grey,
        selectedFontSize: 12,
        unselectedFontSize: 12,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.home_outlined),
            activeIcon: Icon(Icons.home),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.chat_bubble_outline),
            activeIcon: Icon(Icons.chat_bubble),
            label: 'Chat',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.camera_alt_outlined),
            activeIcon: Icon(Icons.camera_alt),
            label: 'Camera',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.person_outline),
            activeIcon: Icon(Icons.person),
            label: 'Profile',
          ),
        ],
      ),
    );
  }
}

/// Floating Explore Button (Alternative to 5th nav item)
class FloatingExploreButton extends StatelessWidget {
  const FloatingExploreButton({super.key});

  @override
  Widget build(BuildContext context) {
    return FloatingActionButton(
      onPressed: () {
        showModalBottomSheet(
          context: context,
          backgroundColor: Colors.white,
          shape: const RoundedRectangleBorder(
            borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
          ),
          builder: (context) => Container(
            padding: const EdgeInsets.all(20),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                ListTile(
                  leading: const Icon(Icons.search, size: 24),
                  title: const Text('Recipes'),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () {
                    Navigator.pop(context);
                    context.go('/search');
                  },
                ),
                ListTile(
                  leading: const Icon(Icons.folder, size: 24),
                  title: const Text('Categories'),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () {
                    Navigator.pop(context);
                    context.go('/categories');
                  },
                ),
              ],
            ),
          ),
        );
      },
      child: const Icon(Icons.explore),
    );
  }
}
