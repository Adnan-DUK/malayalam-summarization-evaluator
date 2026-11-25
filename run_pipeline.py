
from pathlib import Path

from src.ingestion import (
    read_dataset,
    process_dataset,
    export_clean_data,
    write_audit_log
)


def main():

    # Get the main project folder
    project_root = Path(__file__).resolve().parent

    # List of datasets and their respective domains
    datasets = [
        ("malayalam_bible.csv", "Bible"),
        ("malayalam_news.csv", "News"),
        ("malayalam_quran.csv", "Quran"),
        ("malayalam_tweets.csv", "Tweets")
    ]

    # This list will hold records from all four datasets
    all_records = []

    print("\nLoading Malayalam datasets...\n")

    # Read each dataset and combine all the records
    for filename, domain in datasets:

        file_path = project_root / "data" / "raw" / filename

        print(f"Loading {domain} dataset...")

        if not file_path.exists():
            print(f"File not found: {filename}")
            continue

        records = read_dataset(file_path, domain)

        all_records.extend(records)

        print(f"{len(records)} records loaded from {filename}")

    # Check whether any records were loaded
    if not all_records:
        print("\nNo records found. Please check the dataset files.")
        return

    print("\nProcessing all records...")

    # Separate valid records from rejected records
    valid_records, invalid_records = process_dataset(all_records)

    # Create the output folder if it doesn't already exist
    output_folder = project_root / "data" / "processed"
    output_folder.mkdir(parents=True, exist_ok=True)

    # Save the validated records into a clean CSV file
    clean_file = output_folder / "clean_malayalam_summaries.csv"

    export_clean_data(valid_records, clean_file)

    # Create an audit log containing the processing results
    audit_file = output_folder / "summarization_audit.log"

    write_audit_log(
        len(all_records),
        valid_records,
        invalid_records,
        audit_file
    )

    # Display a summary of the completed processing
    print("\nProcessing completed!")
    print("-" * 35)

    print(f"Total records: {len(all_records)}")
    print(f"Valid records: {len(valid_records)}")
    print(f"Rejected records: {len(invalid_records)}")

    print("\nOutput files:")
    print(f"Clean dataset: {clean_file}")
    print(f"Audit log: {audit_file}")


if __name__ == "__main__":
    main()
