from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import sys

diag = {}


class Simulator(BaseHTTPRequestHandler):
    def do_GET(self):
        return self.do_POST()

    def do_POST(self):
        if self.path != "/commonCommand":
            return self.send_error(404)

        length = int(self.headers.get("content-length") or 0)
        body = json.loads(self.rfile.read(length).decode("utf-8"))
        if body.get("protocolVersion") != "1.0" or body.get("source") != 2:
            return self.send_error(400)

        command = body.get("command")
        return getattr(self, command)(command, body)

    def respond(self, command, response):
        data = {"command": command, "protocolVersion": "1.0.0"}
        data.update(response)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def ping(self, command, request):
        self.respond(command, {"status": 0})

    def getConfiguration(self, command, request):
        self.respond(command, diag["data"]["config"])

    def getStatus(self, command, request):
        dest = str(request["destinations"].pop())
        self.respond(command, diag["data"]["dests"][dest]["status"])

    def action(self, command, request):
        actions = request["actions"]
        for action in actions:
            actionId = int(action["actionId"])
            destinationId = int(action["destinationId"])
            dest = str(action["destinationId"])
            details = diag["data"]["dests"][dest]["status"]["details"]
            for detail in details:
                if detail["destinationId"] == destinationId:
                    data = detail["data"]["productData"]
                    for item in data:
                        if item["actionId"] == actionId:
                            item["value"].update(action["parameters"])
        self.respond(command, {"status": 0})


def main(server_class=HTTPServer, handler_class=Simulator):
    if len(sys.argv) != 2:
        print("Usage: python simulator.py <file>")
        sys.exit(1)

    if not os.path.isfile(sys.argv[1]):
        print(f"File {sys.argv[1]} not found")
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        global diag
        diag = json.load(f)

    server_address = ("", 80)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
