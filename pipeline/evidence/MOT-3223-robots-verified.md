# MOT-3223 evidence — robots.txt unblocks GPTBot + ClaudeBot (2026-09-23 tick)

curl https://www.motorinnautogroup.com/robots.txt (from nada-mini):
- line 38: User-Agent: ClaudeBot / line 39: Allow: *
- line 41: User-Agent: GPTBot / line 42: Allow: *
- ChatGPT-User, Claude-SearchBot, OAI-SearchBot stanzas also Allow: *
- User-Agent: * block retains its specific Disallow rules unchanged.

Matches DealerOn case email (thread 1a0c550cd4cb1e40). C1: PASS. MOT-3223 marked Done.

