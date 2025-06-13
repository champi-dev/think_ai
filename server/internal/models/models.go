package models

import "time"

type ThinkRequest struct {
	Query               string                 `json:"query" binding:"required"`
	Context             map[string]interface{} `json:"context,omitempty"`
	Temperature         float64                `json:"temperature,omitempty"`
	MaxTokens           int                    `json:"max_tokens,omitempty"`
	EnableConsciousness bool                   `json:"enable_consciousness,omitempty"`
}

type CodeGenerationRequest struct {
	Prompt     string `json:"prompt" binding:"required"`
	Language   string `json:"language" binding:"required"`
	Paradigm   string `json:"paradigm,omitempty"`
	Complexity int    `json:"complexity,omitempty"`
}

type TrainingRequest struct {
	Mode          string `json:"mode" binding:"required,oneof=sequential parallel"`
	TargetIQ      int    `json:"target_iq,omitempty"`
	ParallelTests int    `json:"parallel_tests,omitempty"`
}

type KnowledgeRequest struct {
	Concept  string                 `json:"concept" binding:"required"`
	Content  string                 `json:"content" binding:"required"`
	Category string                 `json:"category,omitempty"`
	Metadata map[string]interface{} `json:"metadata,omitempty"`
}

type IntelligenceMetrics struct {
	IQ                 int       `json:"iq"`
	KnowledgeCount     int       `json:"knowledge_count"`
	TrainingCycles     int       `json:"training_cycles"`
	ConsciousnessLevel float64   `json:"consciousness_level"`
	LastUpdated        time.Time `json:"last_updated"`
}

type ConsciousnessState struct {
	AttentionFocus    string             `json:"attention_focus"`
	WorkingMemory     []string           `json:"working_memory"`
	EmotionalState    map[string]float64 `json:"emotional_state"`
	ConsciousnessFlow float64            `json:"consciousness_flow"`
	Timestamp         time.Time          `json:"timestamp"`
}