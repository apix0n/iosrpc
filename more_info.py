info = {
    "com.sega.pjsekai": "Hatsune Miku: Colorful Stage",
}

def get_custom_info(bundle_id):
    if bundle_id in info:
        return info[bundle_id]
    return None