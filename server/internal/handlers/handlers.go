package handlers

import (
	"context"
	"net/http"
	"sync"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"
	"github.com/sirupsen/logrus"
	"github.com/think-ai/server/internal/models"
	"github.com/think-ai/server/internal/services"
)

type Handler struct {
	thinkAI  *services.ThinkAIService
	logger   *logrus.Logger
	upgrader websocket.Upgrader
	
	wsClientsLock sync.RWMutex
	wsClients     map[*websocket.Conn]struct{}
}

func NewHandler(thinkAI *services.ThinkAIService, logger *logrus.Logger) *Handler {
	return &Handler{
		thinkAI: thinkAI,
		logger:  logger,
		upgrader: websocket.Upgrader{
			ReadBufferSize:  1024,
			WriteBufferSize: 1024,
			CheckOrigin: func(r *http.Request) bool {
				return true
			},
		},
		wsClients: make(map[*websocket.Conn]struct{}),
	}
}

func (h *Handler) Think(c *gin.Context) {
	var req models.ThinkRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	
	ctx, cancel := context.WithTimeout(c.Request.Context(), 30*time.Second)
	defer cancel()
	
	result, err := h.thinkAI.Call(ctx, "think", map[string]interface{}{
		"query":           req.Query,
		"context":         req.Context,
		"temperature":     req.Temperature,
		"max_tokens":      req.MaxTokens,
		"consciousness":   req.EnableConsciousness,
	})
	
	if err != nil {
		h.logger.WithError(err).Error("Think request failed")
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	
	c.JSON(http.StatusOK, gin.H{"result": result})
}

func (h *Handler) GenerateCode(c *gin.Context) {
	var req models.CodeGenerationRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	
	ctx, cancel := context.WithTimeout(c.Request.Context(), 60*time.Second)
	defer cancel()
	
	result, err := h.thinkAI.Call(ctx, "generate_code", map[string]interface{}{
		"prompt":      req.Prompt,
		"language":    req.Language,
		"paradigm":    req.Paradigm,
		"complexity":  req.Complexity,
	})
	
	if err != nil {
		h.logger.WithError(err).Error("Code generation failed")
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	
	c.JSON(http.StatusOK, gin.H{"code": result})
}

func (h *Handler) GetIntelligence(c *gin.Context) {
	ctx, cancel := context.WithTimeout(c.Request.Context(), 10*time.Second)
	defer cancel()
	
	result, err := h.thinkAI.Call(ctx, "get_intelligence", map[string]interface{}{})
	
	if err != nil {
		h.logger.WithError(err).Error("Get intelligence failed")
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	
	c.JSON(http.StatusOK, result)
}

func (h *Handler) StartTraining(c *gin.Context) {
	var req models.TrainingRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	
	ctx, cancel := context.WithTimeout(c.Request.Context(), 30*time.Second)
	defer cancel()
	
	result, err := h.thinkAI.Call(ctx, "start_training", map[string]interface{}{
		"mode":            req.Mode,
		"target_iq":       req.TargetIQ,
		"parallel_tests":  req.ParallelTests,
	})
	
	if err != nil {
		h.logger.WithError(err).Error("Start training failed")
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	
	c.JSON(http.StatusOK, gin.H{"training_id": result})
}

func (h *Handler) StopTraining(c *gin.Context) {
	ctx, cancel := context.WithTimeout(c.Request.Context(), 10*time.Second)
	defer cancel()
	
	result, err := h.thinkAI.Call(ctx, "stop_training", map[string]interface{}{})
	
	if err != nil {
		h.logger.WithError(err).Error("Stop training failed")
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	
	c.JSON(http.StatusOK, gin.H{"stopped": result})
}

func (h *Handler) GetTrainingStatus(c *gin.Context) {
	ctx, cancel := context.WithTimeout(c.Request.Context(), 10*time.Second)
	defer cancel()
	
	result, err := h.thinkAI.Call(ctx, "get_training_status", map[string]interface{}{})
	
	if err != nil {
		h.logger.WithError(err).Error("Get training status failed")
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	
	c.JSON(http.StatusOK, result)
}

func (h *Handler) StoreKnowledge(c *gin.Context) {
	var req models.KnowledgeRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	
	ctx, cancel := context.WithTimeout(c.Request.Context(), 30*time.Second)
	defer cancel()
	
	result, err := h.thinkAI.Call(ctx, "store_knowledge", map[string]interface{}{
		"concept":     req.Concept,
		"content":     req.Content,
		"category":    req.Category,
		"metadata":    req.Metadata,
	})
	
	if err != nil {
		h.logger.WithError(err).Error("Store knowledge failed")
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	
	c.JSON(http.StatusOK, gin.H{"stored": result})
}

func (h *Handler) SearchKnowledge(c *gin.Context) {
	query := c.Query("q")
	if query == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "query parameter required"})
		return
	}
	
	ctx, cancel := context.WithTimeout(c.Request.Context(), 20*time.Second)
	defer cancel()
	
	result, err := h.thinkAI.Call(ctx, "search_knowledge", map[string]interface{}{
		"query": query,
		"limit": 10,
	})
	
	if err != nil {
		h.logger.WithError(err).Error("Search knowledge failed")
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	
	c.JSON(http.StatusOK, gin.H{"results": result})
}

func (h *Handler) GetConsciousnessState(c *gin.Context) {
	ctx, cancel := context.WithTimeout(c.Request.Context(), 10*time.Second)
	defer cancel()
	
	result, err := h.thinkAI.Call(ctx, "get_consciousness_state", map[string]interface{}{})
	
	if err != nil {
		h.logger.WithError(err).Error("Get consciousness state failed")
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	
	c.JSON(http.StatusOK, result)
}

func (h *Handler) Health(c *gin.Context) {
	activeRequests := h.thinkAI.GetActiveRequests()
	
	c.JSON(http.StatusOK, gin.H{
		"status":          "healthy",
		"active_requests": activeRequests,
		"timestamp":       time.Now().Unix(),
	})
}

func (h *Handler) WebSocket(c *gin.Context) {
	conn, err := h.upgrader.Upgrade(c.Writer, c.Request, nil)
	if err != nil {
		h.logger.WithError(err).Error("WebSocket upgrade failed")
		return
	}
	defer conn.Close()
	
	h.wsClientsLock.Lock()
	h.wsClients[conn] = struct{}{}
	h.wsClientsLock.Unlock()
	
	defer func() {
		h.wsClientsLock.Lock()
		delete(h.wsClients, conn)
		h.wsClientsLock.Unlock()
	}()
	
	done := make(chan struct{})
	
	go func() {
		defer close(done)
		for {
			messageType, message, err := conn.ReadMessage()
			if err != nil {
				if websocket.IsUnexpectedCloseError(err, websocket.CloseGoingAway, websocket.CloseAbnormalClosure) {
					h.logger.WithError(err).Error("WebSocket read error")
				}
				return
			}
			
			if messageType == websocket.TextMessage {
				h.logger.WithField("message", string(message)).Debug("Received WebSocket message")
			}
		}
	}()
	
	ticker := time.NewTicker(30 * time.Second)
	defer ticker.Stop()
	
	for {
		select {
		case <-done:
			return
		case <-ticker.C:
			ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
			state, err := h.thinkAI.Call(ctx, "get_consciousness_state", map[string]interface{}{})
			cancel()
			
			if err != nil {
				h.logger.WithError(err).Error("Failed to get consciousness state for WebSocket")
				continue
			}
			
			if err := conn.WriteJSON(state); err != nil {
				h.logger.WithError(err).Error("Failed to write WebSocket message")
				return
			}
		}
	}
}

func (h *Handler) broadcast(message interface{}) {
	h.wsClientsLock.RLock()
	defer h.wsClientsLock.RUnlock()
	
	for conn := range h.wsClients {
		if err := conn.WriteJSON(message); err != nil {
			h.logger.WithError(err).Error("Failed to broadcast to WebSocket client")
		}
	}
}