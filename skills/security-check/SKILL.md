---
name: security-check
description: Use when reviewing pending changes, branch diffs, or new features for concrete security risks, injection, auth, permissions, or attack paths.
metadata:
  private: true
  clawdbot:
    emoji: "🔴"
    requires:
      bins: ["git"]
---

# Security Check

Red-team style security review for code changes. Think like an attacker.

## Modes

### 1. Pending Changes (default)
Review uncommitted changes in the current working directory:
```bash
git diff HEAD
git diff --cached  # staged changes
```

### 2. Branch vs Main
Review all commits on a branch against main:
```bash
git log main..<branch> --oneline  # list commits
git diff main...<branch>          # three dots = merge-base diff
```

### 3. Specific Commit Range
```bash
git diff <commit1>..<commit2>
```

## Review Checklist

### Input Validation
- [ ] User input sanitized before use?
- [ ] SQL injection vectors?
- [ ] Command injection (shell escapes)?
- [ ] Path traversal (`../` in file paths)?
- [ ] XSS in HTML/JS output?
- [ ] Prototype pollution (JS objects)?

### Authentication & Authorization
- [ ] Auth checks on all sensitive endpoints?
- [ ] Permission escalation paths?
- [ ] Session handling flaws?
- [ ] Token exposure in logs/URLs?
- [ ] Missing rate limiting?

### Secrets & Configuration
- [ ] Hardcoded credentials/API keys?
- [ ] Secrets in logs or error messages?
- [ ] Insecure defaults?
- [ ] Debug mode left enabled?
- [ ] `.env` files committed?

### Data Exposure
- [ ] Sensitive data in responses?
- [ ] PII leaked in logs?
- [ ] Stack traces exposed to users?
- [ ] Internal paths/IPs revealed?

### Cryptography
- [ ] Weak algorithms (MD5, SHA1 for security)?
- [ ] Hardcoded IVs/salts?
- [ ] Predictable random values?
- [ ] Missing HTTPS enforcement?

### Dependencies
- [ ] Known vulnerable packages?
- [ ] Unpinned versions?
- [ ] Typosquatting risk?

### File Operations
- [ ] Arbitrary file read/write?
- [ ] Unsafe deserialization?
- [ ] Temp file races?
- [ ] Symlink attacks?

### Process & Network
- [ ] SSRF vectors?
- [ ] Open redirects?
- [ ] Unsafe subprocess calls?
- [ ] Missing timeouts?

## Output Format

For each finding:

```
🔴 [CRITICAL|HIGH|MEDIUM|LOW] <Title>

📍 Location: <file:line>

💀 Attack Vector:
<How an attacker would exploit this>

📝 Code:
<relevant snippet>

✅ Fix:
<suggested remediation>
```

## Workflow

1. **Identify scope** — Ask which mode (pending/branch/commit range)
2. **Get the diff** — Run appropriate git commands
3. **Analyze systematically** — Go through checklist
4. **Prioritize findings** — CRITICAL > HIGH > MEDIUM > LOW
5. **Suggest fixes** — Concrete code changes, not vague advice
6. **Summary** — Executive summary with risk assessment

## Quick Commands

```bash
# Pending changes
git diff HEAD

# Branch review
git diff main...feature-branch

# Check for secrets (basic)
git diff HEAD | grep -iE "(password|secret|api.?key|token|credential)"

# Check for dangerous functions
git diff HEAD | grep -iE "(eval|exec|system|shell_exec|passthru|popen)"
```

## Risk Levels

- **CRITICAL**: Exploitable now, high impact (RCE, auth bypass, data breach)
- **HIGH**: Likely exploitable, significant impact
- **MEDIUM**: Exploitable under specific conditions
- **LOW**: Defense-in-depth issues, minor exposure
