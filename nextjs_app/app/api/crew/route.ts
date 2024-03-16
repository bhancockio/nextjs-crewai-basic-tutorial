import axios from "axios";
import { NextRequest, NextResponse } from "next/server";

export async function POST(request: Request) {
  const { companies, positions } = await request.json();

  if (!companies.length || !positions.length) {
    return NextResponse.json(
      { message: "Companies or positions array is empty" },
      { status: 400 }
    );
  }

  try {
    // Replace this URL with the actual URL of your backend server
    const crewResponse = await axios.post<{ job_id: string }>(
      "http://localhost:3001/api/crew",
      {
        companies,
        positions,
      }
    );

    console.log("crewResponse", crewResponse.data);

    // Assuming backendResponse.data.jobId is the ID of the job you started
    return NextResponse.json(
      { jobId: crewResponse.data.job_id },
      { status: 200 }
    );
  } catch (error) {
    console.error(error);
    return NextResponse.json(
      { message: "Failed to start job" },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const jobId = searchParams.get("jobId");

  if (!jobId) {
    return Response.json({ error: "No jobId provided" }, { status: 400 });
  }

  try {
    // Make the GET request to your backend server
    const crewResponse = await axios.get(
      `http://localhost:3001/api/crew/${jobId}`
    );

    return NextResponse.json(crewResponse.data, { status: 200 });
  } catch (error) {
    console.error(error);
    // If the backend server returns an error, forward that error to the client
    if (axios.isAxiosError(error) && error.response) {
      return NextResponse.json(error.response.data, {
        status: error.response.status,
      });
    } else {
      // If there was an issue with the request itself, return a 500 error
      return NextResponse.json(
        { message: "Failed to get job status" },
        { status: 500 }
      );
    }
  }
}
