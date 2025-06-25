import { useState } from "react";
import { motion } from "framer-motion";
import { useThinkAIStore } from "../lib/store";
import { getMotionSettings } from "../lib/motion";

export default function QueryInterface() {
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { responses, addResponse } = useThinkAIStore();
  const motionSettings = getMotionSettings();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || isLoading) return;

    setIsLoading(true);

    try {
      const response = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt: query,
          max_length: 5000,
          temperature: 0.7,
          colombian_mode: true,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Handle different response structures
      const responseText =
        data?.generated_text || data?.response || "No response received";
      const consciousnessState = null; // Generate endpoint doesn't return consciousness state

      addResponse({
        id: Date.now().toString(),
        query,
        response: responseText,
        consciousness_state: consciousnessState,
        timestamp: new Date(),
      });

      setQuery("");
    } catch (error) {
      console.error("Query failed:", error);
      addResponse({
        id: Date.now().toString(),
        query,
        response: `Error: ${error instanceof Error ? error.message : "Failed to process query"}`,
        consciousness_state: undefined,
        timestamp: new Date(),
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="relative">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSubmit(e);
            }
          }}
          placeholder="Message the consciousness..."
          className="w-full pl-3 pr-10 py-2 bg-black/30 border border-purple-500/20 rounded-full text-white placeholder-gray-400 focus:outline-none focus:border-purple-500 transition-colors text-sm"
          disabled={isLoading}
        />

        <motion.button
          type="submit"
          disabled={isLoading || !query.trim()}
          whileHover={motionSettings.whileHover}
          whileTap={motionSettings.whileTap}
          className="absolute right-1 top-1/2 -translate-y-1/2 p-1.5 text-purple-400 hover:text-purple-300 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          {isLoading ? (
            <svg
              className="w-4 h-4 animate-spin"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
          ) : (
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
              />
            </svg>
          )}
        </motion.button>
      </form>

      {responses.length > 0 && (
        <div className="space-y-2 max-h-40 overflow-y-auto">
          {responses.map((response, index) => (
            <motion.div
              key={response.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ ...motionSettings.transition, delay: index * 0.05 }}
              className="p-2 bg-black/20 rounded border border-white/5 text-sm"
            >
              <div className="text-sm text-gray-400 mb-2">
                {response.timestamp.toLocaleTimeString()}
              </div>
              <div className="text-purple-400 mb-2">Q: {response.query}</div>
              <div className="text-gray-200">A: {response.response}</div>

              {response.consciousness_state && (
                <div className="mt-3 pt-3 border-t border-white/10 text-xs text-gray-400">
                  <div>
                    Attention: {response.consciousness_state.attention_focus}
                  </div>
                  <div>
                    Flow: {response.consciousness_state.consciousness_flow}
                  </div>
                </div>
              )}
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
