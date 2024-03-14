"use client";

import { EventLog } from "@/components/EventLog";
import { FinalOutput } from "@/components/FinalOutput";
import InputSection from "@/components/InputSection";
import { useState } from "react";
import { Event } from "../types";

export default function Home() {
  const [events, setEvents] = useState<Event[]>([]);
  const [markdownOutput, setMarkdownOutput] = useState<string>("");

  const startJob = () => {};

  return (
    <div className="bg-white min-h-screen text-black">
      <div className="flex">
        <div className="w-1/2 p-4">
          <InputSection title="Companies" placeholder="Add a company" />
          <InputSection title="Positions" placeholder="Add a position" />
          <InputSection title="Info to Gather" placeholder="Add info" />
        </div>
        <div className="w-1/2 p-4 flex flex-col">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold">Output</h2>
            <button
              onClick={startJob}
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded text-sm"
            >
              Run
            </button>
          </div>
          <EventLog events={events} />
          <FinalOutput markdown={markdownOutput} />
        </div>
      </div>
    </div>
  );
}
