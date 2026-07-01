## Configuration

The application loads settings from a `.env` file at startup via `python-dotenv`.
All variables are optional — if omitted, the defaults below are used.

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CALCULATOR_LOG_DIR` | path | `logs` | Directory where log files are written. Created automatically if missing. |
| `CALCULATOR_HISTORY_DIR` | path | `history` | Directory where the CSV calculation history is persisted. |
| `CALCULATOR_MAX_HISTORY_SIZE` | int | `1000` | Maximum number of calculations retained in memory/history. |
| `CALCULATOR_AUTO_SAVE` | bool | `true` | If `true`, history is written to CSV automatically after each operation. |
| `CALCULATOR_PRECISION` | int | `10` | Number of decimal places results are rounded to. |
| `CALCULATOR_MAX_INPUT_VALUE` | number | `1e15` | Rejects operands whose absolute value exceeds this limit (input validation). |
| `CALCULATOR_DEFAULT_ENCODING` | string | `utf-8` | Encoding used when reading/writing log and CSV files. |

### Example `.env`

```env
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history
CALCULATOR_MAX_HISTORY_SIZE=1000
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=10
CALCULATOR_MAX_INPUT_VALUE=1e15
CALCULATOR_DEFAULT_ENCODING=utf-8
```

> **Note:** Booleans accept `true`/`false`, `1`/`0`, or `yes`/`no` (case-insensitive).
> Invalid values raise a `ConfigurationError` at startup.
