import requests

def get_ios_app_icon(bundle_id):
    fallback_countries = ['US', 'JP', 'GB', 'CA', 'DE', 'FR']

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
                    return icon_url
        except Exception as e:
            print(f"⚠️ Error querying {country}: {e}")

    print(f"❌ No icon found for {bundle_id} in any region.")
    return None