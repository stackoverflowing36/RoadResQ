import 'dart:convert';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';

/// Implements the "store-carry-forward" idea from the pitch: when a device
/// has no internet, it can hand incident/alert data to any nearby peer
/// device over Bluetooth. That peer carries the data until it reaches
/// connectivity and uploads it on the original device's behalf.
///
/// This is a starting skeleton — production use needs a defined GATT
/// service/characteristic UUID pair and de-duplication of relayed records.
class RoadResQBluetoothService {
  static const String serviceUuid = '0000fee1-0000-1000-8000-00805f9b34fb';

  Future<List<ScanResult>> scanForPeers({Duration timeout = const Duration(seconds: 6)}) async {
    await FlutterBluePlus.startScan(timeout: timeout);
    final results = await FlutterBluePlus.scanResults.first;
    await FlutterBluePlus.stopScan();
    return results;
  }

  /// Encodes a batch of pending records (incidents/alerts) as JSON bytes
  /// ready to be written to a peer's GATT characteristic.
  List<int> encodePayload(List<Map<String, dynamic>> records) {
    return utf8.encode(jsonEncode(records));
  }

  List<Map<String, dynamic>> decodePayload(List<int> bytes) {
    final decoded = jsonDecode(utf8.decode(bytes));
    return List<Map<String, dynamic>>.from(decoded);
  }

  // TODO: implement connectToPeer() + characteristic write/read using
  // flutter_blue_plus once the GATT service is defined on both ends.
}
