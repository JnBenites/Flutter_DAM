import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  static const String baseUrl = 'https://banco.capacitacioncontinua.info/api';

  Future<bool> login(String username, String password) async {
    final url = Uri.parse('$baseUrl/auth/login/');
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'username': username, 'password': password}),
    );
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('access', data['access']);
      await prefs.setString('refresh', data['refresh']);
      return true;
    }
    return false;
  }

  Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('access');
  }

  Future<List<dynamic>?> getAccounts() async {
    final token = await getToken();
    final url = Uri.parse('$baseUrl/accounts/');
    final response = await http.get(
      url,
      headers: {'Authorization': 'Bearer $token'},
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    return null;
  }

  Future<List<dynamic>?> getPolicies() async {
    final token = await getToken();
    final url = Uri.parse('$baseUrl/policies/');
    final response = await http.get(
      url,
      headers: {'Authorization': 'Bearer $token'},
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    return null;
  }

  Future<List<dynamic>?> getTransactions() async {
    final token = await getToken();
    final url = Uri.parse('$baseUrl/transactions/');
    final response = await http.get(
      url,
      headers: {'Authorization': 'Bearer $token'},
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    return null;
  }

  Future<bool> transfer(int fromAccount, int toAccount, double amount, String description) async {
    final token = await getToken();
    final url = Uri.parse('$baseUrl/transactions/transfer/');
    final response = await http.post(
      url,
      headers: {'Authorization': 'Bearer $token', 'Content-Type': 'application/json'},
      body: jsonEncode({
        'from_account': fromAccount,
        'to_account': toAccount,
        'amount': amount,
        'description': description,
      }),
    );
    return response.statusCode == 201;
  }
}