# Machine-hosted HTTPS playtest

Production Vite client and authoritative Node server run on this computer. A user systemd unit restarts the process on failure. Tailscale Funnel exposes ONLY this HTTP/WebSocket server on HTTPS ports 443 and 8443. Players do not need Tailscale or any installed software. No source folders, credentials, or developer server are served: the Node static root is `dist/`.

This is a real public build served over HTTPS, but it is **not an always-on cloud deployment**. The link depends on this computer being awake, connected, with its user service running. Node restart loses active rooms. User service begins with user sessions; no privileged system service or login lingering is configured.

Enable after the tested production build:
```sh
mkdir -p ~/.config/systemd/user
cp deploy/rach-doi-son-ha.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now rach-doi-son-ha.service
tailscale funnel --bg --https=443 http://127.0.0.1:3000
```
Disable only this game endpoint (preserve any other endpoints):
```sh
tailscale funnel --https=443 off
tailscale funnel --https=8443 off
systemctl --user disable --now rach-doi-son-ha.service
```

Portable cloud/container alternative in `server/Dockerfile` and `server/DEPLOY.md`. A user-provided permanent domain and hosting account can replace this transport while preserving game architecture. No hosting purchase has been made.
