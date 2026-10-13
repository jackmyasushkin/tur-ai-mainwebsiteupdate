const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const routes = {
  '/': [path.join(__dirname,'index.html'),'text/html'],
  '/driver.js': [path.join(__dirname,'driver.js'),'text/javascript'],
  '/formatter.js': [path.join(__dirname,'../../webflow/home-ordinal-format.js'),'text/javascript']
};
http.createServer((req,res)=>{
  const route=routes[new URL(req.url,'http://127.0.0.1').pathname];
  if(!route){res.writeHead(404);res.end();return;}
  res.writeHead(200,{'Content-Type':route[1],'Cache-Control':'no-store'});
  res.end(fs.readFileSync(route[0]));
}).listen(8766,'127.0.0.1',()=>console.log('Isolated QA fixture: http://127.0.0.1:8766'));
