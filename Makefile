DATA_URL = https://tmp-gfx-public-data.s3.amazonaws.com/aspep/aspep_with_extended_derived_stats.json
DATA_FILE = src-data/state_employment.json
DATA_OUTPUT_DIR = static/files/data
PROCESS_SCRIPT = scripts/process_data.py
SUMMARY_SCRIPT = scripts/summarize.py
PYTHON = pipenv run  # Default to pipenv run, can be overridden


# Step 0: Download data
$(DATA_FILE):
	curl $(DATA_URL) -o $(DATA_FILE) --compressed


# Step 1: Process data and generate state-specific JSON files
process_data: $(DATA_FILE)
	$(PYTHON) python $(PROCESS_SCRIPT) --input-file=$(DATA_FILE) --output-dir=$(DATA_OUTPUT_DIR)

# Step 2: Generate markdown summaries from the newly created JSON files
summarize: process_data
	for file in $(DATA_OUTPUT_DIR)/*_data.json; do \
		state=$$(basename $$file _data.json); \
		$(PYTHON) python $(SUMMARY_SCRIPT) --input-file=$$file --output-file=$$file; \
	done

# Run both steps by default
all: summarize

# Cleanup rule (optional) to remove generated files
clean:
	rm -f $(DATA_OUTPUT_DIR)/*.json $(SUMMARY_OUTPUT_DIR)/*.md
