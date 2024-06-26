import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _controller = TextEditingController();
  String _result = "";

  Future<void> _searchQuery(String query) async {
    final response = await http.post(
      Uri.parse('http://127.0.0.1:5000/query'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{
        'query': query,
      }),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      setState(() {
        _result = 'Document: ${data['document']}\n\n${data['text']}';
      });
    } else {
      setState(() {
        _result = 'Error retrieving data';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Chatbot'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Expanded(
              child: SingleChildScrollView(
                child: Text(_result),
              ),
            ),
            if (_result == "") ...[
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
               
                children: [
                  Container(
                    width: 120,
                    height: 120,
                    decoration: BoxDecoration(
                        color: Colors.blue,
                        borderRadius: BorderRadius.circular(20)),
                    child: Center(
                      child: Text(
                        "Ask  Questions To Bot",
                        style: TextStyle(color: Colors.white),
                      ),
                    ),
                  ),
                  SizedBox(
                    width: 20,
                  ),
                  Container(
                    width: 120,
                    height: 120,
                    decoration: BoxDecoration(
                        color: Colors.blue,
                        borderRadius: BorderRadius.circular(20)),
                    child: Center(
                      child: Text(
                        "Ask  Questions To Bot",
                        style: TextStyle(color: Colors.white),
                      ),
                    ),
                  )
                ],
              )
            ],
            Spacer(),
            TextField(
              controller: _controller,
              decoration: InputDecoration(
                hintText: 'What is your query?',
              ),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => _searchQuery(_controller.text),
              child: Text('Search'),
            ),
            SizedBox(height: 20),
          ],
        ),
      ),
    );
  }
}
