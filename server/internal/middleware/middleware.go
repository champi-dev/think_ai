package middleware

import (
	"net/http"
	"sync"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/patrickmn/go-cache"
	"github.com/sirupsen/logrus"
)

func Logger(logger *logrus.Logger) gin.HandlerFunc {
	return func(c *gin.Context) {
		start := time.Now()
		path := c.Request.URL.Path
		raw := c.Request.URL.RawQuery
		
		c.Next()
		
		latency := time.Since(start)
		clientIP := c.ClientIP()
		method := c.Request.Method
		statusCode := c.Writer.Status()
		
		entry := logger.WithFields(logrus.Fields{
			"status_code": statusCode,
			"latency":     latency,
			"client_ip":   clientIP,
			"method":      method,
			"path":        path,
		})
		
		if raw != "" {
			entry = entry.WithField("query", raw)
		}
		
		if len(c.Errors) > 0 {
			entry.Error(c.Errors.String())
		} else {
			entry.Info("Request processed")
		}
	}
}

func CORS() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT, DELETE")
		
		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}
		
		c.Next()
	}
}

type rateLimiter struct {
	requests *cache.Cache
	mu       sync.RWMutex
}

func RateLimiter() gin.HandlerFunc {
	rl := &rateLimiter{
		requests: cache.New(1*time.Minute, 2*time.Minute),
	}
	
	return func(c *gin.Context) {
		clientIP := c.ClientIP()
		
		rl.mu.Lock()
		defer rl.mu.Unlock()
		
		count, found := rl.requests.Get(clientIP)
		if !found {
			rl.requests.Set(clientIP, 1, cache.DefaultExpiration)
			c.Next()
			return
		}
		
		requestCount := count.(int)
		if requestCount >= 100 {
			c.JSON(http.StatusTooManyRequests, gin.H{
				"error": "Rate limit exceeded. Maximum 100 requests per minute.",
			})
			c.Abort()
			return
		}
		
		rl.requests.Set(clientIP, requestCount+1, cache.DefaultExpiration)
		c.Next()
	}
}