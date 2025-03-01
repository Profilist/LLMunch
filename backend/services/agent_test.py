import asyncio
import speech_recognition as sr
from agent import YoutubeService

async def get_voice_input(recognizer: sr.Recognizer, source: sr.Microphone) -> str:
    """Get voice input from the user and convert it to text."""
    try:
        # Listen for audio input
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        # Convert speech to text
        text = recognizer.recognize_google(audio)
        print(f"Heard: {text}")  # Feedback what was heard
        return text.lower()
    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        print("Could not understand audio, please try again")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""

async def listen_for_commands():
    """Continuously listen for the trigger word and commands."""
    service = YoutubeService()
    recognizer = sr.Recognizer()
    
    print("Listening for trigger word 'Max'...")
    print("Example commands:")
    print("- 'Max I want to watch funny cat videos'")
    print("- 'Max play some relaxing music'")
    print("- 'Max show me cooking tutorials'")
    
    try:
        with sr.Microphone() as source:
            # Initial adjustment for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            while True:
                text = await get_voice_input(recognizer, source)
                
                if text.startswith("max"):
                    print("Command recognized!")
                    # Get everything after "max"
                    request = text[3:].strip()
                    
                    if request:
                        print(f"Processing request...")
                        try:
                            result = await service.play_video(request)
                            if result["status"] == "success":
                                print(f"Playing video... Search query used: {result['data']['search_query']}")
                            else:
                                print(f"Error: {result['message']}")
                        except Exception as e:
                            print(f"Error processing request: {e}")
                    else:
                        print("Waiting for video request...")
                        # Listen for the actual command
                        text = await get_voice_input(recognizer, source)
                        if text:
                            try:
                                result = await service.play_video(text)
                                if result["status"] == "success":
                                    print(f"Playing video... Search query used: {result['data']['search_query']}")
                                else:
                                    print(f"Error: {result['message']}")
                            except Exception as e:
                                print(f"Error processing request: {e}")
                
                # Brief pause to prevent CPU overuse
                await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping voice command listener...")
    finally:
        await service.close_browser()

if __name__ == "__main__":
    asyncio.run(listen_for_commands())