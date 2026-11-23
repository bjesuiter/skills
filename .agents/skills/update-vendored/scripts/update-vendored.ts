import { mkdtemp, readdir, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import JSON5 from "json5";

type Vendor = {
  repo: string;
  url: string;
  upstreamSubdirectory?: string;
  /** Local skill name → upstream skill directory, for skills renamed on import. */
  upstreamNames?: Record<string, string>;
  gist?: { id: string; files: Record<string, string> };
  track: { type: "release" } | { type: "commit"; branch: string };
  snapshot: { revision: string; vendoredAt: string } | null;
};

const skills = join(import.meta.dir, "../../../../skills");
const args = Bun.argv.slice(2);
const includeDiffs = args.length === 1 && args[0] === "--diffs";
if (args.length && !includeDiffs) {
  console.error("Usage: bun .agents/skills/update-vendored/scripts/update-vendored.ts [--diffs]");
  process.exit(1);
}
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
    if (includeDiffs) {
      const previous = vendor.snapshot?.revision ?? null;
      const changed = previous !== latest;
      const changes = changed ? await skillDiffs(vendor, directory.name, previous, latest) : [];
      console.log(JSON.stringify({
        status: previous === null ? "unimported" : changed ? "changed" : "unchanged",
        repo: vendor.repo,
        directory: directory.name,
        previous,
        latest,
        changes,
      }));
    } else if (!vendor.snapshot) {
      console.log(`${vendor.repo}: no import recorded; upstream is ${latest}`);
    } else if (vendor.snapshot.revision === latest) {
      console.log(`${vendor.repo}: up to date (${latest})`);
    } else {
      console.log(`${vendor.repo}: upstream differs (${vendor.snapshot.revision} → ${latest})`);
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    if (includeDiffs) {
      console.log(JSON.stringify({ status: "error", directory: directory.name, message }));
    } else {
      console.error(`${directory.name}: ${message}`);
    }
    process.exitCode = 1;
  }
}

if (!checked && !includeDiffs) console.log("No vendor manifests found.");

async function skillDiffs(vendor: Vendor, directory: string, previous: string | null, latest: string) {
  const localFolder = join(skills, directory);
  const entries = await readdir(localFolder, { withFileTypes: true });
  const selected: string[] = [];
  for (const entry of entries) {
    if (entry.isDirectory() && await Bun.file(join(localFolder, entry.name, "SKILL.md")).exists()) {
      selected.push(entry.name);
    }
  }
  if (!selected.length) return [];

  const scratch = await mkdtemp(join(tmpdir(), "vendor-updates-"));
  const git = (...command: string[]) => run(["git", "-C", scratch, ...command]);
  try {
    await git("init", "--bare", "--quiet");
    const ref = (revision: string) => vendor.track.type === "release" ? `refs/tags/${revision}` : revision;
    const refs = [`${ref(latest)}:refs/vendor/incoming`];
    if (previous !== null) refs.push(`${ref(previous)}:refs/vendor/base`);
    await git("fetch", "--quiet", "--depth=1", "--no-tags", "--", vendor.url, ...refs);
    const base = previous === null ? await git("mktree") : "refs/vendor/base^{tree}";
    const incoming = "refs/vendor/incoming^{tree}";
    const upstreamSkills = vendor.upstreamSubdirectory ? `${vendor.upstreamSubdirectory}/skills` : "skills";
    const changes = [];
    for (const skill of selected.sort()) {
      const gistFile = vendor.gist?.files[skill];
      const upstreamPath = gistFile ?? `${upstreamSkills}/${vendor.upstreamNames?.[skill] ?? skill}`;
      const selectedPath = `:(literal)${upstreamPath}`;
      const diff = await git(
        "diff", "--binary", "--no-ext-diff", "--no-textconv", "--no-color", "--find-renames",
        base, incoming, "--", selectedPath,
      );
      const entrypoint = gistFile ? selectedPath : `${selectedPath}/SKILL.md`;
      const oldEntrypoint = await git("ls-tree", "-r", "--name-only", base, "--", entrypoint);
      const newEntrypoint = await git("ls-tree", "-r", "--name-only", incoming, "--", entrypoint);
      const status = newEntrypoint ? "changed" : oldEntrypoint ? "removed" : "missing";
      if (diff || status !== "changed") {
        changes.push({ skill, upstreamPath, localPath: `skills/${directory}/${skill}`, status, diff });
      }
    }
    return changes;
  } finally {
    await rm(scratch, { recursive: true, force: true });
  }
}

function readVendor(source: string, directory: string): Vendor {
  const vendor = JSON5.parse(source) as Partial<Vendor> | null;
  if (
    typeof vendor?.repo !== "string" ||
    !/^[\w.-]+\/[\w.-]+$/.test(vendor.repo)
  ) {
    throw new Error("Expected repo in owner/repo form.");
  }

  const { gist, upstreamSubdirectory, upstreamNames, track, snapshot } = vendor;
  if (
    upstreamNames !== undefined &&
    (gist !== undefined || !upstreamNames || typeof upstreamNames !== "object" || Array.isArray(upstreamNames) ||
      Object.entries(upstreamNames).some(([local, upstream]) =>
        !/^[a-z0-9-]+$/.test(local) || typeof upstream !== "string" || !/^[\w-][\w.-]*$/.test(upstream)))
  ) {
    throw new Error("Expected upstreamNames to map local skill names to upstream skill directories.");
  }

  if (
    upstreamSubdirectory !== undefined &&
    (gist !== undefined || typeof upstreamSubdirectory !== "string" ||
      !/^[\w.-]+(?:\/[\w.-]+)*$/.test(upstreamSubdirectory) ||
      upstreamSubdirectory.split("/").some((part) => part === "." || part === ".."))
  ) {
    throw new Error("Expected upstreamSubdirectory to be a relative directory in a GitHub repository.");
  }

  const repoDirectory = vendor.repo.replace("/", "-");
  const subdirectorySuffix = upstreamSubdirectory?.replaceAll("/", "-");
  if (directory !== repoDirectory && (!subdirectorySuffix || directory !== `${repoDirectory}-${subdirectorySuffix}`)) {
    throw new Error("Expected the owner-repo directory, optionally suffixed with upstreamSubdirectory.");
  }

  if (gist !== undefined) {
    const [owner, repo] = vendor.repo.split("/");
    if (
      repo !== "gists" ||
      typeof gist?.id !== "string" ||
      !/^[a-f0-9]{32}$/.test(gist.id) ||
      vendor.url !== `https://gist.github.com/${owner}/${gist.id}.git` ||
      track?.type !== "commit" ||
      !gist.files ||
      typeof gist.files !== "object" ||
      Array.isArray(gist.files) ||
      !Object.keys(gist.files).length ||
      Object.entries(gist.files).some(([skill, filename]) =>
        !/^[a-z0-9-]+$/.test(skill) || typeof filename !== "string" ||
        !/^[\w.-]+\.md$/i.test(filename))
    ) {
      throw new Error("Expected a GitHub Gist URL, commit tracking, and a skill-to-file map.");
    }
  } else if (
    vendor.url !== `https://github.com/${vendor.repo}` &&
    vendor.url !== `https://github.com/${vendor.repo}.git`
  ) {
    throw new Error("Expected the HTTPS GitHub URL for repo.");
  }

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

  return { repo: vendor.repo, url: vendor.url, gist, upstreamSubdirectory, upstreamNames, track, snapshot };
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
  return stdout.endsWith("\n") ? stdout.slice(0, -1) : stdout;
}
