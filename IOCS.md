# IOCs — ClickFix / AMOS incident, 2026-09-17

| Type | Value |
|---|---|
| Phishing domain | admin.atlassion.com |
| Loader URL | https://deltaten.drchristian.mx/update.sh |
| C2 hostname (resolved 2026-09-17 19:xx CEST) | jse8x92s.me |
| **EtherHiding contract (Polygon mainnet)** | **0xA3a603F8a454a9c905b4c579Bb72628F7C15C2A0** |
| Contract call selector | 0x2686ecea (eth_call, returns ABI-encoded string = current C2 host) |
| **Contract owner wallet (operator)** | **0x363aeaf1f67f1fb7abddc3f9806a301f1c64abe3** — deployed the contract, sole account allowed to set the C2 URL; EIP-7702 delegated to MetaMask EIP-7702 Delegator 0x63c0c19a282a1b52b07dd5a65b58948a07dae32b since block 93296359 (2026-09-05); hidden URL writes routed via MetaMask Delegation Manager 0xdb9b1e94b5b69df7e401ddbede43491141047db3. Full history: `c2_rotation_history.txt` |
| Public RPC nodes abused | polygon.drpc.org, polygon.publicnode.com, polygon-mainnet.gateway.tatum.io, tenderly.rpc.polygon.community |
| Campaign / victim id (txid) | e403efec56aa48f19dafce33977ef541 |
| launchd label | com.ntpebadwvugmokrc |
| Plist path | ~/Library/LaunchAgents/com.ntpebadwvugmokrc.plist |
| Unused staging path | ~/Library/ntpebadwvugmokrc |
| Success markers (never created here) | ~/.passphrase, ~/.txid |
| Module names | bmodule (backdoor), smodule (stealer), lmodule (light stealer), ledger (Ledger Live replacer), shell (remote shell) |
| Fake dialog | title "System Preferences": "To run the application you need to change the settings for its operation. Please enter password for continue:" |

## Files in this folder

See `README.md` for the full file map (the three tiers per script, plus the
supporting files).

## Re-resolve the current C2 from the contract (read-only, public RPC, no contact with attacker)

```bash
curl -s https://polygon.publicnode.com -X POST -H 'Content-Type: application/json' --data '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0xA3a603F8a454a9c905b4c579Bb72628F7C15C2A0","data":"0x2686ecea"},"latest"],"id":1}' | sed -n 's/.*"result":"0x\([^"]*\)".*/\1/p' | (read h; l=$(printf "%d" "0x${h:64:64}"); echo "${h:128:$((l*2))}" | xxd -r -p); echo
```
