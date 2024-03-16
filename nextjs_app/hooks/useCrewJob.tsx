"use client";

import axios from "axios";
import { useEffect, useState } from "react";
import toast from "react-hot-toast";

export type EventType = {
  data: string;
  timestamp: string;
};

export type NamedUrl = {
  name: string;
  url: string;
};

export type PositionInfo = {
  company: string;
  position: string;
  name: string;
  blog_articles_urls: string[];
  youtube_interviews_urls: NamedUrl[];
};

export const useCrewJob = () => {
  // State
  const [running, setRunning] = useState<boolean>(false);
  const [companies, setCompanies] = useState<string[]>([]);
  const [positions, setPositions] = useState<string[]>([]);
  const [events, setEvents] = useState<EventType[]>([]);
  const [positionInfoList, setPositionInfoList] = useState<PositionInfo[]>([]);
  const [currentJobId, setCurrentJobId] = useState<string>("");

  // useEffects
  useEffect(() => {
    let intervalId: number;
    console.log("currentJobId", currentJobId);

    const fetchJobStatus = async () => {
      try {
        console.log("calling fetchJobStatus");
        const response = await axios.get<{
          status: string;
          result: { positions: PositionInfo[] };
          events: EventType[];
        }>(`http://localhost:3001/api/crew/${currentJobId}`);
        const { status, events: fetchedEvents, result } = response.data;

        console.log("status update", response.data);

        setEvents(fetchedEvents);
        if (result) {
          console.log("setting job result", result);
          console.log("setting job positions", result.positions);
          setPositionInfoList(result.positions || []);
        }

        if (status === "COMPLETE" || status === "ERROR") {
          if (intervalId) {
            clearInterval(intervalId);
          }
          setRunning(false);
          toast.success(`Job ${status.toLowerCase()}.`);
        }
      } catch (error) {
        if (intervalId) {
          clearInterval(intervalId);
        }
        setRunning(false);
        toast.error("Failed to get job status.");
        console.error(error);
      }
    };

    if (currentJobId !== "") {
      intervalId = setInterval(fetchJobStatus, 1000) as unknown as number;
    }

    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [currentJobId]);

  const startJob = async () => {
    // Clear previous job data
    setEvents([]);
    setPositionInfoList([]);
    setRunning(true);

    try {
      const response = await axios.post<{ job_id: string }>(
        "http://localhost:3001/api/crew",
        {
          companies,
          positions,
        }
      );

      toast.success("Job started");

      console.log("jobId", response.data.job_id);
      setCurrentJobId(response.data.job_id);
    } catch (error) {
      toast.error("Failed to start job");
      console.error(error);
      setCurrentJobId("");
    }
  };

  return {
    running,
    events,
    setEvents,
    positionInfoList,
    setPositionInfoList,
    currentJobId,
    setCurrentJobId,
    companies,
    setCompanies,
    positions,
    setPositions,
    startJob,
  };
};
