import csv
from pathlib import Path
from datetime import datetime

def read_dataset(file_path, domain):

    records = []

    file_path = Path(file_path)

    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:

        reader = csv.DictReader(file)

        for row_number, row in enumerate(reader, start=2):

            record = {
                "domain": domain,
                "source_text": row.get("Text"),
                "summary_text": row.get("Summary"),
                "source_file": file_path.name,
                "row_number": row_number
            }

            # Check whether the row contains unexpected extra columns
            if None in row:
                record["_read_error"] = "Unexpected extra columns in CSV row"

            records.append(record)

    return records


def validate_record(record):

    if "_read_error" in record:
        return False, record["_read_error"]

    valid_domains = ["Bible", "News", "Quran", "Tweets"]


    required_fields = ["domain", "source_text", "summary_text"]

    for field in required_fields:
        if field not in record:
            return False, f"Missing field: {field}"

    domain = record["domain"]
    source = record["source_text"]
    summary = record["summary_text"]

   
    if not isinstance(source, str) or not source.strip():
        return False, "Empty or invalid source text"

    if not isinstance(summary, str) or not summary.strip():
        return False, "Empty or invalid summary text"


    if domain not in valid_domains:
        return False, f"Invalid domain: {domain}"

    if source.strip() == summary.strip():
        return False, "Source and summary are identical"

    source_words = len(source.split())
    summary_words = len(summary.split())
  
    if summary_words >= source_words:
        return False, "Summary is not shorter than source"

    return True, "Valid record"

def process_dataset(records):

    valid_records = []
    invalid_records = []

    for record in records:

        is_valid, reason = validate_record(record)

        if is_valid:
            valid_records.append(record)

        else:
            # Keep the rejected record along with the reason
            rejected = record.copy()
            rejected["reason"] = reason

            invalid_records.append(rejected)

    return valid_records, invalid_records


def export_clean_data(valid_records, output_path):

    output_path = Path(output_path)

    # Create the folder if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    columns = ["domain", "source_text", "summary_text"]

    with open(output_path, "w", encoding="utf-8", newline="") as file:

        writer = csv.DictWriter(file, fieldnames=columns)

        # Add column names
        writer.writeheader()

        # Save each valid record
        for record in valid_records:
            writer.writerow({
                "domain": record["domain"],
                "source_text": record["source_text"],
                "summary_text": record["summary_text"]
            })

    print("Clean dataset saved successfully!")



def write_audit_log(total_records, valid_records, invalid_records, log_path):

    log_path = Path(log_path)

    # Create the folder if needed
    log_path.parent.mkdir(parents=True, exist_ok=True)

    total_valid = len(valid_records)
    total_invalid = len(invalid_records)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_path, "w", encoding="utf-8") as file:

        file.write("MALAYALAM SUMMARIZATION AUDIT LOG\n")
        file.write("=" * 40 + "\n")

        file.write(f"Date and time: {current_time}\n\n")

        file.write("DATASET SUMMARY\n")
        file.write("-" * 25 + "\n")

        file.write(f"Total records: {total_records}\n")
        file.write(f"Valid records: {total_valid}\n")
        file.write(f"Rejected records: {total_invalid}\n")

        if total_records > 0:
            valid_percentage = (total_valid / total_records) * 100
        else:
            valid_percentage = 0

        file.write(f"Valid percentage: {valid_percentage:.2f}%\n\n")

        file.write("REJECTED RECORDS\n")
        file.write("-" * 25 + "\n")

        for number, record in enumerate(invalid_records, start=1):

            file.write(f"\nRecord {number}\n")
            file.write(f"Domain: {record.get('domain', 'Unknown')}\n")
            file.write(f"Reason: {record.get('reason', 'Unknown')}\n")

            if "source_file" in record:
                file.write(f"Source file: {record['source_file']}\n")

            if "row_number" in record:
                file.write(f"Row number: {record['row_number']}\n")

    print("Audit log created successfully!")