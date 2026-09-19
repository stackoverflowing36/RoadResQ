import 'dart:convert';
import 'package:http/http.dart' as http;

import '../models/incident.dart';
import '../models/route_model.dart';

/// Talks to the RoadResQ FastAPI backend.
/// Update [baseUrl] to point at your deployed backend (or localhost for dev:
/// use 10.0.2.2 instead of localhost when running on the Android emulator).
class ApiService {
  static const String baseUrl = 'https://YOUR-BACKEND-URL.example.com/api/v1';

  Future<Incident> reportIncident(Incident incident) async {
    final response = await http.post(
      Uri.parse('$baseUrl/incidents'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(incident.toJson()),
    );
    if (response.statusCode != 201) {
      throw Exception('Failed to report incident: ${response.body}');
    }
    return Incident.fromJson(jsonDecode(response.body));
  }

  Future<List<Incident>> getIncidents({double? lat, double? lng, double radiusKm = 25}) async {
    final uri = Uri.parse('$baseUrl/incidents').replace(queryParameters: {
      if (lat != null) 'lat': lat.toString(),
      if (lng != null) 'lng': lng.toString(),
      'radius_km': radiusKm.toString(),
    });
    final response = await http.get(uri);
    if (response.statusCode != 200) {
      throw Exception('Failed to load incidents');
    }
    final List data = jsonDecode(response.body);
    return data.map((e) => Incident.fromJson(e)).toList();
  }

  Future<List<RouteOption>> planRoute({
    required LatLngPoint origin,
    required LatLngPoint destination,
    bool avoidHazards = true,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/routes'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'origin': origin.toJson(),
        'destination': destination.toJson(),
        'avoid_hazards': avoidHazards,
      }),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to plan route');
    }
    final data = jsonDecode(response.body);
    return (data['routes'] as List).map((e) => RouteOption.fromJson(e)).toList();
  }
}
