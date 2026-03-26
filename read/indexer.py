import mutagen
import musicbrainzngs
import re
from mutagen.easyid3 import EasyID3
from pathlib import Path

# setup music brainz
musicbrainzngs.set_useragent(
    app = "SmartQueueAlgorithm",
    version = "0.1",
    contact = "test@example.com"
)

# scrubber
def clean_text(text):
    if not text:
        return ""
    
    # remove anything inside parantheses () or brackets []
    text = re.sub(r'[\(\[].*?[\)\]]', '', text)

    # remove "ft" or "feat" and any names after it
    text = re.sub(r'(?i)\b(ft\.|feat\.|feat|ft)\b.*', '', text)

    # remove underscores
    text = text.replace("_", " ")

    # remove extra weird spaces left behind
    return " ".join(text.split())

# scrap the music data
def fetch_meta_data(artist_name, track_title):
    print(f"\n\nScraping data for: {artist_name or 'unknown artist'} - {track_title}")
    try:
        query = {"recording": track_title, "limit":  1}
        if artist_name:
            query["artist"] = artist_name

        result = musicbrainzngs.search_recordings(**query)

        if not result.get("recording-list"):
            return None
        return result["recording-list"][0]
    except Exception as e:
        print(f"Scrapper error: {e}")
        return None

# tag the file
def tag_audio_file(audio_file, artist_name, track_title):
    match = fetch_meta_data(artist_name, track_title)

    if match:
        print("\nInjecting tags into MP3...")

        # load the mp3 tags or create empty ones if they dont exist at all

        try:
            tags = EasyID3(audio_file)

        except mutagen.id3.ID3NoHeaderError:
            tags = mutagen.File(audio_file, easy = True)
            tags.add_tags()

        # safely extract data with fallbacks
        tags["title"] = match.get("title", track_title)
        tags["artist"] = match.get("artist-credit-phrase", artist_name or "unknown artist")

        # dig into the release list for album and year
        if "release-list" in match:
            release = match["release-list"][0]
            tags["album"] = release.get("title", "unknown album")
            tags["date"] = release.get("date", "0000")[:4]

            # dig deeper for track number
            try:
                tags["tracknumber"] = release["medium-list"][0]["track-list"][0]["number"]
            except (KeyError, IndexError):
                pass
            
            # format the generes
        if "tag-list" in match:
            generes = [tag["name"] for tag in match["tag-list"]]
            tags["genre"] = ", ".join(generes)

        tags.save()
        print(f"Success! '{audio_file.name}' is tagged.\n")
    else:
        print(f"could not find meta data for '{audio_file.name}'\n")

def process_audio_dir():
    current_dir = Path(__file__).parent
    audio_dir = current_dir.parent / "audio"

    if not audio_dir.exists():
        print(f"Error: could not find directory {audio_dir}")
        return
    
    print(f"scanning directory: {audio_dir}")

    for audio_file in audio_dir.glob("*.mp3"):
        filename = audio_file.stem

        if "-" in filename:
            parts = filename.split("-", 1)
            raw_artist = parts[0]
            raw_title = parts[1]
        else:
            raw_artist = ""
            raw_title = filename

        clean_artist = clean_text(raw_artist)
        clean_title = clean_text(raw_title)

        tag_audio_file(audio_file, clean_artist, clean_title)
        get_meta_data(audio_file)

def get_meta_data(audio_file):
    audio = mutagen.File(audio_file)

    if audio is not None:
        # technical metadata
        # fhe "info" object contains data about the audio stream itself
        print("--- Technical info ----")
        print(f"Duration: {audio.info.length:.2f} seconds")
        print(f"Bitrate: {audio.info.bitrate} bps")
        print(f"Sample Rate: {audio.info.sample_rate} Hz")

        # tag metadata
        # the tag objects behaves like a dictionary containing the meta data
        print("\n--- Audio tags ---")
        if audio_file.suffix.lower() == ".mp3":
            mp3_tags = EasyID3(audio_file)
            for key, value in mp3_tags.items():
                print(f"{key.capitalize()}: {value[0]}")
            
        else:
            for key, value in audio.tags.items():
                print(f"{key.capitalize()}: {value[0]}")

    else:
        raise Exception("Could not read the file. Ensure path is correct and the format is supported")

if __name__ == "__main__":
    process_audio_dir()