from deep_translator import GoogleTranslator
import random
import sys
import time  # Added import for sleep function

def get_selected_languages(num_languages=None):
    # List of 25 specific languages with their codes
    languages = [
        ("en", "English"),
        ("zh-CN", "Mandarin Chinese"),
        ("es", "Spanish"),
        ("fr", "French"),
        ("ar", "Modern Standard Arabic"),
        ("pt", "Portuguese"),
        ("id", "Indonesian"),
        ("de", "German"),
        ("tr", "Turkish"),
    ]
    
    # If num_languages is specified and valid, take only the top languages
    if num_languages and isinstance(num_languages, int) and num_languages > 0:
        # Ensure we don't try to take more languages than available
        num_languages = min(num_languages, len(languages))
        languages = languages[:num_languages]
    
    # Return just the language codes
    return [lang[0] for lang in languages]

def translation_cycle(text, num_languages=None, num_cycles=1):
    languages = get_selected_languages(num_languages)
    
    print(f"Using {len(languages)} languages for translation")
    
    current_text = text
    previous_language = 'en'  # Assume initial text is English

    for cycle in range(num_cycles):
        print(f"Starting translation cycle {cycle + 1}/{num_cycles}")
        # Shuffle languages to get different translation paths each time
        # random.shuffle(languages)
        
        for lang_code in languages:
            # Skip translating to the same language as the previous one if it's not English
            # (or if it's the first step and previous_language is 'en' but lang_code is also 'en')
            if lang_code == previous_language and lang_code != 'en':
                print(f"Skipping translation from {previous_language} to {lang_code} (same language)")
                continue
            
            try:
                # Translate from current language to the next language
                print(f"Translating from {previous_language} to {lang_code}...")
                translator = GoogleTranslator(source=previous_language, target=lang_code)
                translated_chunk = translator.translate(current_text)

                if translated_chunk is None:
                    print(f"Warning: Translation to {lang_code} returned None. Skipping this step.")
                    # Optionally, decide if previous_language should change or not.
                    # For now, it remains the same, and we try the next language with the same source.
                    continue
                
                current_text = translated_chunk
                previous_language = lang_code  # Update previous_language after successful translation
                print(f"Successfully translated to {lang_code}")
                # time.sleep(0.5)  # 0.5 second delay between API calls
            except Exception as e:
                print(f"Error translating from {previous_language} to {lang_code}: {str(e)}")
                # previous_language remains unchanged, so the next attempt will use the last known good source language
                print(f"Continuing with {previous_language} as source for next attempt.")
                continue
    
    # Finally translate back to English
    try:
        print(f"Translating final text from {previous_language} back to English...")
        translator = GoogleTranslator(source=previous_language, target='en')
        result = translator.translate(current_text)
        if result is None:
            print("Warning: Final translation back to English returned None. Returning last translated text.")
            return current_text
        return result
    except Exception as e:
        print(f"Error translating back to English from {previous_language}: {str(e)}")
        return current_text # Return the last successfully translated text if final translation fails

def main():
    # Default number of languages
    num_languages = 24
    
    # Check if number of languages was specified as command line argument
    if len(sys.argv) > 1:
        try:
            num_languages = int(sys.argv[1])
            if num_languages <= 0:
                print("Number of languages must be positive, using default (24)")
                num_languages = 25
        except ValueError:
            print("Invalid number of languages, using default (24)")
    
    # Read from input.txt
    try:
        with open('input.txt', 'r', encoding='utf-8') as f:
            input_text = f.read()
        
        print(f"Read {len(input_text)} characters from input.txt")
        print(f"Will use top {num_languages} languages for translation")
        
        # Apply translation cycle with specified number of languages
        result = translation_cycle(input_text, num_languages)
        
        # Write to output.txt
        with open('output.txt', 'w', encoding='utf-8') as f:
            f.write(result)
        
        print(f"Translated result written to output.txt")
    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
