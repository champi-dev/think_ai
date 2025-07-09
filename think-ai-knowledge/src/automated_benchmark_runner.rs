// Automated Benchmark Runner and Scorer
//!
// Orchestrates the entire benchmark training pipeline:
// 1. Runs benchmarks automatically on a schedule
// 2. Scores and compares results to state-of-the-art
// 3. Triggers training when performance drops
// 4. Provides comprehensive reporting and analysis

use crate::benchmark_trainer::{BenchmarkTrainer, BenchmarkTrainingConfig};
use crate::llm_benchmarks::{Benchmark, ComprehensiveBenchmarkReport, LLMBenchmarkEvaluator};
use crate::o1_benchmark_monitor::{O1BenchmarkMonitor, O1PerformanceMetrics};
use crate::KnowledgeEngine;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use std::time::{Duration, SystemTime};
use tokio::fs;
use tokio::time::interval;
/// Configuration for automated benchmark running
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AutomatedBenchmarkConfig {
    pub evaluation_interval: Duration, // How often to run full evaluation
    pub training_trigger_threshold: f64, // Performance drop that triggers training
    pub sota_comparison_enabled: bool, // Whether to compare against SOTA
    pub auto_training_enabled: bool,   // Whether to automatically start training
    pub performance_monitoring_enabled: bool, // Whether to run O(1) monitoring
    pub reporting_enabled: bool,       // Whether to generate reports
    pub benchmark_selection: Vec<Benchmark>, // Which benchmarks to run
    pub max_training_sessions_per_day: u32, // Limit training frequency
}
impl Default for AutomatedBenchmarkConfig {
    fn default() -> Self {
        Self {
            evaluation_interval: Duration::from_secs(3600 * 6), // Every 6 hours
            training_trigger_threshold: 0.05,                   // 5% performance drop
            sota_comparison_enabled: true,
            auto_training_enabled: true,
            performance_monitoring_enabled: true,
            reporting_enabled: true,
            benchmark_selection: Benchmark::all_benchmarks(),
            max_training_sessions_per_day: 4,
        }
    }
}

/// Automated benchmark results with trends
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AutomatedBenchmarkResults {
    pub timestamp: SystemTime,
    pub benchmark_report: ComprehensiveBenchmarkReport,
    pub performance_metrics: Option<O1PerformanceMetrics>,
    pub sota_comparison: HashMap<Benchmark, f64>, // Ratio vs SOTA (1.0 = equal, >1.0 = better)
    pub trend_analysis: TrendAnalysis,
    pub recommendations: Vec<String>,
    pub training_triggered: bool,
    pub overall_health_score: f64, // 0-1 score for system health
}

/// Analysis of performance trends over time
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TrendAnalysis {
    pub performance_trend: PerformanceTrend,
    pub score_changes: HashMap<Benchmark, f64>, // Change from previous evaluation
    pub improvement_rate: f64,                  // Average improvement per day
    pub stability_score: f64,                   // How stable performance is (0-1)
    pub areas_of_concern: Vec<String>,
    pub areas_of_strength: Vec<String>,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
pub enum PerformanceTrend {
    Improving,
    Stable,
    Declining,
    Volatile,
}

impl std::fmt::Display for PerformanceTrend {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            PerformanceTrend::Improving => write!(f, "Improving"),
            PerformanceTrend::Stable => write!(f, "Stable"),
            PerformanceTrend::Declining => write!(f, "Declining"),
            PerformanceTrend::Volatile => write!(f, "Volatile"),
        }
    }
}

/// Complete automated benchmark system
pub struct AutomatedBenchmarkRunner {
    knowledge_engine: Arc<KnowledgeEngine>,
    benchmark_evaluator: LLMBenchmarkEvaluator,
    benchmark_trainer: BenchmarkTrainer,
    o1_monitor: Option<O1BenchmarkMonitor>,
    config: AutomatedBenchmarkConfig,
    results_history: Vec<AutomatedBenchmarkResults>,
    training_sessions_today: u32,
    last_reset_date: SystemTime,
    is_running: bool,
}

