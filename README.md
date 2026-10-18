# AMOS / ClickFix macOS attack: samples and analysis

De-obfuscated samples and analysis of a ClickFix attack that delivered the AMOS
(Atomic macOS Stealer) backdoor via an EtherHiding loader. Kept for education and
defense. Full write-up: https://richardkovacs.dev/blog/reverse-engineering-malware-with-my-ai-agent

> **Warning: this is real malware. Do not run any of it.**
> The scripts are saved as `.txt` so macOS does not treat them as executable
> AppleScript. Read them in a text editor only. Do not run them through
> `osascript`/`osacompile`, open them in Script Editor, or double-click them;
> doing so makes macOS quarantine the file. Everything here is provided as-is,
> with no warranty. The author is not liable for any misuse.

## The attack

1. **Typosquat.** The victim mistyped `admin.atlassion.com` (an `o` for the `a`
   in `atlassian`) and landed on a lookalike page.
2. **ClickFix.** A fake "device verification" step told the victim to paste a
   base64 one-liner into a terminal. Decoded, it ran `update.sh`.
3. **Persistence.** `update.sh` installs a launchd agent (`com.ntpebadwvugmokrc`)
   with `RunAtLoad` and `KeepAlive`, so the chain restarts on login and after
   any kill.
4. **Loader (layer 2).** Reads the current C2 (command-and-control) domain from a Polygon smart
   contract (EtherHiding), downloads layer 3 from it, and runs it in memory.
   Hiding the address on-chain lets the operator rotate C2 domains without
   touching infected machines.
5. **Backdoor (layer 3).** Fingerprints the Mac, shows a fake "System
   Preferences" password dialog until a correct password is entered, registers
   the machine with the C2, then polls every 60 seconds for tasks: a stealer, a
   light stealer, a Ledger Live replacer, or a remote shell.

The victim never entered a password, so the gate never opened and nothing was
stolen. The four task payloads (layer 4) were never delivered and are not here.

## Files

The malware samples are in **`samples-encrypted.zip`**, a password-protected
archive so they are not scanned, indexed, or run by accident. The password is in
the [blog post](https://richardkovacs.dev/blog/reverse-engineering-malware-with-my-ai-agent), not in
this repo. Inside, each script has up to three versions: `raw` (as served),
`decoded` (mechanically de-obfuscated), and `annotated` (renamed and commented
for reading):

- `update.sh.{raw,decoded}.txt` — layer 1, installs the launchd agent
- `com.ntpebadwvugmokrc.plist.txt` — the launchd agent it writes
- `layer2.{raw,decoded,annotated}.txt` — loader: resolves the C2 and fetches layer 3
- `layer3.{raw,decoded,annotated}.txt` — backdoor: password gate, registration, task loop

The rest of the repo is in the clear:

| File | What it is |
|---|---|
| `samples-encrypted.zip` | The malware samples (password in the blog post) |
| `deobfuscate.py` | Reverses the character-code obfuscation in layers 2 and 3 |
| `heimdall/` | The decompiled Polygon contract |
| `show_fake_dialog.applescript` | Harmless reproduction of the fake dialog, for screenshots |
| `IOCS.md` | Indicators of compromise |
| `c2_rotation_history.txt` | Every C2 domain the contract has pointed to |
| `c2_history.py` | Rebuilds that history from public chain state (read-only) |

## Resolve the current C2

The live C2 domain is stored on-chain and can be read for free from any public
Polygon node. This only reads the blockchain; it never contacts the C2.

```bash
curl -s https://polygon.publicnode.com -X POST -H 'Content-Type: application/json' --data '{"jsonrpc":"2.0","method":"eth_call","params":[{"to":"0xA3a603F8a454a9c905b4c579Bb72628F7C15C2A0","data":"0x2686ecea"},"latest"],"id":1}' | sed -n 's/.*"result":"0x\([^"]*\)".*/\1/p' | (read h; l=$(printf "%d" "0x${h:64:64}"); echo "${h:128:$((l*2))}" | xxd -r -p); echo
```

For the full history of every domain the contract has pointed to, run
`python3 c2_history.py`. It discovers the contract's whole lifetime from chain
state, so it stays current as the attacker rotates domains, with no edits needed.

## License

The analysis and tooling (`deobfuscate.py`, `c2_history.py`, the docs) are MIT
licensed; see `LICENSE`. The malware samples are the attacker's own code,
included unmodified for research, and are not covered by that license.
