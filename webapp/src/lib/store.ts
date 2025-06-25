import { create } from "zustand";

interface ThinkAIStore {
  consciousnessState: any;
  setConsciousnessState: (state: any) => void;
  intelligenceMetrics: any;
  setIntelligenceMetrics: (metrics: any) => void;
  responses: any[];
  addResponse: (response: any) => void;
}

export const useThinkAIStore = create<ThinkAIStore>((set) => ({
  consciousnessState: null,
  setConsciousnessState: (state) => set({ consciousnessState: state }),
  intelligenceMetrics: null,
  setIntelligenceMetrics: (metrics) => set({ intelligenceMetrics: metrics }),
  responses: [],
  addResponse: (response) =>
    set((state) => ({ responses: [...state.responses, response] })),
}));