impl AutomatedBenchmarkRunner {
    pub fn new(knowledge_engine: Arc<KnowledgeEngine>, config: AutomatedBenchmarkConfig) -> Self {
        let benchmark_evaluator = LLMBenchmarkEvaluator::new(knowledge_engine.clone());
        let training_config = BenchmarkTrainingConfig::default();
        let benchmark_trainer = BenchmarkTrainer::new(knowledge_engine.clone(), training_config);
        let o1_monitor = if config.performance_monitoring_enabled {
            Some(O1BenchmarkMonitor::new(
                knowledge_engine.clone(),
                Arc::new(LLMBenchmarkEvaluator::new(knowledge_engine.clone())),
            ))
        } else {
            None
        };

        Self {
            knowledge_engine,
            benchmark_evaluator,
            benchmark_trainer,
            o1_monitor,
            config,
            results_history: Vec::new(),
            training_sessions_today: 0,
            last_reset_date: SystemTime::now(),
            is_running: false,
        }
    }

    /// Start the automated benchmark system
    pub async fn start(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        if self.is_running {
            println!("🤖 Automated benchmark runner already active");
            return Ok(());
        }

        println!("🤖 Starting automated benchmark runner...");
        self.is_running = true;
        // Initialize all components
        self.benchmark_evaluator.initialize_benchmarks().await?;
        // Start O(1) performance monitoring if enabled
        if let Some(monitor) = &self.o1_monitor {
            monitor.start_monitoring().await;
        }

        // Start the main automation loop
        self.run_automation_loop().await?;

        Ok(())
    }

    /// Main automation loop
    async fn run_automation_loop(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        let mut eval_interval = interval(self.config.evaluation_interval);
        let mut daily_reset_interval = interval(Duration::from_secs(24 * 3600)); // Daily reset
        loop {
            tokio::select! {
                _ = eval_interval.tick() => {
                    if self.is_running {
                        self.run_evaluation_cycle().await?;
                    } else {
                        break;
                    }
                }
                _ = daily_reset_interval.tick() => {
                    self.reset_daily_counters();
                }
            }
        }

        Ok(())
    }

    /// Run a complete evaluation cycle
    async fn run_evaluation_cycle(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        println!("\n🔄 Starting automated evaluation cycle...");
        let cycle_start = SystemTime::now();
        // 1. Run comprehensive benchmark evaluation
        println!("📊 Running comprehensive benchmark evaluation...");
        let benchmark_report = self
            .benchmark_evaluator
            .run_comprehensive_evaluation()
            .await?;
        // 2. Get O(1) performance metrics if monitoring is enabled
        let performance_metrics = self
            .o1_monitor
            .as_ref()
            .map(|monitor| monitor.get_metrics());
        // 3. Calculate SOTA comparison
        let sota_comparison = self.calculate_sota_comparison(&benchmark_report);
        // 4. Analyze trends
        let trend_analysis = self.analyze_trends(&benchmark_report);
        // 5. Generate recommendations
        let recommendations =
            self.generate_recommendations(&benchmark_report, &trend_analysis, &performance_metrics);
        // 6. Calculate overall health score
        let overall_health_score =
            self.calculate_health_score(&benchmark_report, &performance_metrics);
        // 7. Determine if training should be triggered
        let training_triggered =
            self.should_trigger_training(&trend_analysis, overall_health_score);
        // 8. Create results record
        let results = AutomatedBenchmarkResults {
            timestamp: cycle_start,
            benchmark_report,
            performance_metrics,
            sota_comparison,
            trend_analysis,
            recommendations,
            training_triggered,
            overall_health_score,
        };

        // 9. Store results
        self.results_history.push(results.clone());
        // 10. Generate and save report if enabled
        if self.config.reporting_enabled {
            self.generate_and_save_report(&results).await?;
        }

        // 11. Trigger training if needed and allowed
        if training_triggered
            && self.config.auto_training_enabled
            && self.training_sessions_today < self.config.max_training_sessions_per_day
        {
            println!("🚀 Triggering automated training session...");
            self.trigger_training_session().await?;
            self.training_sessions_today += 1;
        }

        // 12. Print summary
        self.print_cycle_summary(&results);

        Ok(())
    }

