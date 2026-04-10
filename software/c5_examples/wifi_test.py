# ESP32-C5 dual-band test on a single SSID
import machine, network, neopixel, time, esp, gc

WIFI_SSID = "SSID"
WIFI_PASS = "Password"


results = {}
def log(name, ok, info=""):
    results[name] = ok
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {info}")

def band_of(ch):
    if 1 <= ch <= 14: return "2.4GHz"
    if 32 <= ch <= 177: return "5GHz"
    return None

def mac(b): return ":".join("%02x" % x for x in b)

# --- Chip / NeoPixel / Battery (same as before) ---
try:
    log("Chip", True, f"{machine.freq()//1_000_000}MHz reset={machine.reset_cause()}")
except Exception as e: log("Chip", False, str(e))

# --- WiFi: find one BSSID per band for our SSID ---
wlan = network.WLAN(network.STA_IF)
wlan.active(False); time.sleep(0.3); wlan.active(True)

best = {"2.4GHz": None, "5GHz": None}  # (bssid, ch, rssi)
try:
    for n in wlan.scan():
        ssid = n[0].decode() if isinstance(n[0], bytes) else n[0]
        if ssid != WIFI_SSID: continue
        bssid, ch, rssi = n[1], n[2], n[3]
        b = band_of(ch)
        if b and (best[b] is None or rssi > best[b][2]):
            best[b] = (bssid, ch, rssi)
    found = [f"{b}:ch{v[1]}@{v[2]}dBm" for b,v in best.items() if v]
    log("WiFi scan", any(best.values()), f"{WIFI_SSID} -> {', '.join(found) or 'none'}")
except Exception as e:
    log("WiFi scan", False, str(e))

def test_band(band):
    tag = f"WiFi {band}"
    entry = best[band]
    if not entry:
        log(tag, False, f"no BSSID of '{WIFI_SSID}' seen on {band} — move AP closer or check radio")
        return
    bssid, ch, rssi = entry
    try: wlan.disconnect()
    except: pass
    time.sleep(0.3)
    try:
        # Connect pinned to this specific BSSID — forces the band
        wlan.connect(WIFI_SSID, WIFI_PASS, bssid=bssid)
        t = time.ticks_ms()
        while not wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), t) > 20000:
                raise OSError("assoc timeout")
            time.sleep(0.2)
        try: assoc_ch = wlan.config('channel')
        except: assoc_ch = ch
        ok = band_of(assoc_ch) == band
        log(tag, ok, f"bssid={mac(bssid)} ch{assoc_ch} IP={wlan.ifconfig()[0]}")
    except Exception as e:
        log(tag, False, str(e))
    finally:
        try: wlan.disconnect()
        except: pass

test_band("2.4GHz")
test_band("5GHz")
wlan.active(False)

gc.collect()
log("Memory", True, f"free={gc.mem_free()}")

print("\n=== SUMMARY ===")
all_ok = all(results.values())
for k,v in results.items(): print(f"  {k}: {'OK' if v else 'FAIL'}")
print("RESULT:", "ALL PASS ✓" if all_ok else "FAILURES ✗")
