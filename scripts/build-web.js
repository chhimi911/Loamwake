const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const dist = path.join(root, "dist");
const web = path.join(root, "web");

function copyFile(source, destination) {
  fs.mkdirSync(path.dirname(destination), { recursive: true });
  fs.copyFileSync(source, destination);
}

function copyDir(source, destination) {
  if (!fs.existsSync(source)) {
    return;
  }
  for (const entry of fs.readdirSync(source, { withFileTypes: true })) {
    const sourcePath = path.join(source, entry.name);
    const destinationPath = path.join(destination, entry.name);
    if (entry.isDirectory()) {
      copyDir(sourcePath, destinationPath);
    } else {
      copyFile(sourcePath, destinationPath);
    }
  }
}

fs.rmSync(dist, { recursive: true, force: true });
fs.mkdirSync(dist, { recursive: true });

copyFile(path.join(web, "index.html"), path.join(dist, "index.html"));
copyFile(path.join(web, "styles.css"), path.join(dist, "styles.css"));
copyFile(path.join(web, "main.js"), path.join(dist, "main.js"));
copyFile(path.join(web, "game-core.mjs"), path.join(dist, "game-core.mjs"));
copyDir(path.join(root, "assets", "sounds"), path.join(dist, "assets", "sounds"));

console.log("Built Loamwake web app to dist/");
