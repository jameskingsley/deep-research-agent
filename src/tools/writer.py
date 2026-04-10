from datetime import datetime

def format_report_metadata(report_content, topic):
    """
    Wraps the AI generated report with professional metadata.
    """
    header = f"# Research Report: {topic.upper()}\n"
    meta = f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    status = "**Status:** Finalized via Autonomous Multi-Agent Synthesis\n\n---\n\n"
    
    return header + meta + status + report_content

def clean_filename(topic):
    """
    Generates a web-safe filename based on the topic.
    """
    safe_name = "".join([c if c.isalnum() else "_" for c in topic.lower()])
    return f"research_{safe_name}_{datetime.now().strftime('%Y%m%d')}"