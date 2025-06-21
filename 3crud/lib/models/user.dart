class User {
  String nombre;
  String correo;
  int edad;

  User({required this.nombre, required this.correo, required this.edad});

  Map<String, dynamic> toMap() => {
    'nombre': nombre,
    'correo': correo,
    'edad': edad,
  };

  factory User.fromMap(Map<String, dynamic> map) => User(
    nombre: map['nombre'],
    correo: map['correo'],
    edad: map['edad'],
  );
}