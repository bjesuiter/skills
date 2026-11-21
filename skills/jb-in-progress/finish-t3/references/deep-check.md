# Deep-check

Run the bundled read-only [script](../scripts/deep_check.py) from a surviving checkout:

```sh
uv run --no-project python /path/to/finish-t3/scripts/deep_check.py \
  --worktree /absolute/worktree --main-checkout /absolute/main-checkout
```

Use the skill's actual script path. The two explicit roots must be different
checkouts of the same repository. The script walks the worktree without
following symlink directories, applies Git's ignore rules, and compares regular
files byte-for-byte at the same relative path in the main checkout. It emits
JSON with paths and statuses, never file contents, hashes, or symlink targets.
It reads all ignored regular files that have a regular counterpart, so large
build/dependency trees can take time. Empty directories are not preservation
candidates. Stop worktree writers before scanning and rerun after saving data;
a scan is not an atomic filesystem snapshot.

Exit codes: `0` means all inventoried ignored files have identical regular-file
copies; `1` means review is needed; `2` means an inventory/comparison failed.
Missing, different, symlink, special-file, and type-mismatch entries need a
recorded disposition. Errors block cleanup until resolved. Identical files
are backed up only at the reported main-checkout path; preserve that checkout.

For each unique candidate, determine whether it can be recreated from saved
sources and available inputs. Reproducible build/dependency outputs such as
`dist/`, `build/`, and caches need no backup. Their names alone do not establish
reproducibility. Local configuration, credentials, databases, uploads, notes,
and manually produced assets may need preservation. Treat uncertain files as
needing preservation until resolved.

Save needed data to an appropriate durable location outside the worktree and
verify the saved copy before removal. Keep secrets out of Git and public
artifacts. If no suitable destination is established, retain the worktree and
ask for the missing destination. Report candidate paths and dispositions,
without sensitive contents.

