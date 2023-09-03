import serial, string
import csv
import datetime

output = ""

# ser = serial.Serial('/dev/ttyUSB0', 9600, 8, 'N', 1, timeout=1)
ser = serial.Serial('COM6', 9600, 8, 'N', 1, timeout=1)

dataS = ""

# Create a list to store log data
log_records = []


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
    writer.writerow(["Timestamp"])# Header row

a = 1
while True:
  dataS = ser.readline().decode('utf-8').strip()
  # a = a+1
  # dataS = str(a)
  current_time = datetime.datetime.now()
  # Generate log data (you can do this whenever you want to log data)
  log_records.append([current_time,dataS])
  if dataS != "":
    with open(csv_filename, mode="a", newline="") as file:
      writer = csv.writer(file)
      for dataL in log_records:
          writer.writerow(dataL)
    log_records = []

  print(f"Log data appended to {csv_filename}")