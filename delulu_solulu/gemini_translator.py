import google.generativeai as genai
import os
import speech_recognition as sr


# Create a PyAudio instance
# p = pyaudio.PyAudio()

# List all available input devices
# for i in range(p.get_device_count()):
#     info = p.get_device_info_by_index(i)
#     print(f"Device Index: {i}, Name: {info['name']}, Channels: {info['maxInputChannels']}")

# p.terminate()

gemini_api_key = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=gemini_api_key)

def translate_gemini(text):
    model = genai.GenerativeModel(
        model_name= "gemini-1.5-flash",
        system_instruction="You are a poet that translates everyday speech into romantic speech")

    response = model.generate_content(
        "Translate the following: " + text,
        generation_config = genai.GenerationConfig(
            max_output_tokens=100,
            temperature=0.8,
        )
    )

    return(response.text)

# Test the translator
# translate('How are you')


def real_time_translate():
    # Create a Recognizer instance
    recognizer = sr.Recognizer()

    with sr.Microphone(device_index=2) as source:
        print('Adjusting for ambient noise...', flush=True)
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for speech...", flush=True)

        try:
            while True:
                print('Listening for the next phrase...')
                audio = recognizer.listen(source,)

                try:
                    # Convert speech to text
                    text = recognizer.recognize_google(audio)
                    print(f'Recognized: {text}')

                    # Translate text into romantic speech using Gemini API
                    romantic_caption = translate_gemini(text)
                    print(f'Romantic caption: {romantic_caption}')

                except sr.UnknownValueError:
                    print('Could not understand audio.')
                except sr.RequestError as e:
                    print(f'Speech recognition service error: {e}')

        except KeyboardInterrupt:
            print('\nReal-time translation stopped.')

            
# test the transcriber
# real_time_translate()