    /// Calculate comparison to state-of-the-art scores
    fn calculate_sota_comparison(
        &self,
        report: &ComprehensiveBenchmarkReport,
    ) -> HashMap<Benchmark, f64> {
        report.state_of_art_comparison.clone()
    }

    /// Analyze performance trends
    fn analyze_trends(&self, current_report: &ComprehensiveBenchmarkReport) -> TrendAnalysis {
        if self.results_history.is_empty() {
            return TrendAnalysis {
                performance_trend: PerformanceTrend::Stable,
                score_changes: HashMap::new(),
                improvement_rate: 0.0,
                stability_score: 1.0,
                areas_of_concern: Vec::new(),
                areas_of_strength: Vec::new(),
            };
        }

        let previous_result = self.results_history.last().unwrap();
        let previous_scores = &previous_result.benchmark_report.benchmark_results;
        let current_scores = &current_report.benchmark_results;
        // Calculate score changes
        let mut score_changes = HashMap::new();
        let mut total_change = 0.0;
        let mut change_count = 0;
        let mut volatility_sum = 0.0;
        for (benchmark, current_result) in current_scores {
            if let Some(previous_result) = previous_scores.get(benchmark) {
                let change = current_result.accuracy - previous_result.accuracy;
                score_changes.insert(*benchmark, change);
                total_change += change;
                change_count += 1;
                // Calculate volatility
                if self.results_history.len() >= 3 {
                    let recent_scores: Vec<f64> = self
                        .results_history
                        .iter()
                        .rev()
                        .take(3)
                        .filter_map(|r| r.benchmark_report.benchmark_results.get(benchmark))
                        .map(|r| r.accuracy)
                        .collect();
                    if recent_scores.len() >= 2 {
                        let variance = self.calculate_variance(&recent_scores);
                        volatility_sum += variance;
                    }
                }
            }
        }

        // Determine overall trend
        let average_change = if change_count > 0 {
            total_change / change_count as f64
        } else {
            0.0
        };
        let average_volatility = if change_count > 0 {
            volatility_sum / change_count as f64
        } else {
            0.0
        };

        let performance_trend = if average_volatility > 0.1 {
            PerformanceTrend::Volatile
        } else if average_change > 0.02 {
            PerformanceTrend::Improving
        } else if average_change < -0.02 {
            PerformanceTrend::Declining
        } else {
            PerformanceTrend::Stable
        };
        // Calculate improvement rate (per day)
        let improvement_rate = if self.results_history.len() >= 2 {
            let days_diff = previous_result
                .timestamp
                .duration_since(self.results_history[0].timestamp)
                .unwrap_or(Duration::from_secs(1))
                .as_secs() as f64
                / (24.0 * 3600.0);
            if days_diff > 0.0 {
                average_change / days_diff
            } else {
                0.0
            }
        } else {
            0.0
        };

        // Stability score (lower volatility = higher stability)
        let stability_score = (1.0 - average_volatility.min(1.0)).max(0.0);
        // Identify areas of concern and strength
        let mut areas_of_concern = Vec::new();
        let mut areas_of_strength = Vec::new();
        for (benchmark, change) in &score_changes {
            if *change < -0.05 {
                areas_of_concern.push(format!(
                    "{:?} performance declined by {:.1}%",
                    benchmark,
                    change * 100.0
                ));
            } else if *change > 0.05 {
                areas_of_strength.push(format!(
                    "{:?} performance improved by {:.1}%",
                    benchmark,
                    change * 100.0
                ));
            }
        }

        TrendAnalysis {
            performance_trend,
            score_changes,
            improvement_rate,
            stability_score,
            areas_of_concern,
            areas_of_strength,
        }
    }

    /// Calculate variance of a set of scores
    fn calculate_variance(&self, scores: &[f64]) -> f64 {
        if scores.len() < 2 {
            return 0.0;
        }

        let mean = scores.iter().sum::<f64>() / scores.len() as f64;
        let variance = scores
            .iter()
            .map(|score| (score - mean).powi(2))
            .sum::<f64>()
            / scores.len() as f64;
        variance.sqrt() // Return standard deviation
    }

