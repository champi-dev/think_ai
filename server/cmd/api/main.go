package main

import (
	"context"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"
	"github.com/spf13/viper"
	"github.com/think-ai/server/internal/handlers"
	"github.com/think-ai/server/internal/middleware"
	"github.com/think-ai/server/internal/services"
)

func init() {
	viper.SetDefault("server.port", "8080")
	viper.SetDefault("server.mode", "release")
	viper.SetDefault("python.executable", "python3")
	viper.SetDefault("python.module", "think_ai.api.bridge")
	viper.SetDefault("cache.ttl", "5m")
	viper.SetDefault("cache.size", 10000)
	
	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath(".")
	viper.AddConfigPath("./config")
	
	viper.AutomaticEnv()
	
	if err := viper.ReadInConfig(); err != nil {
		logrus.WithError(err).Info("No config file found, using defaults")
	}
}

func main() {
	logger := logrus.New()
	logger.SetFormatter(&logrus.JSONFormatter{})
	
	if viper.GetString("server.mode") == "debug" {
		logger.SetLevel(logrus.DebugLevel)
		gin.SetMode(gin.DebugMode)
	} else {
		logger.SetLevel(logrus.InfoLevel)
		gin.SetMode(gin.ReleaseMode)
	}
	
	thinkAIService := services.NewThinkAIService(logger)
	if err := thinkAIService.Initialize(); err != nil {
		logger.WithError(err).Fatal("Failed to initialize ThinkAI service")
	}
	defer thinkAIService.Shutdown()
	
	router := gin.New()
	router.Use(gin.Recovery())
	router.Use(middleware.Logger(logger))
	router.Use(middleware.CORS())
	router.Use(middleware.RateLimiter())
	
	h := handlers.NewHandler(thinkAIService, logger)
	
	v1 := router.Group("/api/v1")
	{
		v1.POST("/think", h.Think)
		v1.POST("/generate-code", h.GenerateCode)
		v1.GET("/intelligence", h.GetIntelligence)
		v1.POST("/training/start", h.StartTraining)
		v1.POST("/training/stop", h.StopTraining)
		v1.GET("/training/status", h.GetTrainingStatus)
		v1.POST("/knowledge/store", h.StoreKnowledge)
		v1.POST("/knowledge/search", h.SearchKnowledge)
		v1.GET("/consciousness/state", h.GetConsciousnessState)
		v1.GET("/health", h.Health)
		v1.GET("/ws", h.WebSocket)
	}
	
	srv := &http.Server{
		Addr:           ":" + viper.GetString("server.port"),
		Handler:        router,
		ReadTimeout:    10 * time.Second,
		WriteTimeout:   60 * time.Second,
		MaxHeaderBytes: 1 << 20,
	}
	
	go func() {
		logger.WithField("port", viper.GetString("server.port")).Info("Server starting")
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			logger.WithError(err).Fatal("Server failed to start")
		}
	}()
	
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	
	logger.Info("Shutting down server...")
	
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()
	
	if err := srv.Shutdown(ctx); err != nil {
		logger.WithError(err).Fatal("Server forced to shutdown")
	}
	
	logger.Info("Server exited")
}