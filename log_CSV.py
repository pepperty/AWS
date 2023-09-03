import csv
import datetime

# Function to log the current timestamp
def log_timestamp():
    current_time = datetime.datetime.now()
    return current_time.strftime("%Y-%m-%d %H:%M:%S")

# Create a list to store log data
log_data = []

# Generate log data (you can do this whenever you want to log data)
log_data.append(log_timestamp())

# CSV filename
csv_filename = "timestamps.csv"

# Check if the file already exists
file_exists = True
try:
    with open(csv_filename, "r") as file:
        reader = csv.reader(file)
        if not list(reader):
            file_exists = False
except FileNotFoundError:
    file_exists = False

# If the file doesn't exist, create it with a header row
if not file_exists:
    with open(csv_filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp"])  # Header row

# Append log data to the CSV file
with open(csv_filename, mode="a", newline="") as file:
    writer = csv.writer(file)
    for data in log_data:
        writer.writerow([data])

print(f"Log data appended to {csv_filename}")
