import asyncio, json, os
import websockets
from om1_bridge.mj_env import MJEnv

HOST = os.getenv("OM1_BRIDGE_HOST", "0.0.0.0")
PORT = int(os.getenv("OM1_BRIDGE_PORT", "8765"))
MODEL = os.getenv("OM1_MODEL", "assets/simple_arm.xml")

env = MJEnv(MODEL)
env.reset()
async def handle(ws):
    async for msg in ws:
        try:
            req = json.loads(msg)
            op = req.get("op")
            if op == "reset":
                obs = env.reset()
                await ws.send(json.dumps({"ok": True, "obs": obs}))
            elif op == "set":
                target = req.get("target", {})
                env.set_target_qpos(target)
                await ws.send(json.dumps({"ok": True}))
            elif op == "step":
                n = int(req.get("n", 1))
                obs = env.step(n)
                await ws.send(json.dumps({"ok": True, "obs": obs}))
            elif op == "state":
                await ws.send(json.dumps({"ok": True, "obs": env._obs()}))
            else:
                await ws.send(json.dumps({"ok": False, "error": "unknown op"}))
        except Exception as e:
            await ws.send(json.dumps({"ok": False, "error": str(e)}))
async def main():
    async with websockets.serve(handle, HOST, PORT):
        print(f"[bridge] running ws://{HOST}:{PORT} model={MODEL}")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
