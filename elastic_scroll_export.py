#!/usr/bin/env python3
import argparse
import csv
import getpass
import json
import os
import time
from datetime import datetime
from elasticsearch import Elasticsearch

def main():
    # Argumentum parser
    parser = argparse.ArgumentParser(description="Elasticsearch Scroll API export")
    parser.add_argument("-u", "--user", help="Elasticsearch username")
    parser.add_argument("-p", "--password", help="Elasticsearch password")
    parser.add_argument("-q", "--query", help="Elasticsearch query file path (JSON)")
    parser.add_argument("-f", "--fields", help="Fields to export (comma-separated, timestamp included automatically)")
    args = parser.parse_args()

    # Interaktív kérdések, ha paraméter nincs
    username = args.user or input("Elasticsearch felhasználónév: ")
    password = args.password or getpass.getpass("Elasticsearch jelszó: ")
    query_file = args.query or input("Query fájl elérési útja: ")
    fields_input = args.fields or input("Exportálandó mezők vesszővel elválasztva (timestamp kötelezően exportálódik): ")

    # Elasticsearch hostok
    hosts = [
        "https://101.0.0.36:9200",
        "https://101.0.0.35:9200"
    ]

    # Index pattern
    index_pattern = "logs-docker*"

    # Elasticsearch kliens
    es = Elasticsearch(
        hosts,
        basic_auth=(username, password),
        verify_certs=False,
        ssl_show_warn=False
    )

    # Query betöltése fájlból
    try:
        with open(query_file, 'r', encoding='utf-8') as f:
            query = json.load(f)
    except Exception as e:
        print(f"Hiba a query fájl betöltésekor: {e}")
        exit(1)

    # Exportálandó mezők feldolgozása
    export_fields = ['@timestamp']  # kötelező mező
    if fields_input:
        extra_fields = [f.strip() for f in fields_input.split(',') if f.strip()]
        export_fields.extend(extra_fields)

    # A size paramétert tegyük a query body-ba (DeprecationWarning elkerülése)
    page_size = 10000
    if 'size' not in query:
        query['size'] = page_size

    # Hozzáadjuk a _source mezőket a query-hez
    if '_source' not in query:
        query['_source'] = export_fields
    else:
        if isinstance(query['_source'], list):
            query['_source'] = list(set(query['_source'] + export_fields))
        else:
            query['_source'] = export_fields

    # Scroll API használata
    scroll_time = "5m"
    try:
        response = es.search(
            index=index_pattern,
            body=query,
            scroll=scroll_time
        )
    except Exception as e:
        print(f"Hiba a keresés indításakor: {e}")
        exit(1)

    scroll_id = response['_scroll_id']
    hits = response['hits']['hits']

    # Output fájlnév generálása
    timestamp_now = datetime.now().strftime('%Y%m%d%H%M%S')
    export_fields_no_at = [field.replace('@', '') for field in export_fields]
    filename_prefix = '_'.join(export_fields_no_at)
    output_file = f"{filename_prefix}-{timestamp_now}.csv"

    # CSV export
    total_docs = 0
    with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(export_fields)  # fejléc

        while hits:
            for hit in hits:
                source = hit.get('_source', {})
                row = [source.get(field, '') for field in export_fields]
                writer.writerow(row)
                total_docs += 1

            response = es.scroll(scroll_id=scroll_id, scroll=scroll_time)
            scroll_id = response['_scroll_id']
            hits = response['hits']['hits']

    print(f"Sikeres export: {output_file} ({total_docs} sor)")

    # Scroll context lezárása
    es.clear_scroll(scroll_id=scroll_id)

if __name__ == "__main__":
    main()
