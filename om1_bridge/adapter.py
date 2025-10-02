from http.server import BaseHTTPRequestHandler, HTTPServer
import json, os
import asyncio, websockets

WS_URI = f"ws://{os.getenv('OM1_BRIDGE_HOST','127.0.0.1')}:{int(os.getenv('OM1_BRIDGE_PORT','8765'))}"

class Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        self.send_response(code)
        self.send_header("Content-Type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_POST(self):
        if self.path != "/control":
            return self._send(404, {"ok": False, "error": "not found"})
        try:
            ln = int(self.headers.get("Content-Length","0"))
            body = self.rfile.read(ln)
            data = json.loads(body or "{}")

            j1 = float(data.get("j1", 0))
            j2 = float(data.get("j2", 0))
            steps = int(data.get("steps", 200))

            async def go():
                async with websockets.connect(WS_URI) as ws:
                    await ws.send(json.dumps({"op":"reset"})); await ws.recv()
                    await ws.send(json.dumps({"op":"set","target":{"j1":j1,"j2":j2}})); await ws.recv()
                    await ws.send(json.dumps({"op":"step","n":steps}))
                    return json.loads(await ws.recv())

            obs = asyncio.run(go())
            return self._send(200, {"ok": True, "result": obs})

        except Exception as e:
            return self._send(400, {"ok": False, "error": str(e)})

def run_http(host="0.0.0.0", port=int(os.getenv("OM1_HTTP_PORT","8088"))):
    httpd = HTTPServer((host, port), Handler)
    print(f"[adapter] HTTP listening on http://{host}:{port}  -> WS {WS_URI}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_http()
