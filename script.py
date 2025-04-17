#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2025 Gabriel Adaro
# Licensed under the GNU General Public License v3.0

import sqlite3
import os
import re
import time
import datetime
import argparse
import google.generativeai as genai

# --- CONFIGURATION ---
# These settings can be modified directly or via CLI arguments
DEFAULT_DB_FILE = 'blocdenotas.db'
DEFAULT_OUTPUT_DIR = 'migrated_notes_md'
DEFAULT_API_KEY = None  # Must be provided via argument or environment variable

# Default table and column names (common in Android note apps)
DEFAULT_TABLE_NAME = 'notes'
DEFAULT_ID_COLUMN = '_id'
DEFAULT_TITLE_COLUMN = 'title'
DEFAULT_BODY_COLUMN = 'body'
DEFAULT_DATE_COLUMN = 'date'
DEFAULT_UPDATED_AT_COLUMN = 'updated_at'

# Content limit to send to the AI API (to save tokens)
DEFAULT_CONTENT_LIMIT_FOR_AI = 2000

# Wait time between API calls to avoid rate limits
DEFAULT_API_DELAY = 4  # seconds

DEFAULT_LANGUAGE = 'en'
PROMPTS = {
    'en': """
    Analyze the following note content and its original title.
    Generate a new title that is brief (5-7 words), concise, and captures the main idea.

    Original Title: \"{display_original}\"

    Note Content:
    \"{truncated}\"

    Suggested New Title:
    """,
    'es': """
    Analiza el siguiente contenido de una nota y su título original.
    Genera un título nuevo que sea corto (idealmente 5-7 palabras máximo), conciso y que capture la esencia principal del texto.

    Título Original: \"{display_original}\"

    Contenido de la Nota:
    \"{truncated}\"

    Título Sugerido:
    """
}

# --- HELPER FUNCTIONS ---

def sanitize_filename(name):
    """
    Cleans a string for use as a safe filename.

    Args:
        name (str): Original string that may contain unsafe characters

    Returns:
        str: Safe filename for different file systems
    """
    # Remove invalid filename characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    # Replace whitespace sequences with underscore
    name = re.sub(r'\s+', '_', name).strip('_')
    # Limit length to avoid filesystem issues
    return name[:100]


def format_timestamp(ts):
    """
    Converts a Unix timestamp to a human-readable format.

    Args:
        ts: Unix timestamp (seconds since epoch) or None

    Returns:
        str: Formatted date/time or fallback string
    """
    if ts is None or ts == 0:
        return "Not available"
    try:
        return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %Y-%m-%d %H:%M:%S')
    except Exception:
        return str(ts)


def generate_new_title(model, original_title, body_content, content_limit, language='en'):
    """
    Uses AI to generate a concise new title based on note content.

    Args:
        model: Configured AI model
        original_title (str): Original note title
        body_content (str): Note body text
        content_limit (int): Max characters to send to the API
        language (str): Language for the prompt ('en' or 'es')

    Returns:
        str: New title or fallback to original
    """
    if not body_content:
        print("  -> Empty content, cannot generate title.")
        return None

    display_original = original_title if original_title else "No Original Title"

    # Truncate body if it exceeds the content limit
    if content_limit and len(body_content) > content_limit:
        truncated = body_content[:content_limit] + "..."
    else:
        truncated = body_content

    prompt = PROMPTS.get(language, PROMPTS['en']).format(
        display_original=display_original,
        truncated=truncated
    )

    try:
        response = model.generate_content(prompt)
        new_title = response.text.strip().replace('"', '').replace('*', '').strip()
        if not new_title or len(new_title) < 3:
            print(f"  -> AI response invalid or too short: '{new_title}'. Using original title.")
            return original_title
        print(f"  -> New title (AI): {new_title}")
        return new_title

    except Exception as e:
        print(f"  !! Error calling AI API: {e}")
        return original_title


def configure_api(api_key):
    """
    Configures the Gemini API client.

    Args:
        api_key (str): Google Generative AI API key

    Returns:
        GenerativeModel: Configured model or None on failure
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("Gemini model configured successfully.")
        return model
    except Exception as e:
        print(f"Error configuring Gemini API: {e}")
        print("Ensure the API key is correct and you have network access.")
        return None


def parse_arguments():
    """
    Parses command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description='Migrate notes from an SQLite database to Markdown files with AI-enhanced titles'
    )

    parser.add_argument(
        '--db', '-d',
        help='Path to the SQLite DB file (default: blocdenotas.db)',
        default=DEFAULT_DB_FILE
    )
    parser.add_argument(
        '--output', '-o',
        help='Directory for Markdown output (default: migrated_notes_md)',
        default=DEFAULT_OUTPUT_DIR
    )
    parser.add_argument(
        '--api-key', '-k',
        help='Google AI (Gemini) API key. If omitted, reads GEMINI_API_KEY env var.',
        default=os.environ.get('GEMINI_API_KEY', DEFAULT_API_KEY)
    )
    parser.add_argument(
        '--table',
        help=f"DB table name (default: {DEFAULT_TABLE_NAME})",
        default=DEFAULT_TABLE_NAME
    )
    parser.add_argument(
        '--id-column',
        help=f"ID column name (default: {DEFAULT_ID_COLUMN})",
        default=DEFAULT_ID_COLUMN
    )
    parser.add_argument(
        '--title-column',
        help=f"Title column name (default: {DEFAULT_TITLE_COLUMN})",
        default=DEFAULT_TITLE_COLUMN
    )
    parser.add_argument(
        '--body-column',
        help=f"Body/content column name (default: {DEFAULT_BODY_COLUMN})",
        default=DEFAULT_BODY_COLUMN
    )
    parser.add_argument(
        '--date-column',
        help=f"Creation date column name (default: {DEFAULT_DATE_COLUMN})",
        default=DEFAULT_DATE_COLUMN
    )
    parser.add_argument(
        '--updated-column',
        help=f"Last-updated column name (default: {DEFAULT_UPDATED_AT_COLUMN})",
        default=DEFAULT_UPDATED_AT_COLUMN
    )
    parser.add_argument(
        '--content-limit',
        help=f"Max characters for AI input (default: {DEFAULT_CONTENT_LIMIT_FOR_AI})",
        type=int,
        default=DEFAULT_CONTENT_LIMIT_FOR_AI
    )
    parser.add_argument(
        '--delay',
        help=f"Delay between API calls in seconds (default: {DEFAULT_API_DELAY})",
        type=float,
        default=DEFAULT_API_DELAY
    )
    parser.add_argument(
        '--no-ai',
        help='Disable AI title generation; keep original titles',
        action='store_true'
    )
    parser.add_argument(
        '--language', '-l',
        choices=['en', 'es'],
        default=DEFAULT_LANGUAGE,
        help='Language for AI prompts (en=English, es=Spanish)'
    )

    return parser.parse_args()

