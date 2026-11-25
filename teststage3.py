from src.ingestion import (
    process_dataset,
    export_clean_data,
    write_audit_log
)

# A few sample records to test the functions
records = [
    {
        "domain": "News",
        "source_text": "This is a long article about technology and development",
        "summary_text": "This is a short summary"
    },
    {
        "domain": "Bible",
        "source_text": "Same text",
        "summary_text": "Same text"
    },
    {
        "domain": "Tweets",
        "source_text": "A short tweet",
        "summary_text": "This summary has more words than the original tweet"
    }
]

# Separate valid and invalid records
valid_records, invalid_records = process_dataset(records)

# Save the clean data
export_clean_data(
    valid_records,
    "data/processed/clean_malayalam_summaries.csv"
)

# Create the audit log
write_audit_log(
    len(records),
    valid_records,
    invalid_records,
    "data/processed/summarization_audit.log"
)

# Display the results
print("\nProcessing completed!")
print("Total records:", len(records))
print("Valid records:", len(valid_records))
print("Rejected records:", len(invalid_records))