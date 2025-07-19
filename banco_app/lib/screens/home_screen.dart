import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Inicio')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () => Navigator.pushNamed(context, '/accounts'),
              child: Text('Ver Cuentas'),
            ),
            ElevatedButton(
              onPressed: () => Navigator.pushNamed(context, '/policies'),
              child: Text('Ver Pólizas'),
            ),
            ElevatedButton(
              onPressed: () => Navigator.pushNamed(context, '/transactions'),
              child: Text('Ver Movimientos'),
            ),
            ElevatedButton(
              onPressed: () => Navigator.pushNamed(context, '/transfer'),
              child: Text('Hacer Transferencia'),
            ),
          ],
        ),
      ),
    );
  }
}