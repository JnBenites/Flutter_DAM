import 'package:flutter/material.dart';
import '../services/api_service.dart';

class TransactionsScreen extends StatefulWidget {
  @override
  State<TransactionsScreen> createState() => _TransactionsScreenState();
}

class _TransactionsScreenState extends State<TransactionsScreen> {
  List<dynamic>? transactions;

  @override
  void initState() {
    super.initState();
    _loadTransactions();
  }

  void _loadTransactions() async {
    final api = ApiService();
    final data = await api.getTransactions();
    setState(() {
      transactions = data;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (transactions == null) {
      return Scaffold(body: Center(child: CircularProgressIndicator()));
    }
    return Scaffold(
      appBar: AppBar(title: Text('Mis movimientos')),
      body: ListView.builder(
        itemCount: transactions!.length,
        itemBuilder: (context, index) {
          final tx = transactions![index];
          return ListTile(
            title: Text('Tipo: ${tx['type']} - \$${tx['amount']}'),
            subtitle: Text('De: ${tx['from_account']} a ${tx['to_account']}'),
          );
        },
      ),
    );
  }
}