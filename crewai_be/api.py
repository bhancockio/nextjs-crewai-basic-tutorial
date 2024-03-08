import datetime
from flask import Flask, jsonify
from threading import Thread
from uuid import uuid4
from threading import Thread, Lock
import time

app = Flask(__name__)

jobs = {}
jobs_lock = Lock()


def append_event(job_id, event_details):
    with jobs_lock:  # Lock the section where the jobs dictionary is accessed
        if job_id in jobs:
            jobs[job_id]['events'].append(event_details)
        else:
            jobs[job_id] = {'status': 'STARTED', 'events': [event_details]}


def kickoff_crew(job_id, company_name: str, postions: list[str], additional_details: str):
    append_event(job_id, {
        'time': str(datetime.datetime.now().time()),
        'details': 'Kickoff started'
    })

    print("Crew running")

    time.sleep(5)

    append_event(job_id, {
        'time': str(datetime.datetime.now().time()),
        'details': 'Task complete'
    })

    with jobs_lock:
        jobs[job_id]['status'] = 'COMPLETE'


@app.route('/api/crew', methods=['POST'])
def run_crew():
    job_id = str(uuid4())
    jobs[job_id] = {
        'status': 'STARTED',
        'events': []
    }

    # Use args or kwargs to pass parameters to your function as needed
    thread = Thread(target=kickoff_crew, args=(
        job_id, "Video Topic", "Video Details"))

    thread.start()
    return jsonify({"job_id": job_id}), 202


@app.route('/api/crew/<job_id>', methods=['GET'])
def get_status(job_id):
    with jobs_lock:  # Use the lock to safely access the shared resource
        job = jobs.get(job_id, {'status': 'UNKNOWN', 'events': []})
    return jsonify({
        "job_id": job_id,
        "status": job['status'],
        "events": job['events']
    })


if __name__ == '__main__':
    app.run(debug=True)
