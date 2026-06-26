import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


HOST = "127.0.0.1"
PORT = int(os.environ.get("PORT", "8080"))
PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_MODEL = os.environ.get("DASHSCOPE_MODEL", "qwen-plus")


class AppHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PROJECT_ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-DashScope-Api-Key")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_POST(self):
        if self.path != "/api/ai-interpret":
            self.send_error(404, "Not Found")
            return
        self.handle_ai_interpret()

    def handle_ai_interpret(self):
        api_key = self.headers.get("X-DashScope-Api-Key", "").strip()
        if not api_key:
            api_key = os.environ.get("DASHSCOPE_API_KEY", "").strip()
        if not api_key:
            self.write_json(
                500,
                {
                    "error": "DASHSCOPE_API_KEY is not configured on the server."
                },
            )
            return

        length = int(self.headers.get("Content-Length", "0") or "0")
        raw_body = self.rfile.read(length)
        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except json.JSONDecodeError:
            self.write_json(400, {"error": "Invalid JSON payload."})
            return

        prompt = (payload.get("prompt") or "").strip()
        if not prompt:
            self.write_json(400, {"error": "Prompt is required."})
            return

        model = (payload.get("model") or DEFAULT_MODEL).strip() or DEFAULT_MODEL
        temperature = payload.get("temperature", 0.8)
        max_tokens = payload.get("max_tokens", 1500)

        upstream_body = json.dumps(
            {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature,
            }
        ).encode("utf-8")

        request = Request(
            "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
            data=upstream_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=60) as response:
                upstream_data = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="ignore")
            self.write_json(
                exc.code,
                {
                    "error": "DashScope request failed.",
                    "details": error_body or str(exc),
                },
            )
            return
        except URLError as exc:
            self.write_json(502, {"error": f"Upstream connection failed: {exc.reason}"})
            return
        except Exception as exc:
            self.write_json(500, {"error": f"Unexpected proxy error: {exc}"})
            return

        text = (
            upstream_data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )
        self.write_json(200, {"text": text, "raw": upstream_data})

    def write_json(self, status_code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    server = ThreadingHTTPServer((HOST, PORT), AppHandler)
    print(f"Serving on http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
