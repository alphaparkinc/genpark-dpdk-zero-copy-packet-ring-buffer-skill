import sys
import json
from client import DPDKRingBuffer

def main():
    ring = DPDKRingBuffer()
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        req = json.loads(line)
        method = req.get("method")
        params = req.get("params", {})
        if method == "enqueue_burst":
            count = ring.enqueue_burst(params.get("packets", []))
            res = {"enqueued": count}
        elif method == "dequeue_burst":
            pkts = ring.dequeue_burst(params.get("max_pkts", 4))
            res = {"dequeued": pkts}
        else:
            res = {"error": "unknown method"}
        sys.stdout.write(json.dumps({"id": req.get("id"), "result": res}) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
