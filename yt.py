import click
from youtube_search import YoutubeSearch
import yt_dlp
import sys
import time


def loading_screen(duration, interval=0.1):
    progress = 0
    total_ticks = duration / interval
    while progress <= 100:
        sys.stdout.write("\r")
        sys.stdout.write(f"Downloading... {progress}%")
        sys.stdout.flush()
        time.sleep(interval)
        progress = round((progress + (100 / total_ticks)) % 101, 2)
    sys.stdout.write("\n")


@click.command()
def search_video():
    """
    Search for a video on YouTube.
    """
    query = input("Enter your search query: ")

    results = YoutubeSearch(query, max_results=10).to_dict()

    for idx, result in enumerate(results, start=1):
        print(f"{idx}. {result['title']}")

    selected_index = int(input("Enter the number of the video you want to download: ")) - 1

    if 0 <= selected_index < len(results):
        selected_video = results[selected_index]
        video_id = selected_video['id']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        download_video(video_url)
    else:
        print("Invalid selection. Please try again.")


def download_video(video_url):
    """
    Download the selected video.
    """
    ydl_opts = {
        'format': 'best',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(video_url, download=True)
            print(f"\nVideo '{info_dict['title']}' downloaded successfully.")
        except Exception as e:
            print(f"Error downloading the video: {str(e)}")


if __name__ == "__main__":
    search_video()

