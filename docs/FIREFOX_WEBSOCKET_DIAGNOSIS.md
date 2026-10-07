# Firefox WebSocket diagnosis — 2026-10-07

Measured root cause: server compression configuration rejected Firefox's valid bare `permessage-deflate` extension offer. Browser security, TLS, and the public proxy did not require weakening.

Evidence before correction:

- `/tmp/rdsh-firefox-net.moz_log` lines 3701–3713 show `GET /ws HTTP/1.1`, matching public Host/HTTPS Origin, WebSocket version 13, and `Sec-WebSocket-Extensions: permessage-deflate`.
- Lines 3773–3790 show HTTP 400, Content-Length 55, TLS destination port 443, and upgrade failure.
- Replaying the logged headers with curl against both HTTPS public `/ws` and HTTP loopback `127.0.0.1:3000/ws` returned the identical 55-byte body: `Invalid or unacceptable Sec-WebSocket-Extensions header`.
- Local installed `node_modules/ws/lib/permessage-deflate.js` `acceptAsServer` rejects an extension offer without `client_max_window_bits` when the server has numeric `clientMaxWindowBits` configured. The server had set that option to 15.

This direct loopback reproduction excludes Funnel/TLS transport as the cause of the measured HTTP 400. It does not depend on whether the installed native Firefox and Playwright Firefox use the same build; the actual logged Firefox offer was replayed byte-for-byte at the header level. Native Firefox 157 is available, but native interaction was not needed after this decisive reproduction. Earlier browser console `ws://` wording alone was insufficient evidence for an insecure URL: the network log proves secure port 443 with correct HTTPS Origin.

Correction: remove explicit `clientMaxWindowBits: 15`. Preserve `serverMaxWindowBits: 15`, both no-context-takeover flags, threshold 1024, zlib memLevel 7, concurrency limit 4, 16 KB decompressed payload limit, connection cap and message rate cap. [RFC 7692 sections 7.1.2.2 and 7.1.3](https://www.rfc-editor.org/rfc/rfc7692.html#section-7.1.2.2) defines the bare offer as valid, forbids a response client-window parameter unless the offer included it, and gives an absent client-window parameter the normal 32,768-byte maximum sliding window.

Verification: `node --test tests/server.test.js` passes 12 tests. The new regression sends the exact bare offer with a raw HTTP upgrade request and receives HTTP 101 with permessage-deflate, both no-context-takeover flags, server window 15 and no unoffered client-window parameter. This is a handshake regression; the parent performs Firefox/Chromium production gameplay acceptance after restarting the server. The diagnostic agent did not restart production or change proxy/network/browser settings.
