#!/usr/bin/env python3
"""Reconstruct every C2 domain the attacker's contract has ever pointed to.

Reads only public Polygon chain state, never contacts a C2. It is self-updating:
it finds the contract's deploy block and walks the history to the latest block,
so it needs no manual list and picks up new domains on every run.

    python3 c2_history.py

How it works: the getter (selector 0x2686ecea) returns the current domain. The
blockchain keeps that value at every past block, so the script bisects the block
range wherever the value at the two ends differs, pinning each change. This finds
every distinct domain regardless of how it was written (a normal transaction to
the contract, or a hidden one via MetaMask's Delegation Manager).

Limitation: a domain that was set and then reverted to the previous value inside
a single un-bisected segment can be collapsed. Distinct domains are still all
found; only a brief flip-flop between two already-seen domains may be missed.
"""
import datetime
import json
import sys
import time
import urllib.request

NODE = "https://polygon.drpc.org"
CONTRACT = "0xA3a603F8a454a9c905b4c579Bb72628F7C15C2A0"
GETTER = "0x2686ecea"  # getServerURL()

cache = {}


def rpc(method, params):
    body = json.dumps({"jsonrpc": "2.0", "method": method, "params": params, "id": 1}).encode()
    for attempt in range(6):
        try:
            req = urllib.request.Request(
                NODE, data=body,
                headers={"Content-Type": "application/json", "User-Agent": "curl/8.7.1"},
            )
            with urllib.request.urlopen(req, timeout=30) as r:
                out = json.loads(r.read())
            if "result" in out:
                time.sleep(0.2)
                return out["result"]
        except Exception:
            pass
        time.sleep(1.0 + attempt)
    raise RuntimeError(f"rpc failed: {method} {params}")


def decode_string(hexres):
    h = hexres[2:]
    if len(h) < 128:
        return ""
    length = int(h[64:128], 16)
    return bytes.fromhex(h[128:128 + 2 * length]).decode("utf-8", "replace")


def domain_at(block):
    if block not in cache:
        cache[block] = decode_string(rpc("eth_call", [{"to": CONTRACT, "data": GETTER}, hex(block)]))
    return cache[block]


def has_code_at(block):
    return rpc("eth_getCode", [CONTRACT, hex(block)]) not in ("0x", "0x0", "")


def find_deploy_block(latest):
    """Smallest block at which the contract already has code."""
    lo, hi = 0, latest
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if has_code_at(mid):
            hi = mid
        else:
            lo = mid
    return hi


def find_change_blocks(lo, hi, out):
    """Append every block in (lo, hi] where the domain differs from the block before it."""
    if domain_at(lo) == domain_at(hi):
        return
    if hi - lo == 1:
        out.append(hi)
        return
    mid = (lo + hi) // 2
    find_change_blocks(lo, mid, out)
    find_change_blocks(mid, hi, out)


def block_date(block):
    b = rpc("eth_getBlockByNumber", [hex(block), False])
    ts = datetime.datetime.fromtimestamp(int(b["timestamp"], 16), datetime.timezone.utc)
    return ts.strftime("%Y-%m-%d %H:%M")


def main():
    latest = int(rpc("eth_blockNumber", []), 16)
    deploy = find_deploy_block(latest)
    sys.stderr.write(f"deploy block {deploy}, latest {latest}; scanning...\n")

    changes = []
    find_change_blocks(deploy, latest, changes)
    milestones = [deploy] + changes

    print(f"{'UTC date':16}  {'block':>9}  domain")
    for block in milestones:
        domain = domain_at(block)
        if domain:
            print(f"{block_date(block):16}  {block:>9}  {domain}")
    print(f"\ncurrent (block {latest}): {domain_at(latest)}")
    print(f"archival reads: {len(cache)}")


if __name__ == "__main__":
    main()
