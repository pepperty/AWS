import serial, string
import csv
import datetime

# Specify the CSV file name
csv_file_name = "datalog.csv"

output = ""

# ser = serial.Serial('/dev/ttyUSB0', 9600, 8, 'N', 1, timeout=1)
ser = serial.Serial('COM6', 9600, 8, 'N', 1, timeout=1)
while True:

  print ("----")
  while output != "":
    output = ser.readline()
    print (output)

  # Get the current timestamp
  current_timestamp = datetime.datetime.now()

  # Create and open the CSV file for writing
  with open(csv_file_name, mode='w', newline='') as file:
      writer = csv.writer(file)

      # Split the string into a list of values (assuming CSV format)
      values = {current_timestamp,output}

      # Write the list of values to the CSV file
      writer.writerow(values)
  output = ""