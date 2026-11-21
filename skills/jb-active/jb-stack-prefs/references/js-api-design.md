# Good JavaScript library API design

JB supplied these guidelines on 2026-10-09. This concise English reference translates the supplied German synthesis of Artem Zakharchenko's work on API design, JavaScript protocols, and library packaging.

A good API is explicit, standards-based, semantically precise, composable, and educational. Minimize hidden state, proprietary concepts, and assumptions about the application. Types, module boundaries, cancellation, errors, and lifecycle contracts all belong to the public API.

## Explicit ownership

Expose behavior through imports, wrappers, adapters, or objects the library owns:

```ts
import { withCache } from 'library'

await fetch(withCache(request, options))
```

This makes the behavior's origin, scope, and impact visible. Avoid patching globals or other packages' prototypes, and keep proprietary semantics distinguishable from platform behavior. Each public function should support independent versioning and deprecation. Convenience must preserve predictability.

## Standard protocols

Prefer a suitable JavaScript or Web Platform protocol before inventing an interface: `AbortSignal` for cancellation and cleanup, `Iterable` and `Symbol.iterator` for iteration and spread, `Request`, `Response`, streams, and events for interoperable platform objects, and promises for asynchronous results.

Use a protocol when its semantics fit naturally and match user expectations. A native appearance alone does not justify it. Standards reduce learning costs and support composition across library boundaries.

## Precise semantics

Keep three concerns distinct:

- Execution: could the operation run?
- Result: did it produce a valid result?
- Policy: does that result satisfy the caller's expectations?

For example, `fetch()` rejects when a request fails, but an HTTP `404` or `500` response does not automatically reject its promise. The caller decides whether that response is an application error. Preserving these distinctions retains information and control for error handling, retries, telemetry, and composition.

## Function and callback contracts

Treat a function as an explicit data-flow contract: input → function → output. Require essential dependencies as inputs, return inspectable and testable outputs, keep responsibility coherent, and expose edge cases and error shapes. Names, inputs, and return values should establish a reliable expectation without unnecessary ambient state.

Higher-order functions let the library own the mechanism while callers supply policy. Document when callbacks run, their frequency and order, arguments and state, whether they may be synchronous or asynchronous, how returns and errors propagate, and what happens on cancellation or early termination. A callback signature alone is incomplete; lifecycle guarantees matter even when TypeScript cannot express them.

## Cancellation and cleanup

Design cancellation into asynchronous or long-lived operations, typically with an optional `AbortSignal`:

```ts
await libraryOperation(input, { signal })
```

The caller controls cancellation. Define which work stops and which resources are released, whether completed side effects remain, the resulting error or result, and how `signal.reason` is used. An abort signal can be aborted only once.

## Module and package contracts

Provide intentional, stable entry points, statically analyzable ESM, targeted subpath exports, and deliberate public exports. Avoid accidental import side effects. Verify tree shaking and consistency between built artifacts and type declarations from a consumer project.

For JB's current bundler default, see [repository tooling](repository-tooling.md). Use Rollup or direct Rolldown configuration only for a concrete compatibility or capability need. The Rollup article below informs architecture, not the current default tool choice. Check concrete `exports` fields and bundler configuration against current Node and tooling behavior.

## Transferable understanding

Teach a model users can apply beyond the library. Keep standards and domain concepts visible, avoid unnecessary proprietary vocabulary, and build abstractions on underlying concepts without hiding them completely. Provide escape hatches that preserve a coherent primary path. A useful abstraction reduces complexity while retaining the user's understanding and ability to migrate.

## Review checklist

- Ownership: is the responsible package clear, does it modify only what it owns, and are side effects and global state absent or explicit?
- Semantics: does the name match the operation, are execution, result, and caller policy distinct, and is relevant information preserved?
- Composition: do platform types and protocols fit, can other libraries compose without hidden collisions, and are cancellation and cleanup defined?
- Contracts: are inputs, outputs, errors, callback timing, order, repetition, and synchronous or asynchronous behavior explicit?
- Types: do they reflect runtime guarantees, make valid states easy and invalid states difficult to express, and infer well without exposing internal generics?
- Packaging: are entry points stable and intentional, do ESM, exports, and declarations work for consumers, and has tree shaking been verified in practice?
- Learning: does the API teach transferable concepts, preserve migration options, and offer convenience without imitating or hiding standards?

## Warning signs

- Framework-specific options attached to global standard functions.
- String-based channels or commands without a shared schema.
- Custom cancellation where `AbortSignal` fits.
- Promises that conflate transport, domain, and policy failures.
- Callbacks with undocumented invocation counts or order.
- A root export that loads the entire library and its side effects.
- TypeScript types that imply runtime validation which does not exist.
- Behavior understandable only by reading implementation code.
- Magical convenience that makes migration or interoperability harder.

## Example: Electron IPC

Use a shared typed contract for main and renderer, explicit operations instead of loose string channels, validated data across the process boundary, and consistent lifecycle and error semantics. The supplied related note is titled "Proper Electron IPC unlocks shared, dynamic application APIs".

## Source titles from JB's notes

The supplied notes use Obsidian references; their external URLs were not supplied.

- Artem Zakharchenko, "Why Patching Globals Is Harmful".
- Artem Zakharchenko, "Don't Sleep on AbortController".
- Artem Zakharchenko, "Why Fetch Promise Doesn't Reject on Error Responses".
- Artem Zakharchenko, "Thinking in Functions, Part I – The Input-Output Pattern".
- Artem Zakharchenko, "Thinking in Functions, Part II – Higher-order Functions".
- Artem Zakharchenko, "Symbol.iterator Is Pretty Neat, Actually".
- Artem Zakharchenko, "Building a Tree-shakable Library with Rollup".
- "kettanaito.com - Artem Zakharchenko", portfolio reference.
