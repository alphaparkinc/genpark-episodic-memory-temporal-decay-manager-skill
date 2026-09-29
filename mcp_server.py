import sys
import json
from client import TemporalDecayMemory

mem = TemporalDecayMemory()

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-episodic-memory-temporal-decay-manager-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "store_episodic_memory",
                        "description": "Store memory item with initial importance weighting",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "content": {"type": "string"},
                                "importance": {"type": "number", "default": 1.0}
                            },
                            "required": ["content"]
                        }
                    },
                    {
                        "name": "retrieve_active_memories",
                        "description": "Retrieve memories that exceed retention decay threshold",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "threshold": {"type": "number", "default": 0.3}
                            }
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "store_episodic_memory":
            c = args.get("content", "")
            imp = args.get("importance", 1.0)
            mem.store(c, imp)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": "Stored"}]}}
        elif tool_name == "retrieve_active_memories":
            th = args.get("threshold", 0.3)
            items = mem.retrieve_active(threshold=th)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(items)}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
