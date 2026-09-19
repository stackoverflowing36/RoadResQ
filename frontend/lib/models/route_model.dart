class LatLngPoint {
  final double latitude;
  final double longitude;

  const LatLngPoint({required this.latitude, required this.longitude});

  Map<String, dynamic> toJson() => {'latitude': latitude, 'longitude': longitude};
}

class RouteOption {
  final String summary;
  final double distanceKm;
  final double durationMinutes;
  final bool isAlternate;
  final bool hazardFree;
  final String? polyline;

  RouteOption({
    required this.summary,
    required this.distanceKm,
    required this.durationMinutes,
    this.isAlternate = false,
    this.hazardFree = true,
    this.polyline,
  });

  factory RouteOption.fromJson(Map<String, dynamic> json) => RouteOption(
        summary: json['summary'] ?? '',
        distanceKm: (json['distance_km'] as num).toDouble(),
        durationMinutes: (json['duration_minutes'] as num).toDouble(),
        isAlternate: json['is_alternate'] ?? false,
        hazardFree: json['hazard_free'] ?? true,
        polyline: json['polyline'],
      );
}
