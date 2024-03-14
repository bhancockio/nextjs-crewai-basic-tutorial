import React from "react";
import ReactMarkdown from "react-markdown";

type FinalOutputProps = {
  markdown: string;
};

export const FinalOutput: React.FC<FinalOutputProps> = ({ markdown }) => {
  return (
    <div className="flex flex-col h-full">
      <h2 className="text-lg font-semibold my-2">Final Output</h2>
      <div className="flex-grow overflow-auto border-2 border-gray-300 p-2">
        <ReactMarkdown>{markdown}</ReactMarkdown>
      </div>
    </div>
  );
};
