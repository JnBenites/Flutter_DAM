import 'package:flutter/material.dart';
import '../services/api_service.dart';

class Categoria3Screen extends StatefulWidget {
  @override
  _Categoria3ScreenState createState() => _Categoria3ScreenState();
}

class _Categoria3ScreenState extends State<Categoria3Screen> {
  final apiService = ApiService();
  late Future<List<dynamic>> datos;

  @override
  void initState() {
    super.initState();
    datos = apiService.fetchData('https://jsonplaceholder.typicode.com/photos');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Categoría 3')),
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
                  title: Text(items[index]['title']),
                  leading: Image.network(items[index]['thumbnailUrl']),
                );
              },
            );
          }
        },
      ),
    );
  }
}