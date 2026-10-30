# Elasticsearch Bulk Exporter

A small Python reference utility for retrieving Elasticsearch log search results in batches with the Scroll API and writing selected fields to CSV.

The useful operational idea is to process one batch at a time rather than collect all search results in memory. The repository contains a single readable script, [export.py](export.py), so its behavior and limits can be inspected directly.

**Status:** reference script. CSV export is the clearest output path in the current implementation. The JSON output has a multi-batch formatting limitation described below. No large-volume benchmark is included.

## How it works

```text
Configured index + query
        |
Initial Elasticsearch search (5-minute scroll context)
        |
Write one batch --> export.csv + export.json --> progress count
        |
Request next batch until empty
        |
Close output files and request scroll cleanup
```

## What this demonstrates

- Authenticated HTTP requests using Python and Requests.
- Paginated retrieval using a scroll context.
- Incremental file writing and progress reporting.
- Extraction of timestamp/message fields from log records.

## Setup

Use Python 3 and an isolated environment:

```bash
git clone https://github.com/vimrul/elasticsearch-bulk-exporter.git
cd elasticsearch-bulk-exporter
python3 -m venv .venv
source .venv/bin/activate
python -m pip install requests
```

Edit a **local copy** of `export.py` for your environment:

| Setting | Current example | What to change |
| --- | --- | --- |
| `ES_URL` | `http://localhost:9200` | Authorized Elasticsearch endpoint; use HTTPS when required |
| `USERNAME`, `PASSWORD` | Placeholder credentials | Local authentication values; never commit real credentials |
| `INDEX` | `filebeat-*` | Index or index pattern you are authorized to read |
| `QUERY["size"]` | `5000` | Batch size appropriate to record size and available memory |
| `QUERY["_source"]` | `@timestamp`, `message` | Fields required by the current CSV-writing code |
| `QUERY["query"]` | An example `match_phrase` filter | Replace with the intended search; it does not export all documents by default |

For a small controlled test, choose a dedicated test index and a narrow query. A `match_phrase` query should not be treated as a wildcard query merely because its text contains asterisks.

Run:

```bash
python export.py
```

On a run with matching documents, output files are opened in write mode and existing files of the same names are overwritten. Keep previous exports elsewhere before rerunning.

## Outputs and validation

- **`export.csv`**: header `timestamp,message`, then values from each hit's `_source`.
- **`export.json`**: full hit objects written as an array for each batch.
- **Console**: running count and a completion message after the normal path finishes.

Validate CSV using a parser rather than counting physical lines, because messages can contain line breaks:

```bash
python - <<'PY'
import csv
with open("export.csv", newline="") as source:
    reader = csv.DictReader(source)
    count = sum(1 for _ in reader)
print(f"CSV records: {count}")
PY
```

Compare the parsed row count to the script's reported count and your controlled input. Check representative timestamps/messages. Successful printing alone does not establish completeness.

## Current limitations

- **JSON across multiple batches is not one valid JSON document.** Each batch is dumped as an array without a surrounding container or separator. Do not feed a multi-batch `export.json` directly to a normal JSON parser. CSV is the usable structured export path until the JSON writer is changed.
- The script retains the initial scroll ID rather than updating it if the server returns a different ID.
- HTTP status checking, request timeouts, retries, and resumable checkpoints are not implemented.
- Scroll cleanup runs at the end of the normal path, not in a guaranteed cleanup handler.
- Missing `@timestamp` or `message` fields can raise an exception.
- Credentials are configured in the script; environment-variable or secret-store integration is not implemented.
- The output is a selected log export, not a restorable Elasticsearch snapshot or a bulk-import file.
- No automated tests or performance results are included.

These constraints are visible in the implementation and are documented here so users can make an informed choice before running it.

## Failure and recovery

If an export stops, treat the output as partial. Inspect the error, verify authentication and the query, and reduce batch size if needed. Preserve or move partial files before another run. The current script restarts from the initial search and does not resume a previous export.

Do not disable TLS verification to work around certificate failures. Handle exported logs as potentially sensitive and keep them out of public repositories.

For API behavior and scroll lifecycle, see the [Elasticsearch Scroll API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-scroll).

Author: [Mohammad Imrul Hasan](https://imrul.net/).