# --- MAIN LOGIC ---

def main():
    """Main execution for the note migration process."""
    args = parse_arguments()

    # Check API key availability
    if not args.no_ai and not args.api_key:
        print("Error: No API key provided for Gemini.")
        print("Options:")
        print("  1. Provide via --api-key or -k")
        print("  2. Set the GEMINI_API_KEY environment variable")
        print("  3. Use --no-ai to keep original titles")
        return

    model = None
    if not args.no_ai:
        model = configure_api(args.api_key)
        if not model:
            print("Failed to configure the AI model. Exiting...")
            return

    os.makedirs(args.output, exist_ok=True)
    print(f"Output directory: {os.path.abspath(args.output)}")

    conn = None
    try:
        if not os.path.exists(args.db):
            print(f"Error: Database file not found at {args.db}")
            return

        print(f"Connecting to database: {args.db}")
        conn = sqlite3.connect(args.db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = f"""
        SELECT
            {args.id_column},
            {args.title_column},
            {args.body_column},
            {args.date_column},
            {args.updated_column}
        FROM {args.table}
        ORDER BY {args.id_column}
        """

        print(f"Running query on table '{args.table}'...")
        cursor.execute(query)
        notes = cursor.fetchall()
        total_notes = len(notes)
        print(f"Found {total_notes} notes in the database.")

        processed, skipped_empty, api_errors, file_errors = 0, 0, 0, 0

        for i, note in enumerate(notes, 1):
            note_id = note[args.id_column]
            orig_title = note[args.title_column] or ""
            body = note[args.body_column] or ""
            creation_date = note[args.date_column] or "Date not available"
            last_updated = note[args.updated_column]

            print(f"\n--- Processing Note {i}/{total_notes} (ID: {note_id}) ---")
            short_title = (orig_title[:60] + '...') if len(orig_title) > 60 else orig_title
            print(f"Original Title: '{short_title}'")

            if not body.strip():
                print("  -> Empty body; skipping note.")
                skipped_empty += 1
                continue

            if args.no_ai:
                final_title = orig_title
                print("  -> AI disabled. Using original title.")
            else:
                new_title = generate_new_title(model, orig_title, body, args.content_limit, args.language)
                if not new_title or not new_title.strip():
                    final_title = orig_title or f"Imported_Note_{note_id}"
                    print(f"  -> Using fallback title: {final_title}")
                    if new_title is None and body.strip():
                        api_errors += 1
                else:
                    final_title = new_title

            safe_title = sanitize_filename(final_title)
            md_filename = f"{note_id}_{safe_title}.md"
            filepath = os.path.join(args.output, md_filename)

            formatted_updated = format_timestamp(last_updated)

            md_content = f"# {final_title}\n\n"
            if orig_title and final_title != orig_title:
                md_content += f"*(Original Title: {orig_title})*\n"
            md_content += f"*(Note ID: {note_id})*\n"
            md_content += f"*(Creation Date: {creation_date})*\n"
            md_content += f"*(Last Updated: {formatted_updated})*\n"
            md_content += "---\n\n"
            md_content += body

            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(md_content)
                print(f"  -> Saved as: {md_filename}")
                processed += 1
            except IOError as e:
                print(f"  !! Error writing file {md_filename}: {e}")
                file_errors += 1
            except Exception as e:
                print(f"  !! Unexpected write error for {md_filename}: {e}")
                file_errors += 1

            if not args.no_ai and args.delay > 0:
                time.sleep(args.delay)

    except sqlite3.Error as e:
        print(f"\nDatabase error: {e}")
        print("Check the .db path and table/column names.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
    finally:
        if conn:
            conn.close()
            print("\nDatabase connection closed.")

    print("\n--- Summary ---")
    print(f"Total notes found: {total_notes}")
    print(f"Notes processed: {processed}")
    print(f"Notes skipped (empty): {skipped_empty}")
    print(f"API errors (fallback): {api_errors}")
    print(f"File errors: {file_errors}")
    print(f"Markdown files saved at: {os.path.abspath(args.output)}")
    print("--- Migration completed ---")

if __name__ == "__main__":
    main()
