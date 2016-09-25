var url = 'http://ec2-54-169-111-88.ap-southeast-1.compute.amazonaws.com/';
var method = 'post';
var http = require("http");
var options = {
  hostname: 'url',
  port: 80,
  path: '/api/postAd',
  method: 'POST',
  headers: {
      'Content-Type': 'application/json',
  }
};
var req = http.request(options, function(res) {
  console.log('Status: ' + res.statusCode);
  console.log('Headers: ' + JSON.stringify(res.headers));
  res.setEncoding('utf8');
  res.on('data', function (body) {
    console.log('Body: ' + body);
  });
});
req.on('error', function(e) {
  console.log('problem with request: ' + e.message);
});
// write data to request body
req.write('{"string": "updated successfully"}');
req.end();
