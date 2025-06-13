package services

import (
	"bufio"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"os/exec"
	"sync"
	"sync/atomic"
	"time"

	"github.com/patrickmn/go-cache"
	"github.com/sirupsen/logrus"
	"github.com/spf13/viper"
	"golang.org/x/sync/semaphore"
)

type ThinkAIService struct {
	logger        *logrus.Logger
	pythonCmd     *exec.Cmd
	stdin         io.WriteCloser
	stdout        io.ReadCloser
	stderr        io.ReadCloser
	
	cache         *cache.Cache
	requestPool   sync.Pool
	responsePool  sync.Pool
	
	semaphore     *semaphore.Weighted
	activeRequests atomic.Int64
	
	mu            sync.RWMutex
	initialized   bool
	shutdownCh    chan struct{}
}

type ThinkRequest struct {
	ID      string                 `json:"id"`
	Method  string                 `json:"method"`
	Params  map[string]interface{} `json:"params"`
}

type ThinkResponse struct {
	ID      string                 `json:"id"`
	Result  interface{}            `json:"result,omitempty"`
	Error   *ThinkError            `json:"error,omitempty"`
}

type ThinkError struct {
	Code    int    `json:"code"`
	Message string `json:"message"`
}

func NewThinkAIService(logger *logrus.Logger) *ThinkAIService {
	cacheTTL, _ := time.ParseDuration(viper.GetString("cache.ttl"))
	
	return &ThinkAIService{
		logger:     logger,
		cache:      cache.New(cacheTTL, cacheTTL*2),
		semaphore:  semaphore.NewWeighted(100),
		shutdownCh: make(chan struct{}),
		requestPool: sync.Pool{
			New: func() interface{} {
				return &ThinkRequest{}
			},
		},
		responsePool: sync.Pool{
			New: func() interface{} {
				return &ThinkResponse{}
			},
		},
	}
}

func (s *ThinkAIService) Initialize() error {
	s.mu.Lock()
	defer s.mu.Unlock()
	
	if s.initialized {
		return nil
	}
	
	pythonExec := viper.GetString("python.executable")
	pythonModule := viper.GetString("python.module")
	
	s.pythonCmd = exec.Command(pythonExec, "-m", pythonModule)
	
	stdin, err := s.pythonCmd.StdinPipe()
	if err != nil {
		return fmt.Errorf("failed to create stdin pipe: %w", err)
	}
	s.stdin = stdin
	
	stdout, err := s.pythonCmd.StdoutPipe()
	if err != nil {
		return fmt.Errorf("failed to create stdout pipe: %w", err)
	}
	s.stdout = stdout
	
	stderr, err := s.pythonCmd.StderrPipe()
	if err != nil {
		return fmt.Errorf("failed to create stderr pipe: %w", err)
	}
	s.stderr = stderr
	
	if err := s.pythonCmd.Start(); err != nil {
		return fmt.Errorf("failed to start Python process: %w", err)
	}
	
	go s.handleStderr()
	
	s.initialized = true
	s.logger.Info("ThinkAI service initialized successfully")
	
	return nil
}

func (s *ThinkAIService) Call(ctx context.Context, method string, params map[string]interface{}) (interface{}, error) {
	cacheKey := s.generateCacheKey(method, params)
	
	if cached, found := s.cache.Get(cacheKey); found {
		s.logger.WithField("method", method).Debug("Cache hit")
		return cached, nil
	}
	
	if err := s.semaphore.Acquire(ctx, 1); err != nil {
		return nil, fmt.Errorf("failed to acquire semaphore: %w", err)
	}
	defer s.semaphore.Release(1)
	
	s.activeRequests.Add(1)
	defer s.activeRequests.Add(-1)
	
	req := s.requestPool.Get().(*ThinkRequest)
	defer s.requestPool.Put(req)
	
	req.ID = fmt.Sprintf("%d", time.Now().UnixNano())
	req.Method = method
	req.Params = params
	
	s.mu.RLock()
	if !s.initialized {
		s.mu.RUnlock()
		return nil, fmt.Errorf("service not initialized")
	}
	stdin := s.stdin
	s.mu.RUnlock()
	
	reqJSON, err := json.Marshal(req)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal request: %w", err)
	}
	
	if _, err := stdin.Write(append(reqJSON, '\n')); err != nil {
		return nil, fmt.Errorf("failed to write request: %w", err)
	}
	
	responseCh := make(chan *ThinkResponse, 1)
	errorCh := make(chan error, 1)
	
	go func() {
		scanner := bufio.NewScanner(s.stdout)
		for scanner.Scan() {
			resp := s.responsePool.Get().(*ThinkResponse)
			if err := json.Unmarshal(scanner.Bytes(), resp); err != nil {
				s.responsePool.Put(resp)
				errorCh <- fmt.Errorf("failed to unmarshal response: %w", err)
				return
			}
			
			if resp.ID == req.ID {
				responseCh <- resp
				return
			}
			s.responsePool.Put(resp)
		}
		
		if err := scanner.Err(); err != nil {
			errorCh <- fmt.Errorf("scanner error: %w", err)
		}
	}()
	
	select {
	case <-ctx.Done():
		return nil, ctx.Err()
	case err := <-errorCh:
		return nil, err
	case resp := <-responseCh:
		defer s.responsePool.Put(resp)
		
		if resp.Error != nil {
			return nil, fmt.Errorf("ThinkAI error: %s", resp.Error.Message)
		}
		
		if s.isCacheable(method) {
			s.cache.Set(cacheKey, resp.Result, cache.DefaultExpiration)
		}
		
		return resp.Result, nil
	case <-time.After(30 * time.Second):
		return nil, fmt.Errorf("request timeout")
	}
}

func (s *ThinkAIService) generateCacheKey(method string, params map[string]interface{}) string {
	paramsJSON, _ := json.Marshal(params)
	return fmt.Sprintf("%s:%s", method, string(paramsJSON))
}

func (s *ThinkAIService) isCacheable(method string) bool {
	switch method {
	case "get_intelligence", "search_knowledge", "get_consciousness_state":
		return true
	default:
		return false
	}
}

func (s *ThinkAIService) handleStderr() {
	scanner := bufio.NewScanner(s.stderr)
	for scanner.Scan() {
		s.logger.WithField("stderr", scanner.Text()).Debug("Python stderr")
	}
}

func (s *ThinkAIService) GetActiveRequests() int64 {
	return s.activeRequests.Load()
}

func (s *ThinkAIService) Shutdown() error {
	s.mu.Lock()
	defer s.mu.Unlock()
	
	if !s.initialized {
		return nil
	}
	
	close(s.shutdownCh)
	
	s.stdin.Close()
	s.stdout.Close()
	s.stderr.Close()
	
	if err := s.pythonCmd.Process.Kill(); err != nil {
		s.logger.WithError(err).Error("Failed to kill Python process")
	}
	
	s.initialized = false
	s.logger.Info("ThinkAI service shut down")
	
	return nil
}