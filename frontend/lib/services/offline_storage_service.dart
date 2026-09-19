import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';

import '../models/incident.dart';

/// Local-first cache: every incident is written here immediately,
/// regardless of connectivity, then synced to the backend when a
/// connection (direct or via a peer device) becomes available.
class OfflineStorageService {
  static final OfflineStorageService _instance = OfflineStorageService._internal();
  factory OfflineStorageService() => _instance;
  OfflineStorageService._internal();

  Database? _db;

  Future<Database> get database async {
    _db ??= await _initDb();
    return _db!;
  }

  Future<Database> _initDb() async {
    final path = join(await getDatabasesPath(), 'roadresq.db');
    return openDatabase(
      path,
      version: 1,
      onCreate: (db, version) async {
        await db.execute('''
          CREATE TABLE incidents (
            local_id INTEGER PRIMARY KEY AUTOINCREMENT,
            id TEXT,
            reporter_id TEXT,
            incident_type TEXT,
            severity TEXT,
            latitude REAL,
            longitude REAL,
            description TEXT,
            photo_url TEXT,
            reported_at TEXT,
            pending_sync INTEGER
          )
        ''');
      },
    );
  }

  Future<void> saveIncidentLocally(Incident incident) async {
    final db = await database;
    await db.insert('incidents', incident.toLocalRow());
  }

  Future<List<Map<String, dynamic>>> getPendingIncidents() async {
    final db = await database;
    return db.query('incidents', where: 'pending_sync = 1');
  }

  Future<void> markSynced(int localId) async {
    final db = await database;
    await db.update(
      'incidents',
      {'pending_sync': 0},
      where: 'local_id = ?',
      whereArgs: [localId],
    );
  }
}
