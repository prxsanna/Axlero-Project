'use client';

import React, { useState } from 'react';
import MetricsCatalog from '../components/MetricsCatalog';
import ChatInterface from '../components/ChatInterface';

export default function WorkspacePage() {
  const [selectedPrompt, setSelectedPrompt] = useState<string | undefined>(undefined);

  return (
    <main className="flex h-screen w-screen bg-dark-base overflow-hidden">
      {/* Sidebar: Governed Metrics & Dimensions Dictionary */}
      <MetricsCatalog onSelectQuery={(q) => setSelectedPrompt(q)} />

      {/* Main Chat & BI Workspace */}
      <ChatInterface
        externalPrompt={selectedPrompt}
        onClearPrompt={() => setSelectedPrompt(undefined)}
      />
    </main>
  );
}
