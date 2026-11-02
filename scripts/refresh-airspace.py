#!/usr/bin/env python3
"""
Refresh data/airspace.js from openAIP (run every few months).

Needs:  Python 3.9+ and `pip install shapely`
Usage:  OPENAIP_KEY=your_key python3 scripts/refresh-airspace.py

Pulls Australian airspaces, airports and helipads from openAIP and keeps what
matters for drones flying near the ground:
  - restricted (R), prohibited (P) and danger (D) areas that start at the surface
  - control zones (C), shown for info
  - controlled and military airports with their runway headings (5.5 km rule)
  - helipads (1.4 km rule)
Data: openAIP, CC BY-NC 4.0 (credit stays on the map).
"""
import json, os, re, sys, time, urllib.request
from shapely.geometry import Polygon, Point

KEY = os.environ.get("OPENAIP_KEY")
if not KEY:
    sys.exit("Set OPENAIP_KEY first, e.g. OPENAIP_KEY=abc123 python3 scripts/refresh-airspace.py")

def fetch_all(kind):
    items, page = [], 1
    while True:
        req = urllib.request.Request(
            f"https://api.core.openaip.net/api/{kind}?country=AU&limit=1000&page={page}",
            headers={"x-openaip-api-key": KEY, "User-Agent": "CAS-website-refresh/1.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.load(r)
        items += d["items"]
        if not d.get("nextPage"):
            return items
        page = d["nextPage"]
        time.sleep(0.5)

airspaces = fetch_all("airspaces")
airports = fetch_all("airports")

zones, ctrs = [], []
for a in airspaces:
    low = a.get("lowerLimit", {})
    if not (low.get("value") == 0 and low.get("referenceDatum") == 0):
        continue
    kind = {1: "R", 2: "D", 3: "P", 4: "C"}.get(a["type"])
    if not kind:
        continue
    poly = Polygon(a["geometry"]["coordinates"][0])
    if not poly.is_valid:
        poly = poly.buffer(0)
    if poly.geom_type != "Polygon":
        poly = max(poly.geoms, key=lambda g: g.area)
    simple = poly.simplify(0.0015, preserve_topology=True)
    z = {"k": kind, "n": re.sub(r"\s*\[.*?\]", "", a["name"]).strip(),
         "p": [[round(y, 4), round(x, 4)] for x, y in simple.exterior.coords][:-1]}
    if "[NOTAM]" in a["name"]:
        z["notam"] = 1
    zones.append(z)
    if kind == "C":
        ctrs.append(poly)

SKIP = {"Calvin Grove", "Katherine Gorge", "Lindeman Island", "Dochra", "Nackeroo", "Hobart/Cambridge"}
EXTRA_ICAO = {"YPDN", "YBTL"}  # Darwin, Townsville (joint civil/military)
aps, helis = [], []
for a in airports:
    lon, lat = a["geometry"]["coordinates"]
    if a["type"] == 7:
        helis.append([a["name"].title(), round(lat, 4), round(lon, 4)])
        continue
    pt = Point(lon, lat)
    in_ctr = any(c.contains(pt) or c.distance(pt) < 0.01 for c in ctrs)
    if (a["type"] in (2, 3, 9) and in_ctr) or a["type"] == 5 or a.get("icaoCode") in EXTRA_ICAO:
        name = a["name"].title()
        if name in SKIP:
            continue
        rw = sorted({int(r["trueHeading"]) % 180 for r in a.get("runways", []) if r.get("trueHeading") is not None})
        if not rw and a["type"] != 5:
            continue
        aps.append({"n": name, "c": a.get("icaoCode", ""), "lat": round(lat, 4), "lon": round(lon, 4), "r": rw})

out = os.path.join(os.path.dirname(__file__), "..", "data", "airspace.js")
with open(out, "w") as f:
    f.write("/* openAIP data (CC BY-NC 4.0), refreshed " + time.strftime("%Y-%m-%d") + " */\n")
    f.write("var OAIP=" + json.dumps({"Z": zones, "A": aps, "H": helis}, separators=(",", ":")) + ";\n")
print(f"Saved {len(zones)} zones, {len(aps)} airports, {len(helis)} helipads to data/airspace.js")
