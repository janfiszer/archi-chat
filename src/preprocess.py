import re
from config import keywords, parameters

from pathlib import Path

def remove_pattern_with_logging(
        text: str,
        pattern: str,
        flags: int = 0,
        verbose: bool = True
):
    """
    Remove all occurrences of a regex pattern from text and log what was removed.

    Args:
        text: The text to clean
        pattern: Regex pattern to search for and remove
        flags: Regex flags (e.g., re.DOTALL, re.IGNORECASE)
        verbose: If True, print what was removed to console
    """
    # Find all matches before removing
    removed_items = re.findall(pattern, text, flags=flags)

    # Remove the pattern
    cleaned_text = re.sub(pattern, '', text, flags=flags)

    # Log if verbose
    if verbose:
        print("=" * 60)
        print(f"REMOVING: {pattern}")
        print("=" * 60)
        print(f"Matches found: {len(removed_items)}")
        print("-" * 60)

        if removed_items:
            for i, item in enumerate(removed_items, 1):
                # Clean up the display
                display_item = item.strip()
                # Truncate long matches
                if len(display_item) > 100:
                    display_item = display_item[:100] + "..."
                # Show newlines as \n for clarity
                display_item = display_item.replace('\n', '\\n')
                print(f"[{i}] {display_item}")
        else:
            print("No matches found.")

        print("=" * 60 + "\n")

    return cleaned_text


def clean_raw_text_from_pdf(text):
    # removing page headers
    text = remove_pattern_with_logging(text, keywords.HEADER_PATTERN, verbose=parameters.LOG_REMOVED_PATTERNS)

    # removing right margin change notes
    text = remove_pattern_with_logging(text, keywords.RIGHT_MARGIN_CHANGE_NOTES_PATTERN, verbose=parameters.LOG_REMOVED_PATTERNS, flags=re.DOTALL)

    return text

if __name__ == "__main__":
    text_filepath = "data/prawo-budowlane.txt"

    with open(text_filepath, "r", encoding='utf-8') as txt_file:
        text = txt_file.read()

    cleaned_text = clean_raw_text_from_pdf(text)

    with open(f"data/cleaned-{Path(text_filepath).stem}.txt", "w", encoding='utf-8') as txt_file:
        txt_file.write(cleaned_text)