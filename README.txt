
# README

## Instructions

### Running the Program

To run the log processing program, use the following command:

```bash
python main.py <log_file_path>
```

Replace `<log_file_path>` with the path to your log file.

#### Example

```bash
python main.py log_file.txt
```

### Assumptions

1. The log file contains valid entries in the format `HH:MM:SS USERNAME Start|End`.
2. Invalid lines will be ignored.
3. Sessions with missing start or end times will assume the earliest or latest times in the log file, respectively.
4. Overlapping sessions are managed by pairing each session end with the earliest unmatched session start for that user, and session starts without an end are assumed to conclude at the latest time recorded in the log, ensuring comprehensive and accurate session tracking.

### File Structure

```
BT_Technical_assessment/
├── log_processor/
│   ├── __init__.py
│   ├── parser.py
│
├── tests/
│   ├── __init__.py
│   ├── test_parser.py
│   └── test_processor.py
│
└── main.py
```

### Running Unit Tests

To run the unit tests, use the following command:

```bash
python -m unittest discover -s tests -v
```

Make sure you are in the root directory of the project where the `tests` directory is located.

### Dependencies

This project does not require any external libraries or dependencies beyond the Python standard library.

