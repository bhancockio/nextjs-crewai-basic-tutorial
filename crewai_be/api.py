# Standard library imports
from datetime import datetime
import json
import re
from threading import Thread, Lock
from uuid import uuid4

# Related third-party imports
from flask import Flask, jsonify, request, abort
from dotenv import load_dotenv

# Local application/library specific imports
from crew import CompanyResearchCrew
from job_manager import append_event, jobs, jobs_lock, Event
from utils.logging import logger


load_dotenv()

app = Flask(__name__)


def kickoff_crew(job_id, companies: list[str], positions: list[str]):
    logger.info(f"Crew for job {job_id} is starting")

    results = None
    try:
        company_research_crew = CompanyResearchCrew(job_id, append_event)
        company_research_crew.setup_crew(
            companies, positions)
        results = company_research_crew.kickoff()
        logger.info(f"Crew for job {job_id} is complete", results)

    except Exception as e:
        logger.error(f"Error in kickoff_crew for job {job_id}: {e}")
        append_event(job_id, f"An error occurred: {e}")
        with jobs_lock:
            jobs[job_id].status = 'ERROR'
            jobs[job_id].result = str(e)

    with jobs_lock:
        jobs[job_id].status = 'COMPLETE'
        jobs[job_id].result = results
        jobs[job_id].events.append(
            Event(timestamp=datetime.now(), data="Crew complete"))


@app.route('/api/crew', methods=['POST'])
def run_crew():
    logger.info("Received request to run crew")
    # Validation
    data = request.json
    if not data or 'companies' not in data or 'positions' not in data:
        abort(400, description="Invalid input data provided.")

    job_id = str(uuid4())
    companies = data['companies']
    positions = data['positions']

    thread = Thread(target=kickoff_crew, args=(
        job_id, companies, positions))
    thread.start()

    return jsonify({"job_id": job_id}), 202


@app.route('/api/crew/<job_id>', methods=['GET'])
def get_status(job_id):
    with jobs_lock:
        job = jobs.get(job_id)
        if job is None:
            abort(404, description="Job not found")

    # Strip markdown backticks and parse the JSON string
    try:
        # Use regex to find JSON object inside the string
        json_str = re.search(r'```json\n(.+)\n```',
                             job.result, re.DOTALL).group(1)
        # Convert the JSON string to a Python dictionary
        result_obj = json.loads(json_str)
    except (AttributeError, json.JSONDecodeError) as e:
        # Handle cases where result is not in the expected format
        result_obj = "Invalid format or content for job results"
        # You might want to log this error or handle it differently depending on your needs

    return jsonify({
        "job_id": job_id,
        "status": job.status,
        "result": result_obj,
        "events": [{"timestamp": event.timestamp.isoformat(), "data": event.data} for event in job.events]
    })


if __name__ == '__main__':
    app.run(debug=True, port=3001)
