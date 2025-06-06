# Elasticsearch Scroll Export Tool

This project is a Python 3.11 + Elastic Python SDK 8.17-based tool that allows exporting large amounts of data from Elasticsearch (using the Scroll API) to CSV.  
The output file name is automatically generated from the order of the exported fields and a timestamp.

## Key Features

- Command-line parameters:
  - -u: Elasticsearch username
  - -p: Elasticsearch password
  - -q: Path to the query JSON file
  - -f: Fields to export (comma-separated)

- Scroll API: stable for exporting large datasets.
- Output filename is automatically generated:
  <fields>_<fields>_-<timestamp>.csv (e.g.: timestamp_summary_message_agent.name-20240605235959.csv).
- Self-signed SSL certificate support (verify_certs=False).

## Usage

1. Create and activate the virtual environment:
   Specify the desired Python version in the python.conf file,  
   then run build-runtime.sh.

2. Prepare the query JSON file:
   Example: my_query.json (can be copied from Kibana):

   {
     "query": {
       "bool": {
         "must": [
           {
             "match_phrase": {
               "container.labels.com_docker_swarm_service_name": "voszmb-prod_member-management-admin"
             }
           },
           {
             "range": {
               "@timestamp": {
                 "gte": "now-24h/h",
                 "lte": "now"
               }
             }
           }
         ]
       }
     }
   }

3. Run:
   python elastic_scroll_export.py -u myuser -p mypass -q my_query.json -f summary,message,agent.name

If any parameter is missing, the script will prompt interactively.

## Configurable Options

The following variables can be easily modified in the script if needed:

- hosts: ["https://101.0.0.36:9200", "https://101.0.0.35:9200"]
  List of Elasticsearch servers (supports https with self-signed certificates).

- index_pattern: "logs-docker*"
  Index pattern to run the query on.

- scroll_time: "2m"
  The scroll context duration (e.g., 2 minutes).

- page_size: 1000
  Number of documents fetched in a single scroll request.

These can be easily modified at the beginning of the script (hosts, index_pattern, scroll_time, page_size).

## Tips

- When using self-signed SSL, the script runs with verify_certs=False — in production, using a CA certificate is recommended.
- The timestamp field is mandatory for export, but in the filename, it appears without the '@' character.
- The scroll context is automatically closed at the end of the script (clear_scroll).

## Dependencies

requirements.txt:
elasticsearch==8.17.0
certifi

## Example Output Filename

timestamp_summary_message_agent.name-20240605235959.csv
