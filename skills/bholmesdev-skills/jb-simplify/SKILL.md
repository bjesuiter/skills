---
name: jb-simplify
description: Review a finished code diff for names, comments, structure, efficiency, fix depth, and overfitting. Use automatically once code works and passes its checks, before you commit or hand it off for human review. Do not load it before writing code, or for docs, prose, or config-only changes.
---
Review changes in the current branch, or in the scope the user specifies. Apply these criteria without changing behavior. Only touch code in that scope.

1. Read the diff (`git diff`, or `git diff <base>...HEAD` for committed work). Do not review from memory.
2. Check each section below against that diff and make the edits.
3. Run the relevant existing checks after changes.
4. Report each edit in one line, or "no change" with the reason. Do not claim a jb-simplify pass without steps 1 and 4.

## Word choice in code and comments

Variable names, function names, and comments are all prose. Apply Orwell's rules ("Politics and the English Language") to each:

> Never use a long word where a short one will do.
> 
> If it is possible to cut a word out, always cut it out.
> 
> Never use the passive where you can use the active.
> 
> Never use a foreign phrase, a scientific word, or a jargon word if you can think of an everyday English equivalent.

Latinate vocabulary (reconcile, coalesce, normalize, reconciliation) sounds technical and abstract; Anglo-Saxon words (prune, run, watch, stop, drop, walk) are short and physical. Prefer the Saxon word.

### Names

1. **One word per concept, one concept per word.** Keep a vocabulary. If `sync` names "pulling remote changes," it cannot also name "flushing edits to disk;" rename one of them.
2. **Cut words the context already carries.** A module named `workspaceWatcher` does not need `startNativeWorkspaceWatcher`; `watchWorkspace` says the same thing.
3. **A compound name is usually a hedge:**

- ❌ `lastObservedDiskContent` is a specification to defend
- ✅ `baseline` is a readable description

### Comments

State, in plain English, the constraint the code cannot show: why the **non-obvious** exists.

- ✅ If code is complex and the implementation is non-obvious, add a comment.
- ✅ If a function contains complex behaviors or side effects, add a doc comment.
- 🗑️ If a comment narrates change history from the conversation, delete it.
- 🗑️ If a comment restates code whose behavior is self-evident, delete it.

## Code structure

1. **Inverted pyramid.** Within a file, lead with the exported or significant functions and push helpers below them. Don't bury the lead.
2. **Related concepts over monoliths.** Break a large file into modules that each own one concept.
3. **Combine overlapping concepts.** If two types, functions, or constants overlap significantly, merge them. The fewer distinct concepts a reader must hold in their head, the better.
4. **Use shared code.** Common utilities (ex. file path parsing) may exist in the codebase already. Check for library or utility functions before inlining.
5. **Derivability.** If a value can be computed from values already in scope, don't pass or store it separately. Removing derivable state often simplifies signatures, types, and control flow in one move. Example: an `isDirty` parameter that is always `editorContent !== baseline` can be dropped.

## Efficiency

Flag wasted work the diff adds: repeated computation or I/O, independent operations run one after another, and blocking work on startup or hot paths. Name the cheaper form.

## Altitude

Fix the root cause at the right depth, not the symptom. A special case added to shared code is a sign the fix is too shallow. Prefer one general change to the underlying mechanism.

## Overfitting

Code must stand on its own. If a change only makes sense to someone who watched it happen (this conversation, this PR), it is overfitted. Write for the reader who arrives with no history.

- If a name or comment needs the conversation to be understood, rewrite it against the codebase's own vocabulary.
- **No backwards compatibility with unshipped code.** Supporting an old signature, alias, or data shape that only existed earlier in the same branch is compatibility with something that was never deployed. Delete the old path and update its callers.

