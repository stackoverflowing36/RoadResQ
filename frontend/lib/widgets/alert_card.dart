import 'package:flutter/material.dart';

import '../models/incident.dart';
import '../theme/app_theme.dart';

class AlertCard extends StatelessWidget {
  final String title;
  final String subtitle;
  final IncidentSeverity severity;
  final IconData icon;

  const AlertCard({
    super.key,
    required this.title,
    required this.subtitle,
    required this.severity,
    this.icon = Icons.warning_amber_rounded,
  });

  Color get _severityColor {
    switch (severity) {
      case IncidentSeverity.critical:
      case IncidentSeverity.high:
        return AppColors.danger;
      case IncidentSeverity.medium:
        return AppColors.warning;
      case IncidentSeverity.low:
        return AppColors.safe;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: _severityColor.withValues(alpha: 0.15),
          child: Icon(icon, color: _severityColor),
        ),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Text(subtitle),
        trailing: Icon(Icons.chevron_right, color: Colors.grey.shade400),
      ),
    );
  }
}
