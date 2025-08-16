# Security Advisory: Beyond Compare MCP

**Date:** 2025-08-13  
**Severity:** CRITICAL  
**Status:** ACTIVE

## ⚠️ Security Vulnerabilities

### 1. Remote Code Execution (Critical)
- **CVE:** PENDING
- **Affected Versions:** All versions
- **Impact:** Attackers can execute arbitrary code on the host system
- **Vulnerable Code:** `beyondcompare_mcp/server.py` (command injection in subprocess calls)
- **Fix Status:** Not fixed - Complete rewrite required

### 2. Path Traversal (Critical)
- **CVE:** PENDING
- **Affected Versions:** All versions
- **Impact:** Unauthorized file system access
- **Vulnerable Code:** `beyondcompare_mcp/core.py` (inadequate path validation)
- **Fix Status:** Not fixed - Complete rewrite required

### 3. Insecure Dependencies (High)
- **Affected Dependencies:**
  - `fastmcp>=2.10.0` (non-existent package)
  - Outdated and vulnerable transitive dependencies
- **Impact:** Supply chain attacks, dependency confusion
- **Fix Status:** Requires dependency audit and update

### 4. Insecure Default Configuration (Medium)
- **Issues:**
  - Hardcoded credentials in example configurations
  - Insecure default permissions
  - Verbose error messages
- **Impact:** Information disclosure, privilege escalation
- **Fix Status:** Requires secure configuration template

## 🔒 Mitigation

### Immediate Actions
1. **IMMEDIATELY** remove any production deployments
2. **DO NOT** use this package in any environment
3. **AUDIT** any systems that may have used this package
4. **REVOKE** any credentials/secrets that were used with this package

### For Developers
1. **DO NOT** attempt to patch individual vulnerabilities - the codebase requires complete redesign
2. **WAIT** for the official secure version (v2.0.0+)
3. **FOLLOW** the migration guide that will be provided with the secure release

## 🔄 Status

| Version | Status | Notes |
|---------|--------|-------|
| All versions < 2.0.0 | ❌ UNSAFE | Do not use |
| 2.0.0+ | ⚠️ Pending | Complete rewrite in progress |

## 📞 Contact

For security-related concerns, please contact the maintainers through GitHub issues with the `security` label.

## 📅 Timeline

- 2025-08-13: Initial security audit completed
- 2025-08-13: Security advisory published
- 2025-08-13: Repository marked as unsafe
- 2025-09-13: Planned release of secure version (v2.0.0)

## 🔍 Additional Resources

- [OWASP Top 10](https://owasp.org/Top10/)
- [Python Security Best Practices](https://snyk.io/learn/python-security/)
- [Secure Coding Guidelines for Python](https://docs.python.org/3/howto/security.html)

---

**NOTE:** This is a living document. Check back for updates as the security situation evolves.