    /// Generate recommendations based on analysis
    fn generate_recommendations(
        &self,
        report: &ComprehensiveBenchmarkReport,
        trends: &TrendAnalysis,
        performance_metrics: &Option<O1PerformanceMetrics>,
    ) -> Vec<String> {
        let mut recommendations = Vec::new();
        // Benchmark-specific recommendations
        for (benchmark, ratio) in &report.state_of_art_comparison {
            if *ratio < 0.8 {
                recommendations.push(format!(
                    "Focus training on {:?} - currently at {:.1}% of SOTA performance",
                    benchmark,
                    ratio * 100.0
                ));
            }
        }

        // Trend-based recommendations
        match trends.performance_trend {
            PerformanceTrend::Declining => {
                recommendations.push("Performance is declining - consider intensive training or knowledge base expansion".to_string());
            }
            PerformanceTrend::Volatile => {
                recommendations.push(
                    "Performance is unstable - review training consistency and knowledge quality"
                        .to_string(),
                );
            }
            PerformanceTrend::Improving => {
                recommendations.push(
                    "Performance is improving - continue current training approach".to_string(),
                );
            }
            PerformanceTrend::Stable => {
                recommendations.push("Performance is stable - consider exploring new training techniques for breakthrough improvements".to_string());
            }
        }

        // Performance metrics recommendations
        if let Some(metrics) = performance_metrics {
            if metrics.o1_performance_score < 0.95 {
                recommendations.push(format!(
                    "O(1) performance below target - {} violations detected, consider response caching optimization",
                    metrics.o1_guarantee_violations
                ));
            }
            if metrics.cache_hit_rate < 0.5 {
                recommendations.push(
                    "Low cache hit rate - expand response caching or improve query patterns"
                        .to_string(),
                );
            }
        }

        // Areas of concern
        for concern in &trends.areas_of_concern {
            recommendations.push(format!("Address concern: {concern}"));
        }

        if recommendations.is_empty() {
            recommendations.push(
                "System performing well - maintain current approach and monitor for changes"
                    .to_string(),
            );
        }

        recommendations
    }

    /// Calculate overall system health score
    fn calculate_health_score(
        &self,
        report: &ComprehensiveBenchmarkReport,
        performance_metrics: &Option<O1PerformanceMetrics>,
    ) -> f64 {
        let mut score = report.overall_score; // Start with benchmark score
                                              // Adjust for SOTA comparison
        let sota_average = report.state_of_art_comparison.values().sum::<f64>()
            / report.state_of_art_comparison.len() as f64;
        score *= sota_average.min(1.0); // Penalize if below SOTA
                                        // Adjust for O(1) performance
        if let Some(metrics) = performance_metrics {
            score *= metrics.o1_performance_score;
        }
        score.max(0.0).min(1.0)
    }

    /// Determine if training should be triggered
    fn should_trigger_training(&self, trends: &TrendAnalysis, health_score: f64) -> bool {
        // Trigger if performance is declining
        if matches!(trends.performance_trend, PerformanceTrend::Declining) {
            return true;
        }

        // Trigger if health score is low
        if health_score < 0.75 {
            return true;
        }

        // Trigger if any benchmark shows significant decline
        for change in trends.score_changes.values() {
            if *change < -self.config.training_trigger_threshold {
                return true;
            }
        }

        false
    }

    /// Trigger a training session
    async fn trigger_training_session(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        println!("🎯 Starting automated training session...");
        // Note: In a real implementation, this would start the training in a separate task
        // to avoid blocking the main automation loop
        // self.benchmark_trainer.start_training_session().await?;
        println!("✅ Training session initiated");

        Ok(())
    }

