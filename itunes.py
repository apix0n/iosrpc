import requests
import csv
import os
import time

CACHE_FILE = "icon_cache.csv"
CACHE_TTL = 7 * 24 * 60 * 60  # 7 days in seconds

def read_icon_cache():
    cache = {}
    if not os.path.exists(CACHE_FILE):
        return cache

    now = time.time()
    updated_cache = {}

    with open(CACHE_FILE, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) != 3:
                continue
            bundle_id, icon_url, timestamp_str = row
            try:
                timestamp = float(timestamp_str)
                if now - timestamp < CACHE_TTL:
                    cache[bundle_id] = icon_url
                    updated_cache[bundle_id] = (icon_url, timestamp)
            except ValueError:
                continue

    # Rewrite only valid (non-expired) cache
    write_icon_cache(updated_cache)
    return cache

def write_icon_cache(cache):
    with open(CACHE_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        for bundle_id, (icon_url, timestamp) in cache.items():
            writer.writerow([bundle_id, icon_url, timestamp])

def get_ios_app_icon(bundle_id):
    fallback_countries = ['US', 'JP', 'GB', 'CA', 'DE', 'FR']
    raw_cache = read_icon_cache()

    if bundle_id in raw_cache:
        print(f"🗂️  Using cached icon for {bundle_id}")
        return raw_cache[bundle_id]

    for country in fallback_countries:
        url = f"https://itunes.apple.com/lookup?bundleId={bundle_id}&country={country}"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            results = data.get("results", [])
            if results:
                icon_url = results[0].get("artworkUrl100")
                if icon_url:
                    print(f"✅ Found icon for {bundle_id} in {country}: {icon_url}")
                    # Update and save cache
                    raw_cache[bundle_id] = icon_url
                    # Pass timestamps to write function
                    write_icon_cache({
                        bid: (url, time.time()) for bid, url in raw_cache.items()
                    })
                    return icon_url
        except Exception as e:
            print(f"⚠️ Error querying {country}: {e}")

    print(f"❌ No icon found for {bundle_id} in any region.")
    return None
