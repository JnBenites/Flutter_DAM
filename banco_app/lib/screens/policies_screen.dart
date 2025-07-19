import 'package:flutter/material.dart';
import '../services/api_service.dart';

class PoliciesScreen extends StatefulWidget {
  @override
  State<PoliciesScreen> createState() => _PoliciesScreenState();
}

class _PoliciesScreenState extends State<PoliciesScreen> {
  List<dynamic>? policies;

  @override
  void initState() {
    super.initState();
    _loadPolicies();
  }

  void _loadPolicies() async {
    final api = ApiService();
    final data = await api.getPolicies();
    setState(() {
      policies = data;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (policies == null) {
      return Scaffold(body: Center(child: CircularProgressIndicator()));
    }
    return Scaffold(
      appBar: AppBar(title: Text('Mis pólizas')),
      body: ListView.builder(
        itemCount: policies!.length,
        itemBuilder: (context, index) {
          final policy = policies![index];
          return ListTile(
            title: Text('Monto: \$${policy['amount']}'),
            subtitle: Text('Estado: ${policy['status']}'),
          );
        },
      ),
    );
  }
}