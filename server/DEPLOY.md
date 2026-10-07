# Portable server

Build from the repository root:

```sh
docker build -f server/Dockerfile -t rach-doi-son-ha .
docker run --rm -p 3000:3000 rach-doi-son-ha
```

Terminate HTTPS in a reverse proxy that forwards `/ws` WebSocket upgrades and the public Host header. The server rejects browser cross-origin upgrades. Caddy configuration for a domain owned by the operator:

```caddy
YOUR_DOMAIN {
    reverse_proxy 127.0.0.1:3000
}
```

`GET /health` checks liveness. Rooms are in memory and are lost on restart; use one server process for all seats in a room. No accounts or database required. `PORT` defaults to 3000; `HOST` defaults to 0.0.0.0 when run directly. Grace is 60 seconds, with simulation paused during a missing connection. Finished rooms expire after five inactive minutes. No external deployment was performed.

Capacity defaults suit a single small host: `MAX_ROOMS=8`, `MAX_CONNECTIONS=64`, `RECONNECT_SECONDS=60`. Allowed integer ranges are 1–64 rooms, 2–256 simultaneous sockets and 5–120 reconnect seconds. Missing, nonfinite, fractional or out-of-range values fall back to those defaults. Test callers may set direct `createGameServer` options including short grace windows. Host operators should benchmark their machine before increasing room capacity.
