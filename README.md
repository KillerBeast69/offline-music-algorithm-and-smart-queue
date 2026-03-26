# Offline Music Algorithm & Smart Queue: Auto-Tagger

This project is the foundational data-ingestion engine for a custom offline "Smart Queue" music player. It automatically scans a directory of raw, untagged `.mp3` files (such as YouTube rips or basic downloads), aggressively scrubs the filenames to remove internet noise, fetches pristine metadata from the MusicBrainz API, and permanently embeds standard ID3 tags directly into the audio files.

## Features

* **Intelligent Filename Scrubber:** Automatically uses Regex to strip out unwanted noise from filenames, including things like `(Official Video)`, `ft. Artist`, and underscores, ensuring clean API queries.
* **MusicBrainz Integration:** Connects to the open-source MusicBrainz database to download highly accurate metadata, including Title, Artist, Album, Year, Track Number, and acoustic genres/tags.
* **ID3 Auto-Tagging:** Uses `mutagen` to seamlessly inject the downloaded metadata directly into the `.mp3` files for permanent offline use.
* **Batch Processing:** Iterates over an entire directory of music, identifying and tagging files automatically.
* **Lightning Fast Management:** Powered by `uv` for instant dependency management and execution without the hassle of manual virtual environments.

## Prerequisites

This project uses [uv](https://github.com/astral-sh/uv), the modern, wildly fast Python package manager written in Rust.

If you don't have `uv` installed, install it system-wide (Arch Linux example):

    sudo pacman -S uv

## Project Structure

Ensure your project matches this directory structure before running:

    offline_music_algorithm_and_smart_queue/
    ├── audio/                   # Drop your untagged .mp3 files here
    ├── read/                    
    │   └── indexer.py           # The main scraping and tagging engine
    ├── .gitignore               
    ├── pyproject.toml           # uv project configuration
    └── README.md

## Installation

1. Clone the repository:

    git clone https://github.com/yourusername/offline_music_algorithm_and_smart_queue.git
    cd offline_music_algorithm_and_smart_queue

2. Let `uv` handle the setup. You don't need to manually create a virtual environment or run `pip install`. `uv` will read the `pyproject.toml` and lock files automatically on the first run.

## Usage

1. **Prepare your audio:** Place your untagged `.mp3` files into the `audio/` directory. For best results, files should be formatted as `Artist - Title.mp3` (though the scrubber will attempt to handle edge cases).
2. **Run the indexer:**

    uv run read/indexer.py

3. Watch the terminal as the script scrubs the names, queries MusicBrainz, and injects the tags. You can verify the success by checking the file properties in your OS.

## How it Works

1. **The Scrubber:** The script reads a file like `Drake - Not You Too (Audio) ft. Chris Brown.mp3`. It splits it at the hyphen, then scrubs the strings to extract a clean Artist (`Drake`) and Title (`Not You Too`).
2. **The API:** It pings the MusicBrainz API with those clean strings and retrieves a comprehensive JSON dictionary of the track's official release data.
3. **The Tagger:** It maps the JSON data to standard EasyID3 tags, establishes fallbacks to prevent empty fields, and permanently saves the `mutagen` object back to the hard drive.

## Next Steps (Roadmap)
* Extract acoustic features (Tempo/BPM, Energy, Danceability) using librosa or a similar audio analysis library.
* Build the Smart Queue algorithm to group tracks logically for seamless offline playback.
