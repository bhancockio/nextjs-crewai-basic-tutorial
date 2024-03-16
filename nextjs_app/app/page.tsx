"use client";

import { EventLog } from "@/components/EventLog";
import { FinalOutput } from "@/components/FinalOutput";
import InputSection from "@/components/InputSection";
import { useCrewJob } from "@/hooks/useCrewJob";

export default function Home() {
  // Hooks
  const crewJob = useCrewJob();

  return (
    <div className="bg-white min-h-screen text-black">
      <div className="flex">
        <div className="w-1/2 p-4">
          <InputSection
            title="Companies"
            placeholder="Add a company"
            data={crewJob.companies}
            setData={crewJob.setCompanies}
          />
          <InputSection
            title="Positions"
            placeholder="Add a position"
            data={crewJob.positions}
            setData={crewJob.setPositions}
          />
        </div>
        <div className="w-1/2 p-4 flex flex-col">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold">Output</h2>
            <button
              onClick={() => crewJob.startJob()}
              className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded text-sm"
              disabled={crewJob.running}
            >
              {crewJob.running ? "Running..." : "Start"}
            </button>
          </div>
          <FinalOutput positionInfoList={crewJob.positionInfoList} />
          <EventLog events={crewJob.events} />
        </div>
      </div>
    </div>
  );
}
