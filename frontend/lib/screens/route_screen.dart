import 'package:flutter/material.dart';

import '../models/route_model.dart';
import '../services/api_service.dart';
import '../theme/app_theme.dart';

class RouteScreen extends StatefulWidget {
  const RouteScreen({super.key});

  @override
  State<RouteScreen> createState() => _RouteScreenState();
}

class _RouteScreenState extends State<RouteScreen> {
  final ApiService _api = ApiService();
  List<RouteOption>? _routes;
  bool _loading = false;
  String? _error;

  Future<void> _findRoutes() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      // Placeholder coordinates — wire up geolocator + a destination
      // picker (map tap or search) here.
      final routes = await _api.planRoute(
        origin: const LatLngPoint(latitude: 26.1445, longitude: 91.7362), // Guwahati
        destination: const LatLngPoint(latitude: 25.5788, longitude: 91.8933), // Shillong
      );
      setState(() => _routes = routes);
    } catch (e) {
      setState(() => _error = 'Could not fetch routes. Showing offline/cached data if available.');
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  void initState() {
    super.initState();
    _findRoutes();
  }

  @override
  Widget build(BuildContext context) {
    return RefreshIndicator(
      onRefresh: _findRoutes,
      child: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const Text('Alternate Routes', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          // TODO: replace with google_maps_flutter GoogleMap widget showing
          // the route polylines and any hazard markers along the way.
          Container(
            height: 200,
            decoration: BoxDecoration(
              color: Colors.grey.shade300,
              borderRadius: BorderRadius.circular(14),
            ),
            alignment: Alignment.center,
            child: const Text('Map view goes here'),
          ),
          const SizedBox(height: 16),
          if (_loading) const Center(child: CircularProgressIndicator()),
          if (_error != null)
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 8),
              child: Text(_error!, style: const TextStyle(color: AppColors.warning)),
            ),
          if (_routes != null)
            ..._routes!.map(
              (r) => Card(
                child: ListTile(
                  leading: Icon(
                    r.hazardFree ? Icons.check_circle : Icons.error,
                    color: r.hazardFree ? AppColors.safe : AppColors.danger,
                  ),
                  title: Text(r.summary),
                  subtitle: Text('${r.distanceKm} km · ${r.durationMinutes.round()} min'),
                  trailing: r.isAlternate ? const Chip(label: Text('Alt')) : null,
                ),
              ),
            ),
        ],
      ),
    );
  }
}
