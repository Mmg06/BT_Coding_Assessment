import sys
import logging
from collections import defaultdict, deque
from datetime import datetime, timedelta
from log_processor.parser import parse_log_line

# Configure logging to display info-level messages
logging.basicConfig(level=logging.INFO)

def process_log_file(filepath, suppress_logging=False):
    """
    Process the log file to calculate the total duration of user sessions.

    Parameters:
    filepath (str): The path to the log file.
    suppress_logging (bool): If True, suppresses error logging output.

    Returns:
    dict: A dictionary containing the count of sessions and total duration for each user.
    """
    if suppress_logging:
        logging.disable(logging.ERROR)  # Suppress error logging if requested

    # Dictionary to hold session data for each user
    sessions = defaultdict(deque)
    earliest_time = None  # To track the earliest time in the log
    latest_time = None  # To track the latest time in the log

    try:
        # Open and read the log file
        with open(filepath, 'r') as file:
            for line in file:
                # Parse each line of the log file
                parsed_line = parse_log_line(line)
                if parsed_line:
                    time, username, action = parsed_line
                    # Update the earliest and latest times encountered
                    if earliest_time is None or time < earliest_time:
                        earliest_time = time
                    if latest_time is None or time > latest_time:
                        latest_time = time
                    # Append the parsed action to the user's session data
                    sessions[username].append((time, action))
    except IOError:
        logging.error("Error: File {} not found.".format(filepath))
        if suppress_logging:
            logging.disable(logging.NOTSET)  # Re-enable logging if it was suppressed
        return {}

    if earliest_time is None or latest_time is None:
        logging.error("No valid log entries found.")
        if suppress_logging:
            logging.disable(logging.NOTSET)  # Re-enable logging if it was suppressed
        return {}

    results = {}
    for user, entries in sessions.items():
        total_duration = timedelta()  # Total duration of all sessions for the user
        session_count = 0  # Count of sessions for the user
        open_sessions = deque()  # Stack to track start times of open sessions

        for time, action in entries:
            if action == 'Start':
                open_sessions.append(time)  # Record the start time of a session
            elif action == 'End':
                if open_sessions:
                    start_time = open_sessions.popleft()  # Match end time with the earliest unmatched start time
                    total_duration += (time - start_time)
                    session_count += 1
                else:
                    # If there's an unmatched end time, assume the session started at the earliest time
                    total_duration += (time - earliest_time)
                    session_count += 1

        # Handle any remaining open sessions without an end time
        while open_sessions:
            start_time = open_sessions.popleft()
            total_duration += (latest_time - start_time)
            session_count += 1

        if session_count > 0:
            results[user] = (session_count, total_duration.total_seconds())

    if suppress_logging:
        logging.disable(logging.NOTSET)  # Re-enable logging if it was suppressed

    return results

def main():
    """
    Main function to run the log file processing and print the results.
    """
    if len(sys.argv) != 2:
        logging.error("Usage: python main.py <log_file_path>")
        sys.exit(1)

    log_file_path = sys.argv[1]

    # Process the log file and get the results
    results = process_log_file(log_file_path)

    if results:
        # Print the results for each user
        for user in sorted(results.keys()):
            session_count, duration = results[user]
            print("{} {} {}".format(user, session_count, int(duration)))
    else:
        logging.info('No valid log entries found or no sessions were processed.')

if __name__ == "__main__":
    main()
