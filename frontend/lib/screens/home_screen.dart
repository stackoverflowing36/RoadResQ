import 'package:flutter/material.dart';

import 'alerts_screen.dart';
import 'route_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _index = 0;

  final _screens = const [RouteScreen(), AlertsScreen()];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('RoadResQ')),
      body: _screens[_index],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _index,
        onDestinationSelected: (i) => setState(() => _index = i),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.alt_route), label: 'Route'),
          NavigationDestination(icon: Icon(Icons.notifications_active), label: 'Alerts'),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          // TODO: open incident report flow (camera + on-device Edge AI check).
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Incident reporting flow goes here')),
          );
        },
        icon: const Icon(Icons.report),
        label: const Text('Report'),
      ),
    );
  }
}
