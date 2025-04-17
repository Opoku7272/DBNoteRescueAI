# DBNoteRescueAI

**DBNoteRescueAI** is an intelligent migration tool that converts notes stored in SQLite databases (commonly used by mobile note-taking applications) into standalone Markdown files, leveraging artificial intelligence to enhance titles and organize content efficiently.

![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)
![Python 3.7+](https://img.shields.io/badge/Python-3.7+-blue)

## 🚀 Features

- **Comprehensive Note Migration**: Extract notes from SQLite databases and convert them to individual Markdown files with metadata preservation
- **AI-Powered Title Enhancement**: Uses Google Gemini API to generate descriptive, concise titles based on note content
- **Multi-language Support**: Supports both English and Spanish for AI title generation prompts
- **Rich Markdown Formatting**: Exports notes with enhanced Markdown formatting, preserving creation dates, modification timestamps, and original metadata
- **Highly Customizable**: Configure for different database structures through command-line parameters
- **Non-AI Mode**: Option to migrate notes without using AI, maintaining original titles when preferred
- **API Rate Limit Management**: Built-in delay system to respect API quotas and ensure smooth operation

## 📋 Prerequisites

- Python 3.7 or higher
- Internet connection (for AI functionality)
- Google Gemini API key (optional, required only if you wish to use the AI title enhancement)
- Access to the SQLite database file containing your notes

## 📦 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Gabriel-Adaro/DBNoteRescueAI.git
   cd DBNoteRescueAI
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) If you plan to use the AI functionality, [obtain a Google Gemini API key](https://ai.google.dev/gemini-api/docs/api-key?hl=es-419).

## 🔍 Detailed Usage Guide

### Basic Command Structure

```bash
python dbnoterescueai.py --db /path/to/your/database.db [options]
```

### Essential Parameters

| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| `--db` | `-d` | Path to the SQLite database file | `blocdenotas.db` |
| `--output` | `-o` | Output directory for Markdown files | `migrated_notes_md` |
| `--api-key` | `-k` | Google Gemini API key | Environment variable `GEMINI_API_KEY` |
| `--no-ai` | | Disable AI title generation | False (AI enabled) |
| `--language` | `-l` | Language for AI prompts (`en` or `es`) | `en` (English) |

### Database Structure Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--table` | Database table name | `notes` |
| `--id-column` | Column name for note ID | `_id` |
| `--title-column` | Column name for note title | `title` |
| `--body-column` | Column name for note content | `body` |
| `--date-column` | Column name for creation date | `date` |
| `--updated-column` | Column name for last update timestamp | `updated_at` |

### API Behavior Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--content-limit` | Maximum characters to send to the API | `2000` |
| `--delay` | Delay between API calls in seconds | `4` |

## 🚀 Usage Examples

### Basic Migration with AI Title Enhancement

```bash
python dbnoterescueai.py --db my_notes.db --api-key YOUR_API_KEY
```

### Migrating Notes in Spanish Language

```bash
python dbnoterescueai.py --db my_notes.db --api-key YOUR_API_KEY --language es
```

### Migration without AI (Keep Original Titles)

```bash
python dbnoterescueai.py --db my_notes.db --no-ai
```

### Using Environment Variable for API Key

```bash
export GEMINI_API_KEY=your_api_key_here
python dbnoterescueai.py --db my_notes.db
```

### Custom Database Structure

```bash
python dbnoterescueai.py --db my_notes.db --api-key YOUR_API_KEY \
  --table my_notes_table \
  --title-column note_title \
  --body-column note_content \
  --date-column created_at \
  --updated-column modified_at
```

### Adjusting API Rate Limits

```bash
python dbnoterescueai.py --db my_notes.db --api-key YOUR_API_KEY --delay 2
```

## 🔑 Why use the Google Gemini API integration?

DBNoteRescueAI uses Google's Gemini API for several reasons:

1. **Free Tier Availability**: Gemini offers a generous free tier that allows up to 30 requests per minute (RPM) for the `gemini-2.0-flash-lite` model, making it accessible for personal use

2. **Performance**: The `gemini-2.0-flash-lite` model provides an excellent balance between speed and quality for tasks

4. **Multi-language Support**: Native support for multiple languages, including English and Spanish

### Rate Limit Management

The script includes built-in protection against API rate limiting:

- By default, the script introduces a 4-second delay between API calls (`--delay 4`)
- This default setting keeps you well below Gemini's 30 RPM limit for the free tier
- You can adjust this delay based on your specific API quota:
  - For free tier users: 3-4 seconds is recommended
  - For paid tier users: Can be reduced to 0.5-1 seconds if needed

If you're processing a large number of notes and want to optimize speed while staying within your rate limits, you can adjust the delay parameter:

```bash
# Example: Faster processing (2-second delay)
python dbnoterescueai.py --db my_notes.db --api-key YOUR_API_KEY --delay 2

# Example: Very conservative approach (6-second delay)
python dbnoterescueai.py --db my_notes.db --api-key YOUR_API_KEY --delay 6
```

**Note**: With the default settings, you should not encounter rate limit errors as long as you're within the free tier's 30 RPM limit.

## 🌐 Language Support

DBNoteRescueAI supports generating AI titles in multiple languages:

- **English** (`--language en`): Default option with prompts optimized for English title generation
- **Spanish** (`--language es`): Specialized prompts for Spanish title generation

The language parameter affects:
1. The prompts sent to the Gemini API
2. The style and structure of generated titles

Example usage for Spanish notes:

```bash
python dbnoterescueai.py --db mis_notas.db --api-key YOUR_API_KEY --language es
```

## 🔎 Database Compatibility

### Expected Database Structure

By default, DBNoteRescueAI expects a SQLite database with the following structure:

```sql
CREATE TABLE notes (
    _id INTEGER PRIMARY KEY,
    title TEXT,
    body TEXT,
    date TEXT,
    updated_at INTEGER
);
```

### Compatible Note Applications

DBNoteRescueAI works well with databases from various note-taking applications, including:

- Simple note-taking apps that use SQLite storage
- Many Android-based note applications
- Exported databases from certain note management systems

If your database has a different structure, use the table and column parameters to customize the migration process.

## 📝 Output Format

The tool generates Markdown files with the following structure:

```markdown
# AI-Generated Title (or Original Title)

*(Original Title: The original title if different)*
*(Note ID: 123)*
*(Creation Date: 2023-04-15)*
*(Last Updated: 2023-05-20 14:30:45)*
---

Note content preserved in its original form...
```

## 🛠️ Additional Configuration Options

### Setting Up Environment Variables

For convenience, you can set up the API key as an environment variable:

**Linux/macOS**:
```bash
export GEMINI_API_KEY=your_api_key_here
```

**Windows (CMD)**:
```cmd
set GEMINI_API_KEY=your_api_key_here
```

**Windows (PowerShell)**:
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

### Content Limitation for API

To optimize token usage and API costs, DBNoteRescueAI limits the content sent to the AI:

```bash
# Send only the first 1000 characters for title generation
python dbnoterescueai.py --db my_notes.db --api-key YOUR_API_KEY --content-limit 1000
```

## 🔍 Obtaining a Google Gemini API Key

Google Gemini offers a free tier with generous usage limits, sufficient for processing hundreds of notes:

1. Visit [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key?hl=es-419)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

**Important Notes on the Free Tier**:
- Free tier provides up to 30 requests per minute (RPM) for the `gemini-2.0-flash-lite` model
- The default 4-second delay between requests ensures you stay well below the rate limit
- No credit card is required for the free tier

## 🔧 Troubleshooting Guide

### Database Connection Issues

If you encounter database connection problems:
- Verify the database path is correct
- Ensure you have read permissions for the file
- Confirm it's a valid SQLite database
- Try using an absolute path instead of a relative one

```bash
# Using absolute path
python dbnoterescueai.py --db /absolute/path/to/your/notes.db
```

### API Errors

For Gemini API issues:
- Verify your API key is correct
- Check your internet connection
- Confirm you haven't exceeded your API quota
- Try increasing the delay between requests:

```bash
python dbnoterescueai.py --db my_notes.db --api-key YOUR_API_KEY --delay 6
```

### Character Encoding Problems

If you see strange characters in generated files:
- Ensure your database uses UTF-8 encoding
- Check for compatibility issues between source and destination systems
- For Windows users, consider setting the console to UTF-8 mode:

```cmd
chcp 65001
```

### Missing or Empty Output

If files aren't being generated:
- Check that the output directory exists and is writable
- Verify that notes in the database have content
- Use verbose mode to see detailed processing information

## 📊 Performance Considerations

- **Processing Speed**: With default settings (4-second delay), expect to process approximately 15 notes per minute
- **Memory Usage**: The script has minimal memory requirements and can handle databases with thousands of notes
- **Disk Space**: Output files are typically smaller than the original database
- **API Costs**: Free tier is sufficient for most personal use cases

## 📄 License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

## 🤝 Contributing

Contributions are welcome! If you encounter bugs or have suggestions for improvements:

1. Open an issue describing the problem or enhancement
2. Fork the repository and create a new branch for your feature
3. Submit a pull request with a clear description of the changes

For major changes, please open an issue first to discuss what you would like to change.

## 🙏 Acknowledgements

- Google for providing accessible AI capabilities
