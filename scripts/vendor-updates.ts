import { readdir } from "node:fs/promises";
import { join } from "node:path";
import JSON5 from "json5";

type Vendor = {
  repo: string;
  url: string;
  track: { type: "release" } | { type: "commit"; branch: string };
  snapshot: { revision: string; vendoredAt: string } | null;
};

const skills = join(import.meta.dir, "../skills");
const directories = await readdir(skills, { withFileTypes: true });
let checked = 0;

for (const directory of directories) {
  if (!directory.isDirectory()) continue;
  const manifest = Bun.file(join(skills, directory.name, "vendor.json5"));
  if (!(await manifest.exists())) continue;

  checked++;
  try {
    const vendor = readVendor(await manifest.text(), directory.name);
    const latest = await upstreamRevision(vendor);
    if (!vendor.snapshot) {
      console.log(`${vendor.repo}: no import recorded; upstream is ${latest}`);
    } else if (vendor.snapshot.revision === latest) {
      console.log(`${vendor.repo}: up to date (${latest})`);
    } else {
      console.log(`${vendor.repo}: upstream differs (${vendor.snapshot.revision} → ${latest})`);
    }
  } catch (error) {
    console.error(`${directory.name}: ${error instanceof Error ? error.message : error}`);
    process.exitCode = 1;
  }
}

if (!checked) console.log("No vendor manifests found.");

function readVendor(source: string, directory: string): Vendor {
  const vendor = JSON5.parse(source) as Partial<Vendor> | null;
  if (
    typeof vendor?.repo !== "string" ||
    !/^[\w.-]+\/[\w.-]+$/.test(vendor.repo) ||
    directory !== vendor.repo.replace("/", "-")
  ) {
    throw new Error("Expected repo owner/repo matching the owner-repo directory.");
  }

  if (
    vendor.url !== `https://github.com/${vendor.repo}` &&
    vendor.url !== `https://github.com/${vendor.repo}.git`
  ) {
    throw new Error("Expected the HTTPS GitHub URL for repo.");
  }

  const { track, snapshot } = vendor;
  if (
    track?.type !== "release" &&
    (track?.type !== "commit" || typeof track.branch !== "string" || !track.branch.trim())
  ) {
    throw new Error("Expected release tracking or commit tracking with a branch.");
  }

  if (
    snapshot !== null &&
    (typeof snapshot?.revision !== "string" ||
      !snapshot.revision.trim() ||
      (track.type === "commit" && !/^[a-f0-9]{40}$/.test(snapshot.revision)) ||
      typeof snapshot.vendoredAt !== "string" ||
      !/^\d{4}-\d{2}-\d{2}$/.test(snapshot.vendoredAt) ||
      !Number.isFinite(Date.parse(snapshot.vendoredAt)) ||
      new Date(snapshot.vendoredAt).toISOString().slice(0, 10) !== snapshot.vendoredAt)
  ) {
    throw new Error("Expected snapshot: null or a revision and a YYYY-MM-DD vendoredAt date.");
  }

  return { repo: vendor.repo, url: vendor.url, track, snapshot };
}

async function upstreamRevision(vendor: Vendor): Promise<string> {
  if (vendor.track.type === "release") {
    return run(["gh", "api", `repos/${vendor.repo}/releases/latest`, "--jq", ".tag_name"]);
  }

  const ref = `refs/heads/${vendor.track.branch}`;
  await run(["git", "check-ref-format", ref]);
  const result = await run(["git", "ls-remote", "--exit-code", "--refs", "--", vendor.url, ref]);
  return result.split("\t")[0];
}

async function run(command: string[]): Promise<string> {
  const child = Bun.spawn(command, {
    stdin: "ignore",
    stdout: "pipe",
    stderr: "pipe",
    env: { ...process.env, GIT_TERMINAL_PROMPT: "0" },
  });
  const [status, stdout, stderr] = await Promise.all([
    child.exited,
    child.stdout.text(),
    child.stderr.text(),
  ]);
  if (status !== 0) throw new Error(stderr.trim() || `${command.join(" ")} exited with ${status}.`);
  return stdout.trim();
}
