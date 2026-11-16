# Lab 12 - Read a Sales CSV, Write a Cleaned Report
# Name: Yashvini Jamnadas
# ISM2411 - Fall 2026
#
# Reflection
# 1. In Excel I'd open the file, add a total column, filter it, and copy the
#    results into a new sheet by hand, and I'd have to redo all of that every
#    time the data changed. Python does the whole read-transform-write process
#    in one run, works on files too big for Excel, and gives the same result
#    every time. Excel is still better for quickly looking at the data, making
#    a chart, or doing a one-off check.
#
# 2. For LYK Studios, I could keep a log of every outreach message I send to a
#    local business, adding one line each time with the date and the business
#    name. Append mode is right because it adds the new line to the end of the
#    file without erasing the earlier entries, so the log builds up a full
#    history over time.

import csv
from datetime import datetime

SALES_FILE = "data/sales.csv"
CLEANED_FILE = "data/cleaned.csv"
LOG_FILE = "data/run_log.txt"


# Exercise 1: Get the file
# sales.csv lives in data/ and has the columns product, price, quantity.
print("--- Exercise 1: Get the file ---")
with open(SALES_FILE) as f:
    print("Opened", SALES_FILE, "with no errors")


# Exercise 2: Read and print raw rows
print("\n--- Exercise 2: Read and print raw rows ---")
with open(SALES_FILE) as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)                     # every value is a string


# Exercise 3: Skip the header
print("\n--- Exercise 3: Skip the header ---")
with open(SALES_FILE) as f:
    reader = csv.reader(f)
    header = next(reader)
    print("Header:", header)
    for row in reader:
        print(row)


# Exercise 4: Compute totals
print("\n--- Exercise 4: Compute totals ---")
total_revenue = 0
with open(SALES_FILE) as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        product = row[0]
        price = float(row[1])
        quantity = int(row[2])
        line_total = price * quantity
        total_revenue += line_total
        print(f"{product}: {quantity} units × ${price:.2f} = ${line_total:.2f}")
print(f"Total revenue: ${total_revenue:.2f}")


# Exercise 5: Filter and write
print("\n--- Exercise 5: Filter and write ---")
original_count = 0
written_count = 0
with open(SALES_FILE) as infile, open(CLEANED_FILE, "w", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    next(reader)
    writer.writerow(["Product", "Price", "Qty", "Total"])
    for row in reader:
        original_count += 1
        price = float(row[1])
        quantity = int(row[2])
        line_total = price * quantity
        if line_total > 100:
            writer.writerow([row[0], f"{price:.2f}", quantity, f"{line_total:.2f}"])
            written_count += 1
print(f"Wrote {written_count} of {original_count} rows to {CLEANED_FILE}")


# Exercise 6: csv.DictReader
print("\n--- Exercise 6: csv.DictReader ---")
# csv.reader is fine for small files where you know the column order.
# DictReader is safer and easier to read because you use column names, not positions.
dict_total = 0
with open(SALES_FILE) as f:
    reader = csv.DictReader(f)
    for row in reader:
        price = float(row["price"])
        quantity = int(row["quantity"])
        line_total = price * quantity
        dict_total += line_total
        print(f"{row['product']}: {quantity} units × ${price:.2f} = ${line_total:.2f}")
print(f"Total revenue: ${dict_total:.2f}")
print("Matches Exercise 4:", round(dict_total, 2) == round(total_revenue, 2))


# Exercise 7: Sales summary by product
print("\n--- Exercise 7: Sales summary by product ---")
summary = {}
with open(SALES_FILE) as f:
    reader = csv.DictReader(f)
    for row in reader:
        product = row["product"]
        line_total = float(row["price"]) * int(row["quantity"])
        summary[product] = summary.get(product, 0) + line_total
for product in sorted(summary):
    print(f"{product}: ${summary[product]:.2f}")


# Exercise 8: Append mode log
print("\n--- Exercise 8: Append mode log ---")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(LOG_FILE, "a") as log:
    log.write(f"{timestamp} | Total revenue: ${total_revenue:.2f}\n")
print("Added a line to", LOG_FILE)
with open(LOG_FILE) as log:
    print(log.read())
