import 'package:flutter/material.dart';
import 'screens/categoria1_screen.dart';
import 'screens/categoria2_screen.dart';
import 'screens/categoria3_screen.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Menú API',
      home: MenuPrincipal(),
    );
  }
}

class MenuPrincipal extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Menú Principal')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              child: Text('Categoría 1'),
              onPressed: () => Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => Categoria1Screen()),
              ),
            ),
            ElevatedButton(
              child: Text('Categoría 2'),
              onPressed: () => Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => Categoria2Screen()),
              ),
            ),
            ElevatedButton(
              child: Text('Categoría 3'),
              onPressed: () => Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => Categoria3Screen()),
              ),
            ),
          ],
        ),
      ),
    );
  }
}