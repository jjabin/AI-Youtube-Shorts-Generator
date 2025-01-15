import traceback
import logging
from Components.YoutubeDownloader import download_youtube_video
from Components.Edit import extractAudio, crop_video
from Components.Transcription import transcribeAudio
from Components.LanguageTasks import GetHighlight
from Components.FaceCrop import crop_to_vertical, combine_videos

# Set up logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s',
                   handlers=[
                       logging.FileHandler('debug.log'),
                       logging.StreamHandler()
                   ])

def main():
    try:
        url = input("Enter YouTube video URL: ")
        logging.info(f"Attempting to download video from URL: {url}")
        
        Vid = download_youtube_video(url)
        if not Vid:
            logging.error("Failed to download video")
            return

        Vid = Vid.replace(".webm", ".mp4")
        logging.info(f"Downloaded video successfully at {Vid}")

        try:
            Audio = extractAudio(Vid)
            if not Audio:
                logging.error("Failed to extract audio")
                return
            logging.info("Audio extracted successfully")

            try:
                transcriptions = transcribeAudio(Audio)
                if not transcriptions:
                    logging.error("No transcriptions generated")
                    return
                logging.info(f"Generated {len(transcriptions)} transcription segments")

                TransText = ""
                for text, start, end in transcriptions:
                    TransText += (f"{start} - {end}: {text}\n")

                try:
                    start, stop = GetHighlight(TransText)
                    if start == 0 or stop == 0:
                        logging.error("Failed to get highlight timestamps")
                        return
                    logging.info(f"Highlight section identified: {start} to {stop}")

                    Output = "Out.mp4"
                    try:
                        crop_video(Vid, Output, start, stop)
                        logging.info("Video cropped successfully")
                        
                        croped = "croped.mp4"
                        try:
                            crop_to_vertical(Output, croped)
                            logging.info("Video converted to vertical format")
                            
                            try:
                                combine_videos(Output, croped, "Final.mp4")
                                logging.info("Final video generated successfully!")
                            except Exception as e:
                                logging.error(f"Error in combining videos: {str(e)}")
                                traceback.print_exc()
                        except Exception as e:
                            logging.error(f"Error in vertical cropping: {str(e)}")
                            traceback.print_exc()
                    except Exception as e:
                        logging.error(f"Error in video cropping: {str(e)}")
                        traceback.print_exc()
                except Exception as e:
                    logging.error(f"Error in getting highlights: {str(e)}")
                    traceback.print_exc()
            except Exception as e:
                logging.error(f"Error in transcription: {str(e)}")
                traceback.print_exc()
        except Exception as e:
            logging.error(f"Error in audio extraction: {str(e)}")
            traceback.print_exc()
    except Exception as e:
        logging.error(f"Main error: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()