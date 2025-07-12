// screens/categoria2_screen.dart
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class Categoria2Screen extends StatefulWidget {
  @override
  _Categoria2ScreenState createState() => _Categoria2ScreenState();
}

class _Categoria2ScreenState extends State<Categoria2Screen> {
  final apiService = ApiService();
  late Future<List<dynamic>> datos;

  @override
  void initState() {
    super.initState();
    datos = apiService.fetchData('https://jsonplaceholder.typicode.com/users');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Categoría 2')),
      body: FutureBuilder<List<dynamic>>(
        future: datos,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else {
            final items = snapshot.data!;
            return ListView.builder(
              itemCount: items.length,
              itemBuilder: (context, index) {
                return ListTile(
                  title: Text(items[index]['name']),
                  subtitle: Text(items[index]['email']),
                );
              },
            );
          }
        },
      ),
    );
  }
}