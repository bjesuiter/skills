# Import upstream skills

Each local vendor directory (`skills/<owner>-<repo>/`) has a `vendor.json5` with the GitHub repository, its HTTPS URL, and the revision to track. See [the tstack manifest](../../../../skills/t3dotgg-tstack/vendor.json5).

When upstream keeps its `skills/` folder below the repository root, set `upstreamSubdirectory` to the relative path that contains it. A local vendor folder may append that path to its name, with slashes replaced by hyphens. For example, [the Cursor manifest](../../../../skills/cursor-plugins-pstack/vendor.json5) sets `upstreamSubdirectory: "pstack"` and tracks skills under `pstack/skills/`.

Keep the selection and reasons for omissions in the local vendor directory's `README.md`. Check that file before choosing what to export for an update.

- Fetch the pinned revision into a temporary Git repository. Use `git archive` to export the selected skill directories and upstream license and notices. Copy whole skill directories so bundled files and executable modes carry over.
- Inspect cross-skill references before selecting directories. Include required sibling skills and document them in the catalog when a user might install skills individually.
- Use `track: { type: "commit", branch: "main" }` to check a branch tip, or `track: { type: "release" }` to check the latest GitHub release using `gh`.
- Set `snapshot` to `null` until the first import. After importing, record `snapshot: { revision: "...", vendoredAt: "YYYY-MM-DD" }` with the full commit SHA or exact release tag that was imported.
- Use one snapshot per local vendor directory. When refreshing a folder, bring all its imported skills to the recorded revision and reapply local changes.

For GitHub Gists, use `<owner>-gists` as the folder and `<owner>/gists` as the manifest's `repo`. Set `url` to the gist's HTTPS Git clone URL and add `gist: { id: "...", files: { "<skill-name>": "<gist-filename>.md" } }`. Track the gist branch by commit. The checker diffs the mapped source file. Adapt changes into the local skill using the source folder's README.
