import musicbrainzngs
import json

musicbrainzngs.set_useragent(
    app = "SmartQueueAlgorithm",
    version = "0.1",
    contact = "test@example.com"
)

def fetch_all_raw_data(artist_name, track_title):
    print(f"Searching MusicBrainz for: {artist_name} - {track_title}...\n")

    try:
        result = musicbrainzngs.search_recordings(
            artist = artist_name,
            recording = track_title,
            limit = 1
        )

        if not result.get("recording-list"):
            return "No Matches Found."
        
        # extract raw dictionary for the first match
        match = result["recording-list"][0]

        # iterating and printing everything
        print("=== THE COMPLETE MUSICBRAINZ DICTIONARY ===")
        print(json.dumps(match, indent=4))
        print("===========================================\n")

        # get the musical tags (generes)
        print("=== THE MUSICAL TAGS ===")
        if "tag-list" in match:
            for tag in match["tag-list"]:
                print(f"Tag: {tag['name']} (Score: {tag.get('count', 0)})")
        else:
            print("No musical tags found for this specific recording")
        
        return match
    
    except Exception as e:
        return f"an error occurred: {e}"

if __name__ == "__main__":
    fetch_all_raw_data("Stardust", "Music Sounds Better With You")

