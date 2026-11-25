# URL Shortener CLI

Shorten URLs using the free [is.gd](https://is.gd) API — no API key needed.

## Requirements

- Python 3 (standard library only — no extra packages)
- Internet access (the is.gd API is called over HTTPS)

## Usage

```bash
python3 main.py https://www.example.com/some/very/long/path
python3 main.py --file urls.txt
python3 main.py https://example.com --custom my-link
```

Options:

- `urls` — one or more URLs to shorten
- `--file, -f FILE` — file with one URL per line
- `--custom NAME` — request a custom short name (single URL only)
- `--timeout SECONDS` — request timeout (default: 10)

## Example

```bash
$ python3 main.py https://www.example.com/some/very/long/path
https://www.example.com/some/very/long/path -> https://is.gd/AbCdEf
```

API errors (for example an already-taken custom name, or an invalid
URL) are reported as `ERROR` with the message returned by is.gd.
