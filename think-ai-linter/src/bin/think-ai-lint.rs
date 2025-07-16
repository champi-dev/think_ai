// Think AI O(1) Linter CLI

use clap::Parser;
use colored::*;
use indicatif::{ProgressBar, ProgressStyle};
use std::path::PathBuf;
use think_ai_linter::{
    analyzer::FileAnalyzer,
    fixer::CodeFixer,
    rules::Severity,
};
use walkdir::WalkDir;
#[derive(Parser)]
#[command(name = "think-ai-lint")]
#[command(about = "O(1) performance linter for Rust", long_about = None)]
struct Cli {
    /// Path to analyze
    path: PathBuf,
    /// Fix violations automatically
    #[arg(short, long)]
    fix: bool,
    /// File extensions to analyze
    #[arg(short, long, default_value = "rs")]
    extensions: Vec<String>,
}
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let cli = Cli::parse();
    println!("{}", "🚀 Think AI O(1) Linter".bold().cyan());
    println!("{}", "Analyzing for O(1) performance...".dimmed());
    let analyzer = FileAnalyzer::new();
    let fixer = CodeFixer::new();
    // Count files
    let total_files: usize = WalkDir::new(&cli.path)
        .into_iter()
        .filter_map(Result::ok)
        .filter(|e| e.file_type().is_file())
        .filter(|e| {
            cli.extensions.iter().any(|ext| {
                e.path()
                    .extension()
                    .map(|e| e == ext.as_str())
                    .unwrap_or(false)
            })
        })
        .count();
    let pb = ProgressBar::new(total_files as u64);
    pb.set_style(
        ProgressStyle::default_bar()
            .template("{spinner:.green} [{bar:40.cyan/blue}] {pos}/{len} {msg}")
            .unwrap()
    );
    let mut total_violations = 0;
    let mut files_with_issues = 0;
    // Analyze files
    for entry in WalkDir::new(&cli.path)
    {
        let path = entry.path();
        // Check extension
        let has_valid_ext = cli.extensions.iter().any(|ext| {
            path.extension()
                .map(|e| e == ext.as_str())
                .unwrap_or(false)
        });
        if !has_valid_ext {
            continue;
        }
        pb.set_message(format!("Analyzing {}", path.display()));
        match analyzer.analyze_file(path) {
            Ok(violations) => {
                if !violations.is_empty() {
                    files_with_issues += 1;
                    total_violations += violations.len();
                    println!("\n{}: {}", "File".bold(), path.display());
                    for violation in &violations {
                        let icon = match violation.severity {
                            Severity::Error => "❌".red(),
                            Severity::Warning => "⚠️ ".yellow(),
                            Severity::Info => "ℹ️ ".blue(),
                        };
                        println!(
                            "  {} [{}:{}] {}",
                            icon,
                            violation.rule.dimmed(),
                            violation.line,
                            violation.message
                        );
                    }
                    if cli.fix {
                        // Apply fixes
                        if let Ok(content) = std::fs::read_to_string(path) {
                            match fixer.fix_violations(&content, &violations) {
                                Ok(fixed) => {
                                    std::fs::write(path, fixed)?;
                                    println!("  {} Fixed violations", "✅".green());
                                }
                                Err(e) => {
                                    println!("  {} Failed to fix: {}", "❌".red(), e);
                            }
                        }
                }
            }
            Err(e) => {
                println!("\n{} {}: {}", "❌".red(), path.display(), e);
        pb.inc(1);
    }
    pb.finish_and_clear();
    // Summary
    println!("\n{}", "Summary".bold().underline());
    println!(
        "Files analyzed: {}",
        total_files.to_string().cyan()
        "Files with issues: {}",
        files_with_issues.to_string().yellow()
        "Total violations: {}",
        total_violations.to_string().red()
    if total_violations > 0 && !cli.fix {
        println!(
            "\n{} Run with {} to automatically fix violations",
            "Tip:".dimmed(),
            "--fix".bold()
        );
    Ok(())
