const http = require("http");
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const web = path.join(root, "web");
const port = Number(process.env.PORT || 4173);

const types = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".wav": "audio/wav",
  ".png": "image/png"
};

function resolveRequest(url) {
  const clean = decodeURIComponent(url.split("?")[0]);
  if (clean === "/" || clean === "/index.html") {
    return path.join(web, "index.html");
  }
  if (clean.startsWith("/assets/")) {
    return path.join(root, clean);
  }
  return path.join(web, clean);
}

const server = http.createServer((request, response) => {
  const filePath = resolveRequest(request.url);
  if (!filePath.startsWith(web) && !filePath.startsWith(path.join(root, "assets"))) {
    response.writeHead(403);
    response.end("Forbidden");
    return;
  }
  fs.readFile(filePath, (error, content) => {
    if (error) {
      response.writeHead(404);
      response.end("Not found");
      return;
    }
    response.writeHead(200, { "Content-Type": types[path.extname(filePath)] || "application/octet-stream" });
    response.end(content);
  });
});

server.listen(port, "127.0.0.1", () => {
  console.log(`Loamwake web dev server: http://127.0.0.1:${port}`);
});
