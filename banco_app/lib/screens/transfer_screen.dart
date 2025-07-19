import 'package:flutter/material.dart';
import '../services/api_service.dart';

class TransferScreen extends StatefulWidget {
  @override
  State<TransferScreen> createState() => _TransferScreenState();
}

class _TransferScreenState extends State<TransferScreen> {
  final _fromController = TextEditingController();
  final _toController = TextEditingController();
  final _amountController = TextEditingController();
  final _descController = TextEditingController();
  String? _message;

  void _transfer() async {
    final api = ApiService();
    final success = await api.transfer(
      int.parse(_fromController.text),
      int.parse(_toController.text),
      double.parse(_amountController.text),
      _descController.text,
    );
    setState(() {
      _message = success ? 'Transferencia exitosa' : 'Error en la transferencia';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Hacer transferencia')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _fromController,
              decoration: InputDecoration(labelText: 'ID Cuenta origen'),
              keyboardType: TextInputType.number,
            ),
            TextField(
              controller: _toController,
              decoration: InputDecoration(labelText: 'ID Cuenta destino'),
              keyboardType: TextInputType.number,
            ),
            TextField(
              controller: _amountController,
              decoration: InputDecoration(labelText: 'Monto'),
              keyboardType: TextInputType.number,
            ),
            TextField(
              controller: _descController,
              decoration: InputDecoration(labelText: 'Descripción'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _transfer,
              child: Text('Transferir'),
            ),
            if (_message != null) Text(_message!),
          ],
        ),
      ),
    );
  }
}