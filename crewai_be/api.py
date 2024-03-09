from dataclasses import dataclass
from datetime import datetime
import logging
from typing import List, Dict
from flask import Flask, jsonify
from threading import Thread
from uuid import uuid4
from threading import Thread, Lock

from crew import CompanyResearchCrew

app = Flask(__name__)


@dataclass
class Event:
    timestamp: datetime
    data: str


@dataclass
class Job:
    status: str
    events: List[Event]
    result: str


jobs: Dict[str, Job] = {}
jobs_lock = Lock()


def append_event(job_id, event_details):
    with jobs_lock:  # Lock the section where the jobs dictionary is accessed
        logging.info("Current jobs", jobs)
        if job_id not in jobs:
            jobs[job_id] = Job(status='STARTED', events=[
                               Event(datetime.now(), 'Job started')])
        jobs[job_id].events.append(
            Event(timestamp=datetime.now(), data=event_details))


def kickoff_crew(job_id, companies: list[str], positions: list[str], additional_details: str):
    print("Crew running")

    # Create and kick off the crew
    company_research_crew = CompanyResearchCrew(
        job_id, append_event, companies, positions, additional_details)
    results = company_research_crew.kickoff()
    print("Crew results", results)

    with jobs_lock:
        jobs[job_id].status = 'COMPLETE'
        jobs[job_id].events.append(
            Event(timestamp=datetime.now(), data="Crew complete"))


@app.route('/api/crew', methods=['POST'])
def run_crew():
    job_id = str(uuid4())

    # Use args or kwargs to pass parameters to your function as needed
    companies = ["Google", "Facebook", "Saltbox"]
    positions = ["CEO"]
    thread = Thread(target=kickoff_crew, args=(
        job_id, companies, positions, "Find the name, email, and linkedin profile for each position in each company."))

    thread.start()
    return jsonify({"job_id": job_id}), 202


@app.route('/api/crew/<job_id>', methods=['GET'])
def get_status(job_id):
    with jobs_lock:  # Use the lock to safely access the shared resource
        job = jobs.get(job_id)
        if job is None:
            return jsonify({"error": "Job not found"}), 404

    return jsonify({
        "job_id": job_id,
        "status": job.status,
        "events": [{"timestamp": event.timestamp.isoformat(), "data": event.data} for event in job.events]
    })


if __name__ == '__main__':
    app.run(debug=True)
