# Web stack preferences

Confirmed by JB on 2026-10-09 in the initial `jb-stack-prefs` discussion. These are personal stack choices; release labels below reflect that discussion and need verification when selecting an actual dependency version.

## SPAs and offline PWAs

- Preferred default: SolidJS 1.x, JB's stable-branch choice for single-page web apps and PWAs with offline functionality.
- Allowed for less important projects: SolidJS 2 RC. Keep this scoped to projects where JB accepts prerelease risk.
- Offline functionality remains a project requirement to design and verify; the framework preference alone does not provide it.

## Cloudflare services and websites with a server and frontend

- Preferred default: TanStack Start with React, especially when developing a product.
- Rationale: JB prefers the React variant for compatibility with the React library ecosystem.
- Database: Cloudflare D1, with the Drizzle preference below applying to the ORM choice.
- Object storage: Cloudflare R2 for S3-style storage.
- Add other Cloudflare services as the product needs them.

## Authentication and payments

- Preferred when enterprise authentication is required: WorkOS. Use Theo's sponsor code when signing up; verify the current code from Theo's official sponsorship material at that time. Confirmed by JB on 2026-10-09 in a follow-up to the initial discussion.
- Preferred managed SaaS authentication: Clerk, especially for the Cloudflare product stack above.
- Evaluating: Clerk for payments. JB wants to assess it; this is not an adopted payment choice.
- Preferred when JB wants to build and control authentication more directly: Better Auth with Drizzle.

## ORMs and query builders

- Preferred default for web products: Drizzle ORM.
- Deliberate alternative: Kysely with queries written by the agent, when reducing the final bundle's weight is a goal.
- Treat bundle savings as a hypothesis to check for the target build, rather than an automatic property of switching libraries.
- Choosing Kysely requires a deliberate decision and a rigid project structure that keeps database access organized. Agree on query ownership and module boundaries before spreading queries through the application.

No legacy stack choices or replacements have been identified yet.