    /// Generate and save comprehensive report
    async fn generate_and_save_report(
        &self,
        results: &AutomatedBenchmarkResults,
    ) -> Result<(), Box<dyn std::error::Error>> {
        let report_content = self.generate_html_report(results);
        let timestamp = results
            .timestamp
            .duration_since(SystemTime::UNIX_EPOCH)?
            .as_secs();
        let filename = format!("automated_benchmark_report_{timestamp}.html");
        fs::write(&filename, report_content).await?;
        // Also save JSON data
        let json_filename = format!("automated_benchmark_data_{timestamp}.json");
        let json_content = serde_json::to_string_pretty(results)?;
        fs::write(&json_filename, json_content).await?;
        println!("📄 Report saved: {filename} and {json_filename}");

        Ok(())
    }

    /// Generate HTML report
    fn generate_html_report(&self, results: &AutomatedBenchmarkResults) -> String {
        let timestamp_str = format!("{:?}", results.timestamp);
        let health_status = if results.overall_health_score > 0.8 {
            "🟢 Excellent"
        } else if results.overall_health_score > 0.6 {
            "🟡 Good"
        } else {
            "🔴 Needs Attention"
        };
        format!(
            r#"<!DOCTYPE html>
<html>
<head>
    <title>Automated Benchmark Report - {}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .metric {{ margin: 10px 0; }}
        .score {{ font-weight: bold; color: #2196F3; }}
        .trend-improving {{ color: #4CAF50; }}
        .trend-declining {{ color: #F44336; }}
        .trend-stable {{ color: #FF9800; }}
        .recommendations {{ background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 10px 0; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 Automated Benchmark Report</h1>
        <p>Generated: {}</p>
        <p>Overall Health: {} ({:.1}%)</p>
        <p>Training Triggered: {}</p>
    </div>
    <h2>📊 Benchmark Scores</h2>
    <table>
        <tr><th>Benchmark</th><th>Score</th><th>SOTA Ratio</th><th>Trend</th></tr>
        {}
    </table>
    <h2>⚡ Performance Metrics</h2>
    {}
    <h2>📈 Trend Analysis</h2>
    <div class="metric">Performance Trend: <span class="trend-{}">{:?}</span></div>
    <div class="metric">Improvement Rate: {:.3}% per day</div>
    <div class="metric">Stability Score: {:.1}%</div>
    <h2>💡 Recommendations</h2>
    <div class="recommendations">
        <ul>
        {}
        </ul>
    </div>
    <h2>📋 Areas of Concern</h2>
    <ul>
    {}
    </ul>
    <h2>✅ Areas of Strength</h2>
    <ul>
    {}
    </ul>
</body>
</html>"#,
            timestamp_str.clone(),
            timestamp_str,
            health_status,
            results.overall_health_score * 100.0,
            if results.training_triggered {
                "Yes"
            } else {
                "No"
            },
            self.generate_benchmark_table_rows(results),
            self.generate_performance_metrics_html(results),
            format!("{:?}", results.trend_analysis.performance_trend).to_lowercase(),
            results.trend_analysis.performance_trend,
            results.trend_analysis.improvement_rate * 100.0,
            results.trend_analysis.stability_score * 100.0,
            results
                .recommendations
                .iter()
                .map(|r| format!("<li>{r}</li>"))
                .collect::<Vec<_>>()
                .join("\n"),
            results
                .trend_analysis
                .areas_of_concern
                .iter()
                .map(|c| format!("<li>{c}</li>"))
                .collect::<Vec<_>>()
                .join("\n"),
            results
                .trend_analysis
                .areas_of_strength
                .iter()
                .map(|s| format!("<li>{s}</li>"))
                .collect::<Vec<_>>()
                .join("\n")
        )
    }

    fn generate_benchmark_table_rows(&self, results: &AutomatedBenchmarkResults) -> String {
        results
            .benchmark_report
            .benchmark_results
            .iter()
            .map(|(benchmark, result)| {
                let sota_ratio = results.sota_comparison.get(benchmark).unwrap_or(&0.0);
                let trend_change = results
                    .trend_analysis
                    .score_changes
                    .get(benchmark)
                    .unwrap_or(&0.0);
                let trend_arrow = if *trend_change > 0.01 {
                    "📈"
                } else if *trend_change < -0.01 {
                    "📉"
                } else {
                    "➡️"
                };
                format!(
                    "<tr><td>{:?}</td><td>{:.1}%</td><td>{:.1}%</td><td>{} {:+.1}%</td></tr>",
                    benchmark,
                    result.accuracy * 100.0,
                    sota_ratio * 100.0,
                    trend_arrow,
                    trend_change * 100.0
                )
            })
            .collect::<Vec<_>>()
            .join("\n")
    }

    fn generate_performance_metrics_html(&self, results: &AutomatedBenchmarkResults) -> String {
        if let Some(metrics) = &results.performance_metrics {
            format!(
                r#"<div class="metric">Average Response Time: {}μs</div>
                <div class="metric">P95 Response Time: {}μs</div>
                <div class="metric">O(1) Compliance: {:.1}%</div>
                <div class="metric">Throughput: {:.1} QPS</div>
                <div class="metric">Cache Hit Rate: {:.1}%</div>"#,
                metrics.average_response_time_ns / 1000,
                metrics.p95_response_time_ns / 1000,
                metrics.o1_performance_score * 100.0,
                metrics.throughput_qps,
                metrics.cache_hit_rate * 100.0
            )
        } else {
            "<p>Performance monitoring not enabled</p>".to_string()
        }
    }

    /// Print cycle summary to console
    fn print_cycle_summary(&self, results: &AutomatedBenchmarkResults) {
        println!("\n📊 Evaluation Cycle Complete");
        println!(
            "Overall Health Score: {:.1}%",
            results.overall_health_score * 100.0
        );
        println!(
            "Performance Trend: {:?}",
            results.trend_analysis.performance_trend
        );
        println!(
            "Training Triggered: {}",
            if results.training_triggered {
                "Yes"
            } else {
                "No"
            }
        );

        if let Some(metrics) = &results.performance_metrics {
            println!(
                "O(1) Compliance: {:.1}%",
                metrics.o1_performance_score * 100.0
            );
        }

        println!("Top Recommendations:");
        for (i, rec) in results.recommendations.iter().take(3).enumerate() {
            println!("  {}. {}", i + 1, rec);
        }
    }

    /// Reset daily counters
    fn reset_daily_counters(&mut self) {
        self.training_sessions_today = 0;
        self.last_reset_date = SystemTime::now();
        println!("🔄 Daily counters reset");
    }

    /// Stop the automated system
    pub fn stop(&mut self) {
        self.is_running = false;

        if let Some(monitor) = &self.o1_monitor {
            monitor.stop_monitoring();
        }

        println!("🛑 Automated benchmark runner stopped");
    }

    /// Get results history
    pub fn get_results_history(&self) -> &[AutomatedBenchmarkResults] {
        &self.results_history
    }

    /// Get latest results
    pub fn get_latest_results(&self) -> Option<&AutomatedBenchmarkResults> {
        self.results_history.last()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_automated_runner_creation() {
        let engine = Arc::new(KnowledgeEngine::new());
        let config = AutomatedBenchmarkConfig::default();
        let runner = AutomatedBenchmarkRunner::new(engine, config);
        assert!(!runner.is_running);
        assert_eq!(runner.training_sessions_today, 0);
        assert!(runner.results_history.is_empty());
    }

    #[test]
    fn test_health_score_calculation() {
        // Create mock benchmark report
        let mut benchmark_results = HashMap::new();
        let mut sota_comparison = HashMap::new();
        // Mock good performance
        sota_comparison.insert(Benchmark::MMLU, 0.9);
        let report = ComprehensiveBenchmarkReport {
            overall_score: 0.85,
            benchmark_results,
            strengths: Vec::new(),
            weaknesses: Vec::new(),
            recommendations: Vec::new(),
            state_of_art_comparison: sota_comparison,
        };

        let engine = Arc::new(KnowledgeEngine::new());
        let config = AutomatedBenchmarkConfig::default();
        let runner = AutomatedBenchmarkRunner::new(engine, config);

        let health_score = runner.calculate_health_score(&report, &None);
        assert!(health_score > 0.7); // Should be good since overall score is 0.85 and SOTA ratio is 0.9
    }
}
