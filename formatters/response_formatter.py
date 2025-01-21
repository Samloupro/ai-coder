import uuid
import time

def format_execution_time(start_time):
    execution_time = time.time() - start_time
    minutes = int(execution_time // 60)
    seconds = int(execution_time % 60)
    return f"{minutes:02d} mn : {seconds:02d} s"

def format_scraping_response(
    url,
    root_domain,
    visited_links,
    emails={},
    phones={},
    social_links={},
    include_emails=True,
    include_phones=True,
    include_social_links=True,
    include_unique_links=True,
    start_time=None
):
    execution_time_str = format_execution_time(start_time) if start_time else "N/A"
    links_analysed_count = f"{len(visited_links)} links"

    return {
        "request_id": str(uuid.uuid4()),
        "execution_time": execution_time_str,
        "links_analysed_count": links_analysed_count,
        "root_domain": root_domain,
        "query": url,
        "status": "OK",
        "data": [
            {
                "emails": [{"value": email, "sources": sources} for email, sources in emails.items()] if include_emails else [],
                "phone_numbers": [{"value": phone, "sources": sources} for phone, sources in phones.items()] if include_phones else [],
                "social_links": social_links if include_social_links else {},
                "unique_links": sorted(list(visited_links)) if include_unique_links else []
            }
        ]
    }

def format_error_response(error_message, status="ERROR"):
    return {
        "error": str(error_message),
        "status": status
    }