
## Adapter (HTTP → WS Bridge)

Run both the WebSocket bridge and the HTTP adapter:
```bash
./run_all.sh

Send a control command (degrees + steps):
curl -s -X POST http://127.0.0.1:8088/control \
  -H 'Content-Type: application/json' \
  -d '{"j1": 25, "j2": -35, "steps": 250}' | jq .

Expected response:
{
  "ok": true,
  "result": {
    "ok": true,
    "obs": {
      "qpos": [...],
      "qvel": [...],
      "time": ...
    }
  }
}



