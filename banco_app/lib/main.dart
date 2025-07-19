import 'package:flutter/material.dart';
import 'screens/login_screen.dart';
import 'screens/home_screen.dart';
import 'screens/accounts_screen.dart';
import 'screens/policies_screen.dart';
import 'screens/transactions_screen.dart';
import 'screens/transfer_screen.dart';

void main() {
  runApp(BancoApp());
}

class BancoApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Banco App',
      initialRoute: '/',
      routes: {
        '/': (context) => LoginScreen(),
        '/home': (context) => HomeScreen(),
        '/accounts': (context) => AccountsScreen(),
        '/policies': (context) => PoliciesScreen(),
        '/transactions': (context) => TransactionsScreen(),
        '/transfer': (context) => TransferScreen(),
      },
    );
  }
}