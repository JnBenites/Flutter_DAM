import 'package:flutter/material.dart';
import '../services/api_service.dart';

class AccountsScreen extends StatefulWidget {
  @override
  State<AccountsScreen> createState() => _AccountsScreenState();
}

class _AccountsScreenState extends State<AccountsScreen> {
  List<dynamic>? accounts;

  @override
  void initState() {
    super.initState();
    _loadAccounts();
  }

  void _loadAccounts() async {
    final api = ApiService();
    final data = await api.getAccounts();
    setState(() {
      accounts = data;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (accounts == null) {
      return Scaffold(body: Center(child: CircularProgressIndicator()));
    }
    return Scaffold(
      appBar: AppBar(title: Text('Mis cuentas')),
      body: ListView.builder(
        itemCount: accounts!.length,
        itemBuilder: (context, index) {
          final account = accounts![index];
          return ListTile(
            title: Text('Cuenta: ${account['number']}'),
            subtitle: Text('Saldo: \$${account['balance']}'),
          );
        },
      ),
    );
  }
}