"""Read-only cloud preflight. Never calls a YouTube write endpoint."""

import json
import os
from urllib import parse, request


def read_json_env(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing GitHub secret: {name}")
    return json.loads(value)


client = read_json_env("CUBECUT_OAUTH_CLIENT_JSON")["installed"]
saved = read_json_env("CUBECUT_YOUTUBE_TOKEN_JSON")
if client.get("project_id") != saved.get("project_id"):
    raise RuntimeError("OAuth client and token project mismatch")
if saved.get("channel_title") != "CubeCut":
    raise RuntimeError("Unexpected saved channel title")

form = parse.urlencode({
    "client_id": client["client_id"],
    "client_secret": client["client_secret"],
    "refresh_token": saved["refresh_token"],
    "grant_type": "refresh_token",
}).encode("ascii")
token_request = request.Request(
    "https://oauth2.googleapis.com/token",
    data=form,
    headers={"Content-Type": "application/x-www-form-urlencoded"},
)
with request.urlopen(token_request, timeout=30) as response:
    access_token = json.load(response)["access_token"]

query = parse.urlencode({"part": "snippet,brandingSettings,localizations", "mine": "true"})
channel_request = request.Request(
    "https://www.googleapis.com/youtube/v3/channels?" + query,
    headers={"Authorization": "Bearer " + access_token},
)
with request.urlopen(channel_request, timeout=30) as response:
    channels = json.load(response).get("items", [])
if len(channels) != 1:
    raise RuntimeError("Expected exactly one authorized YouTube channel")
channel = channels[0]
if channel["id"] != saved["channel_id"] or channel["snippet"]["title"] != "CubeCut":
    raise RuntimeError("Authorized channel is not CubeCut")
if channel.get("brandingSettings", {}).get("channel", {}).get("defaultLanguage") != "en":
    raise RuntimeError("CubeCut default language is not English")
if len(channel.get("localizations", {})) < 26:
    raise RuntimeError("CubeCut channel is missing some language localizations")

# Build the approved English example in memory, with no video and no API mutation.
title = "Avocado vs 1000 Cuts #satisfying #oddlysatisfying #asmr"
description = (
    "One avocado, six rounds: 10 → 50 → 100 → 240 → 500 → 1,000 cuts. "
    "By the final round it's about 18.4 million cubes.\n"
    "Fully 3D-animated, with original close-up cutting sound design.\n"
    "What should we cube next? Tell us in the comments 👇\n\n"
    "#satisfying #cutting #avocado #asmr #3danimation #shorts"
)
tags = (
    "avocado, avocado cutting, avocado vs 1000 cuts, CubeCut, cutting ASMR, "
    "knife ASMR, satisfying cuts, oddly satisfying, cube cutting, cubes, "
    "3D animation, shorts"
).split(", ")
if len(title) > 100 or len(",".join(tags)) > 500 or not description:
    raise RuntimeError("English metadata is invalid")
upload_body = {
    "snippet": {
        "title": title,
        "description": description,
        "tags": tags,
        "categoryId": "22",
        "defaultLanguage": "en",
    },
    "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False},
}
if upload_body["status"]["privacyStatus"] != "private":
    raise RuntimeError("Dry-run metadata is not private")

print("PASS: GitHub runner refreshed OAuth and read the expected CubeCut channel.")
print("PASS: English metadata and private-upload settings can be prepared in memory.")
print("READ ONLY: No video upload, video update, localization update, or comment request was sent.")
