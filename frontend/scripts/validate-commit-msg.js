const fs = require("fs");

const filePath = process.argv[2];

if (!filePath) {
  console.error("Missing commit message file path.");
  process.exit(1);
}

const rawMessage = fs.readFileSync(filePath, "utf8");
// Only validate the header line (Conventional Commits applies to the first line).
const header = rawMessage.split(/\r?\n/, 1)[0].trim();
// Skip common auto-generated Git messages.
if (
  header.startsWith("Merge ") ||
  header.startsWith("Revert ") ||
  header.startsWith("fixup! ") ||
  header.startsWith("squash! ")
) {
  process.exit(0);
}
const message = header;
const pattern =
  /^(feat|fix|hotfix|bugfix|wip|docs|chore|style|refactor|ci|test|revert|perf|build)(\([^)]+\))?(!)?: .{1,}$/;

if (!pattern.test(message)) {
  console.error(`✗ Invalid commit message: '${message}'`);
  console.error("");
  console.error("Format: <type>(<scope>): <description>");
  console.error(
    "Types: feat|fix|hotfix|bugfix|wip|docs|chore|style|refactor|ci|test|revert|perf|build"
  );
  console.error("Contoh: feat(auth): add login page");
  process.exit(1);
}
