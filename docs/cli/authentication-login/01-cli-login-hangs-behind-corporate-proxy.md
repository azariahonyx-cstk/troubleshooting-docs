---
title: "CLI Login Hangs Indefinitely Behind a Corporate Proxy"
slug: "cli-login-hangs-behind-corporate-proxy"
pod: "CLI"
section: "Authentication & Login"
order: 1
meta_title: "CLI Login Hangs Behind a Corporate Proxy | Contentstack"
meta_description: "Resolve CLI login commands that hang indefinitely with no error on corporate networks by configuring the HTTPS_PROXY environment variable."
status: "draft"
source_case_id: "00099005"
contentstack_parent_entry_uid: null
contentstack_category_heading: null
migrated_from: null
migrated_on: null
---

# CLI Login Hangs Indefinitely Behind a Corporate Proxy

CLI login hangs indefinitely with no error message when run from a network that requires a corporate proxy for outbound traffic.

## Root cause

The CLI's login flow attempts to reach the auth server directly, bypassing the corporate HTTP proxy required for outbound traffic on networks that mandate one. Because the direct connection attempt is silently blocked, the login command hangs with no error returned to the user.

## Resolution

1. Set the `HTTPS_PROXY` environment variable to point to your corporate proxy.
2. Run the CLI login command again.

## Verification

After completing these steps, confirm the issue no longer occurs. If it persists, escalate with relevant details (logs, version, screenshots, configuration) to Contentstack support.
