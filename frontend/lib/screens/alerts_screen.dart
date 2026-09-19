import 'package:flutter/material.dart';

import '../models/incident.dart';
import '../widgets/alert_card.dart';

class AlertsScreen extends StatelessWidget {
  const AlertsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // TODO: wire up ApiService.getIncidents()/alerts endpoint and fall back
    // to OfflineStorageService cache when offline.
    final demoAlerts = [
      const AlertCard(
        title: 'Landslide Reported',
        subtitle: 'NH-6 near Dima Hasao · 2.3 km ahead',
        severity: IncidentSeverity.critical,
        icon: Icons.terrain,
      ),
      const AlertCard(
        title: 'Heavy Rainfall',
        subtitle: 'Expected in the next hour',
        severity: IncidentSeverity.medium,
        icon: Icons.cloud,
      ),
      const AlertCard(
        title: 'Road Reopened',
        subtitle: 'Traffic resumed on alternate route',
        severity: IncidentSeverity.low,
        icon: Icons.check_circle_outline,
      ),
    ];

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        const Text('Alerts & Notifications', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        ...demoAlerts,
      ],
    );
  }
}
