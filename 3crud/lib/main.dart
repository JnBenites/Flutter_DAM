import 'package:crud_sqlite/models/user.dart';
import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Hive.initFlutter();
  await Hive.openBox('users');
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CRUD',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: UserListScreen(),
    );
  }
}

class UserListScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final box = Hive.box('users'); // Obtiene la referencia a la box de Hive
    
    return Scaffold(
      appBar: AppBar(title: Text('Lista de usuarios')),
      body: ValueListenableBuilder(
        valueListenable: box.listenable(),
        builder: (context, Box box, _) {
          if (box.isEmpty) {
            return Center(
              child: Text(
                'No hay usuarios registrados',
                style: TextStyle(fontSize: 18),
              ),
            );
          }
          return ListView.builder(
            itemCount: box.length,
            itemBuilder: (context, index) {
              final user = User.fromMap(
                Map<String, dynamic>.from(box.getAt(index)),
              );
              return Card(
                margin: EdgeInsets.all(8.0),
                child: ListTile(
                  title: Text(user.nombre),
                  subtitle: Text('${user.correo} - ${user.edad} años'),
                ),
              );
            },
          );
        },
      ),
    );
  }
}