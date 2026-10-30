# Agent Readiness: https://ai.motorinnautogroup.com

**Level 1/5 -- Basic Web Presence**

## Discoverability (3/4 passing)
- PASS robotsTxt: robots.txt exists with valid format
- PASS sitemap: sitemap.xml exists with valid structure (url: https://ai.motorinnautogroup.com/sitemap.xml, from robots txt, format: xml)
- PASS linkHeaders: Found agent-useful Link relations: api-catalog, service-desc, service-doc, describedby (relationsFound: {"rel":"api-catalog","href":"https://ai.motorinnautogroup.com/api"}, {"rel":"service-desc","href":"https://ai.motorinnautogroup.com/openapi.json"}, {"rel":"service-doc","href":"https://ai.motorinnautogroup.com/skills.txt"}, {"rel":"describedby","href":"https://ai.motorinnautogroup.com/ai.txt"}, totalLinks: 5)

## Content Accessibility (1/1 passing)
- PASS markdownNegotiation: Site supports Markdown for Agents (contentType: text/markdown; charset=utf-8)

## Bot Access Control (1/2 passing)
- PASS robotsTxtAiRules: Found rules for AI bots: gptbot, oai-searchbot, google-extended, perplexitybot, claudebot, claude-searchbot (targetPath: /, robotsStatus: ok, botPolicies: {"userAgent":"gptbot","effectiveAccess":"disallowed","ruleSource":"explicit","rules":[{"directive":"disallow","pattern":"/"}],"matchedRule":{"directive":"disallow","pattern":"/"}}, {"userAgent":"chatgpt-user","effectiveAccess":"allowed","ruleSource":"wildcard","rules":[{"directive":"allow","pattern":"/"},{"directive":"disallow","pattern":"/__health"},{"directive":"disallow","pattern":"/__cache"}],"matchedRule":{"directive":"allow","pattern":"/"}}, {"userAgent":"oai-searchbot","effectiveAccess":"allowed","ruleSource":"explicit","rules":[{"directive":"allow","pattern":"/"}],"matchedRule":{"directive":"allow","pattern":"/"}}, {"userAgent":"google-extended","effectiveAccess":"disallowed","ruleSource":"explicit","rules":[{"directive":"disallow","pattern":"/"}],"matchedRule":{"directive":"disallow","pattern":"/"}}, {"userAgent":"ccbot","effectiveAccess":"allowed","ruleSource":"wildcard","rules":[{"directive":"allow","pattern":"/"},{"directive":"disallow","pattern":"/__health"},{"directive":"disallow","pattern":"/__cache"}],"matchedRule":{"directive":"allow","pattern":"/"}}, {"userAgent":"anthropic-ai","effectiveAccess":"allowed","ruleSource":"wildcard","rules":[{"directive":"allow","pattern":"/"},{"directive":"disallow","pattern":"/__health"},{"directive":"disallow","pattern":"/__cache"}],"matchedRule":{"directive":"allow","pattern":"/"}}, {"userAgent":"claude-web","effectiveAccess":"allowed","ruleSource":"wildcard","rules":[{"directive":"allow","pattern":"/"},{"directive":"disallow","pattern":"/__health"},{"directive":"disallow","pattern":"/__cache"}],"matchedRule":{"directive":"allow","pattern":"/"}}, {"userAgent":"bytespider","effectiveAccess":"allowed","ruleSource":"wildcard","rules":[{"directive":"allow","pattern":"/"},{"directive":"disallow","pattern":"/__health"},{"directive":"disallow","pattern":"/__cache"}],"matchedRule":{"directive":"allow","pattern":"/"}}, {"userAgent":"perplexitybot","effectiveAccess":"allowed","ruleSource":"explicit","rules":[{"directive":"allow","pattern":"/"}],"matchedRule":{"directive":"allow","pattern":"/"}}, {"userAgent":"cohere-ai","effectiveAccess":"allowed","ruleSource":"wildcard","rules":[{"directive":"allow","pattern":"/"},{"directive":"disallow","pattern":"/__health"},{"directive":"disallow","pattern":"/__cache"}],"matchedRule":{"directive":"allow","pattern":"/"}}, {"userAgent":"applebot-extended","effectiveAccess":"allowed","ruleSource":"wildcard","rules":[{"directive":"allow","pattern":"/"},{"directive":"disallow","pattern":"/__health"},{"directive":"disallow","pattern":"/__cache"}],"matchedRule":{"directive":"allow","pattern":"/"}}, {"userAgent":"amazonbot","effectiveAccess":"allowed","ruleSource":"wildcard","rules":[{"directive":"allow","pattern":"/"},{"directive":"disallow","pattern":"/__health"},{"directive":"disallow","pattern":"/__cache"}],"matchedRule":{"directive":"allow","pattern":"/"}}, {"userAgent":"meta-externalagent","effectiveAccess":"allowed","ruleSource":"wildcard","rules":[{"directive":"allow","pattern":"/"},{"directive":"disallow","pattern":"/__health"},{"directive":"disallow","pattern":"/__cache"}],"matchedRule":{"directive":"allow","pattern":"/"}}, {"userAgent":"facebookbot","effectiveAccess":"allowed","ruleSource":"wildcard","rules":[{"directive":"allow","pattern":"/"},{"directive":"disallow","pattern":"/__health"},{"directive":"disallow","pattern":"/__cache"}],"matchedRule":{"directive":"allow","pattern":"/"}}, {"userAgent":"omgilibot","effectiveAccess":"allowed","ruleSource":"wildcard","rules":[{"directive":"allow","pattern":"/"},{"directive":"disallow","pattern":"/__health"},{"directive":"disallow","pattern":"/__cache"}],"matchedRule":{"directive":"allow","pattern":"/"}}, {"userAgent":"diffbot","effectiveAccess":"allowed","ruleSource":"wildcard","rules":[{"directive":"allow","pattern":"/"},{"directive":"disallow","pattern":"/__health"},{"directive":"disallow","pattern":"/__cache"}],"matchedRule":{"directive":"allow","pattern":"/"}}, {"userAgent":"claudebot","effectiveAccess":"disallowed","ruleSource":"explicit","rules":[{"directive":"disallow","pattern":"/"}],"matchedRule":{"directive":"disallow","pattern":"/"}}, {"userAgent":"claude-searchbot","effectiveAccess":"allowed","ruleSource":"explicit","rules":[{"directive":"allow","pattern":"/"}],"matchedRule":{"directive":"allow","pattern":"/"}}, {"userAgent":"claude-user","effectiveAccess":"allowed","ruleSource":"wildcard","rules":[{"directive":"allow","pattern":"/"},{"directive":"disallow","pattern":"/__health"},{"directive":"disallow","pattern":"/__cache"}],"matchedRule":{"directive":"allow","pattern":"/"}}, {"userAgent":"perplexity-user","effectiveAccess":"allowed","ruleSource":"wildcard","rules":[{"directive":"allow","pattern":"/"},{"directive":"disallow","pattern":"/__health"},{"directive":"disallow","pattern":"/__cache"}],"matchedRule":{"directive":"allow","pattern":"/"}}, botsFound: gptbot, oai-searchbot, google-extended, perplexitybot, claudebot, claude-searchbot)
- FAIL contentSignals -- Declare AI content usage preferences with Content Signals in robots.txt
  No Content Signals found in robots.txt
  **Fix:** Add Content-Signal directives to your robots.txt declaring preferences for ai-train, search, and ai-input. For example:
Content-Signal: ai-train=no, search=yes, ai-input=no
  **Skill:** https://isitagentready.com/.well-known/agent-skills/content-signals/SKILL.md
  **Spec:** https://contentsignals.org/, https://datatracker.ietf.org/doc/draft-romm-aipref-contentsignals/
- OK webBotAuth: Web Bot Auth directory not found (informational only)

## API, Auth, MCP & A2A Discovery (2/9 passing)
- PASS apiCatalog: API Catalog found with 1 API listed (apiCount: 1, linksetEntries: 1, correct content type)
- FAIL oauthDiscovery -- Publish OAuth/OIDC discovery metadata so agents can authenticate with your APIs
  No OAuth/OIDC discovery metadata found
  **Fix:** If your site has protected APIs, publish /.well-known/openid-configuration (for OpenID Connect) or /.well-known/oauth-authorization-server (for pure OAuth 2.0) with your issuer, authorization_endpoint, token_endpoint, jwks_uri, and grant_types_supported. This allows AI agents to programmatically discover how to authenticate.
  **Skill:** https://isitagentready.com/.well-known/agent-skills/oauth-discovery/SKILL.md
  **Spec:** http://openid.net/specs/openid-connect-discovery-1_0.html, https://www.rfc-editor.org/rfc/rfc8414
- FAIL oauthProtectedResource -- Publish OAuth Protected Resource Metadata so agents can discover how to authenticate
  No OAuth Protected Resource Metadata found
  **Fix:** Publish /.well-known/oauth-protected-resource with your resource identifier, authorization_servers (list of OAuth/OIDC issuer URLs that can issue tokens for this resource), and scopes_supported. This tells agents how to obtain access tokens for your protected APIs. You can also return a WWW-Authenticate header with a resource_metadata parameter on 401 responses to enable dynamic discovery.
  **Skill:** https://isitagentready.com/.well-known/agent-skills/oauth-protected-resource/SKILL.md
  **Spec:** https://www.rfc-editor.org/rfc/rfc9728
- FAIL authMd -- Publish Auth.md metadata for agent registration
  auth.md returned status 502
  **Fix:** Serve /auth.md at the site root with agent registration instructions, publish /.well-known/oauth-protected-resource, and include an agent_auth block in /.well-known/oauth-authorization-server with register_uri, supported identity types, credential types, and claim/revocation URLs where applicable.
  **Skill:** https://isitagentready.com/.well-known/agent-skills/auth-md/SKILL.md
  **Spec:** https://workos.com/auth-md, https://github.com/workos/auth.md
- PASS mcpServerCard: MCP Server Card found at /.well-known/mcp.json (path: /.well-known/mcp.json, format: registry, name: Motor Inn Auto Group, has version, has description, has remotes, has name, has schema, mcpProbeStatus: skipped)
- FAIL a2aAgentCard -- Publish an A2A Agent Card for agent-to-agent discovery
  A2A Agent Card not found
  **Fix:** Serve an A2A Agent Card (JSON) at /.well-known/agent-card.json describing your agent. Include name, version, description, supportedInterfaces (with service URL and transport protocol), capabilities, and skills (each with id, name, description). This enables other AI agents to discover and interact with your agent via the A2A protocol.
  **Skill:** https://isitagentready.com/.well-known/agent-skills/a2a-agent-card/SKILL.md
  **Spec:** https://a2a-protocol.org/latest/specification/, https://a2a-protocol.org/latest/topics/agent-discovery/
- FAIL agentSkills -- Publish an agent skills discovery index
  Agent Skills index not found
  **Fix:** Publish a skills discovery index at /.well-known/agent-skills/index.json (per the Agent Skills Discovery RFC v0.2.0). Include a $schema field, and a skills array where each entry has name, type ("skill-md" or "archive"), description, url, and a sha256 digest for integrity verification.
  **Skill:** https://isitagentready.com/.well-known/agent-skills/agent-skills/SKILL.md
  **Spec:** https://github.com/cloudflare/agent-skills-discovery-rfc, https://agentskills.io/
- FAIL ard -- Publish an ARD (Agentic Resource Discovery) manifest so agents can discover your site's capabilities (MCP servers, A2A agents, OpenAPI schemas, and more)
  ARD capability manifest not found
  **Fix:** Serve /.well-known/ai-catalog.json at the origin root with Content-Type: application/json and Access-Control-Allow-Origin: *. Include specVersion, a host object, and an entries array. Give each entry a urn:air:<your-domain>:<namespace>:<name> identifier, a displayName, an IANA media type in "type", and exactly one of url or data. Add 2-5 representativeQueries per entry so registries can build semantic embeddings, and a trustManifest when you need verifiable publisher identity.
  **Skill:** https://isitagentready.com/.well-known/agent-skills/ard/SKILL.md
  **Spec:** https://agenticresourcediscovery.org/, https://github.com/ards-project/ard-spec, https://github.com/Agent-Card/ai-catalog
- INFO personalAgentProtocol (informational, not scored) -- Personal Agent Protocol (Poppy) discovery and OAuth issuer binding
  Personal Agent Protocol manifest not found
  **Skill:** https://isitagentready.com/.well-known/agent-skills/personal-agent-protocol/SKILL.md
  **Spec:** https://personalagentprotocol.org/docs/spec#3-discovery

## Commerce (0/0 passing)
- OK x402: x402 payment protocol not detected (not a commerce site)
- OK mpp: MPP payment discovery not detected (not a commerce site)
- OK ucp: UCP profile not found (not a commerce site)
- OK acp: ACP discovery document not found (not a commerce site)
- OK ap2: AP2 not detected (no A2A Agent Card) (not a commerce site)

## Unable to Check (2)
- dnsAid: Could not reliably determine DNS for AI Discovery (DNS-AID) support: DNS query returned SERVFAIL
- webMcp: Could not check WebMCP: net::ERR_CONNECTION_RESET at https://ai.motorinnautogroup.com
