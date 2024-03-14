Market Research

- Front end:
  - Company name
  - Positions to research
  - Other instructions & details

#Ideal Flow:

## Prepare

- User has a text area where they can add company names. They can press "Add" to add company to the list.
- Added companies will have the name and an "X" next to the company name to delete them.
- There will be a positions table as well where you can specify the positions you want.
- There will be a information to find table where you can add LinkedIn, Phone number, email, etc.

## Run

- You can press the run to start the job which will kickoff the crew.
- While the crew is in the `running` state, we are goign to continually poll the job to look for event details.
  - We will show those event details in cards below the job as they run.

# Cancel Job

- There will be an X button that will kill the job.

## Finished

- When the job is in a completed state, fetch and show the result in the UI.

Todos:
[ ] Properly format people we find into JSON instead of bulleted list for research agent.
[ ] Use Ollama with Mistral Function Calling instead of ChatGPT
[ ] Clean up logging.
[ ] Setup cancel api endpoint to kill thread.
[ ] Update the Job to include a result JSON object
