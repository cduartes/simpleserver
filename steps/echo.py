import requests
import json
from nose.tools import *

def createEchoHeader(method, path, headers):  
  echoHeader = {}  
  echoHeader['method'] = method
  echoHeader['path'] = path
  echoHeader['headers'] = json.loads(headers)
  echoHeader['protocol'] = "HTTP/1.1"  
  return echoHeader

def compareEchoHeaders(response_headers, expected_headers):
  response_h = response_headers.pop('headers')
  expected_h = expected_headers.pop('headers')
  response_h_items = list(map(lambda x: (x[0].strip(), x[1].strip()), response_h.items()))
  expected_h_items = list(map(lambda x: (x[0].strip(), x[1].strip()), expected_h.items()))
  print(set(expected_h_items) <= set(response_h_items))
  
  return (set(expected_h_items) <= set(response_h_items)) and (expected_headers == response_headers)

@given(u'the server is running at localhost:9100,')
def step_impl(context):
  requests.get("http://localhost:9100/")  

@when(u'the server receives a request with method "{method}", path "{path}" and headers "{headers}"')
def step_impl(context, method, path, headers):

  url = "http://localhost:9100" + path
  r = None  
  r = requests.get   (url, headers = json.loads(headers)) if "GET"    == method else r
  r = requests.post  (url, headers = json.loads(headers)) if "POST"   == method else r
  r = requests.delete(url, headers = json.loads(headers)) if "DELETE" == method else r
  r = requests.put   (url, headers = json.loads(headers)) if "PUT"    == method else r
  if r is None:
    raise ValueError("Unsupported method %s" % method)
  
  context.result = r  
  context.expected_echo_header = createEchoHeader(method, path, headers)  
  
@then(u'the server responds with the "{expected_status}" status')
def step_impl(context, expected_status):
  ok_(str(context.result.status_code) == expected_status
      , "Response did not match expected status %s" % expected_status)

@then(u'there exists an X-RequestEcho header')
def step_impl(context):
  ok_("X-RequestEcho" in context.result.headers, "X-RequestEcho not sent as a response header")

@then(u'the contentx of X-RequestEcho are as expected, containing at least the same headers as sent by the client')
def step_impl(context):  
  response_echo_header = json.loads(context.result.headers['X-RequestEcho'])  
  ok_(compareEchoHeaders(response_echo_header, context.expected_echo_header)
      , "X-RequestEcho header does not match expected content")
  