enum IncidentType { landslide, flood, roadBlock, accident, weatherHazard, other }

enum IncidentSeverity { low, medium, high, critical }

class Incident {
  final String? id;
  final String? reporterId;
  final IncidentType type;
  final IncidentSeverity severity;
  final double latitude;
  final double longitude;
  final String? description;
  final String? photoUrl;
  final DateTime reportedAt;
  final bool syncedOffline;

  Incident({
    this.id,
    this.reporterId,
    required this.type,
    this.severity = IncidentSeverity.medium,
    required this.latitude,
    required this.longitude,
    this.description,
    this.photoUrl,
    required this.reportedAt,
    this.syncedOffline = false,
  });

  Map<String, dynamic> toJson() => {
        'reporter_id': reporterId,
        'incident_type': type.name,
        'severity': severity.name,
        'latitude': latitude,
        'longitude': longitude,
        'description': description,
        'photo_url': photoUrl,
        'reported_at': reportedAt.toIso8601String(),
        'synced_offline': syncedOffline,
      };

  factory Incident.fromJson(Map<String, dynamic> json) => Incident(
        id: json['id'],
        reporterId: json['reporter_id'],
        type: IncidentType.values.firstWhere(
          (t) => t.name == json['incident_type'],
          orElse: () => IncidentType.other,
        ),
        severity: IncidentSeverity.values.firstWhere(
          (s) => s.name == json['severity'],
          orElse: () => IncidentSeverity.medium,
        ),
        latitude: (json['latitude'] as num).toDouble(),
        longitude: (json['longitude'] as num).toDouble(),
        description: json['description'],
        photoUrl: json['photo_url'],
        reportedAt: DateTime.tryParse(json['reported_at'] ?? '') ?? DateTime.now(),
        syncedOffline: json['synced_offline'] ?? false,
      );

  // Row shape used by the local SQLite cache (see offline_storage_service.dart).
  Map<String, dynamic> toLocalRow() => {
        'id': id,
        'reporter_id': reporterId,
        'incident_type': type.name,
        'severity': severity.name,
        'latitude': latitude,
        'longitude': longitude,
        'description': description,
        'photo_url': photoUrl,
        'reported_at': reportedAt.toIso8601String(),
        'pending_sync': syncedOffline ? 0 : 1,
      };
}
