Feature: Server echo. In order to test the correct parsing of the server we test it.

Scenario Outline: Simple GET request
Given the server is running at localhost:9100,
 when the server receives a request with method "<method>", path "<path>" and headers "<headers>"
 then the server responds with the "<expected_status>" status 
 and there exists an X-RequestEcho header
 and the contentx of X-RequestEcho are as expected, containing at least the same headers as sent by the client

 Examples: Simple
  | request  | method | path       | headers | expected_status |
  | REQ1     | GET    | /index.html | {"host": "localhost:9100"} | 200 |
  | REQ2     | POST   | /index.html | {"host": "localhost:9100", "Accept": "text/html"} | 200 |
  | REQ3     | GET    | /app1/index.html | {"host": "localhost:9100"} | 200 |
  | REQ4     | PUT    | /app2/index.html | {"host": "localhost:9100"} | 200 |
  | REQ5     | DELETE | /myapp3/index_v3.html | {"host": "localhost:9100"} | 404 |
