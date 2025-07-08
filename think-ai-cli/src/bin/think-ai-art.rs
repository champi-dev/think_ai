//! Think AI Art - Open Source Image Generation with AI Learning

use anyhow::Result;
use clap::{Parser, Subcommand};
use think_ai_image_gen::{AIImageImprover, UserFeedback};
use std::path::PathBuf;
use tokio::fs;

#[derive(Parser)]
#[command(name = "think-ai-art")]
#[command(about = "AI-powered image generation with continuous learning", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Generate an image with AI improvements
    Generate {
        /// The prompt describing what to generate
        prompt: String,
        
        /// Output file path
        #[arg(short, long, default_value = "output.png")]
        output: PathBuf,
        
        /// Image width
        #[arg(short, long, default_value = "512")]
        width: u32,
        
        /// Image height
        #[arg(short, long, default_value = "512")]
        height: u32,
        
        /// Use Hugging Face API token (optional)
        #[arg(long, env = "HUGGINGFACE_TOKEN")]
        api_token: Option<String>,
    },
    
    /// Provide feedback on a generated image
    Feedback {
        /// The prompt that was used
        prompt: String,
        
        /// Feedback rating (excellent, good, average, poor)
        rating: String,
        
        /// Optional suggestions for improvement
        #[arg(short, long)]
        suggestions: Vec<String>,
    },
    
    /// Show AI learning statistics
    Stats,
    
    /// Interactive mode for generating and improving
    Interactive {
        /// Use Hugging Face API token (optional)
        #[arg(long, env = "HUGGINGFACE_TOKEN")]
        api_token: Option<String>,
    },
    
    /// Train the AI with batch feedback
    Train {
        /// Directory containing images and feedback
        #[arg(short, long)]
        data_dir: PathBuf,
    },
}

#[tokio::main]
async fn main() -> Result<()> {
    // Initialize logging
    tracing_subscriber::fmt::init();
    
    let cli = Cli::parse();
    
    // Default cache directory
    let cache_dir = PathBuf::from("./ai_art_cache");
    fs::create_dir_all(&cache_dir).await?;
    
    match cli.command {
        Commands::Generate { prompt, output, width, height, api_token } => {
            println!("🎨 Think AI Art - Generating with AI improvements...");
            
            let improver = AIImageImprover::new(&cache_dir, api_token).await?;
            
            let (image_data, enhanced_prompt) = improver.generate_improved(
                &prompt,
                Some(width),
                Some(height),
            ).await?;
            
            // Save the image
            fs::write(&output, &image_data).await?;
            
            println!("✅ Image saved to: {}", output.display());
            println!("🤖 AI-enhanced prompt: {}", enhanced_prompt);
            println!("\n💡 To improve results, provide feedback:");
            println!("   think-ai-art feedback \"{}\" <rating> -s \"suggestion\"", prompt);
            
            // Show stats
            let stats = improver.get_ai_stats().await;
            println!("\n📊 AI Learning Progress:");
            println!("   Total generations: {}", stats.total_generations);
            println!("   Success rate: {:.1}%", stats.success_rate * 100.0);
            if stats.improvement_rate > 0.0 {
                println!("   Improvement trend: +{:.1}%", stats.improvement_rate * 100.0);
            }
        }
        
        Commands::Feedback { prompt, rating, suggestions } => {
            let feedback = match rating.to_lowercase().as_str() {
                "excellent" => UserFeedback::Excellent,
                "good" => UserFeedback::Good,
                "average" => UserFeedback::Average,
                "poor" => UserFeedback::Poor,
                _ => {
                    eprintln!("❌ Invalid rating. Use: excellent, good, average, or poor");
                    return Ok(());
                }
            };
            
            let improver = AIImageImprover::new(&cache_dir, None).await?;
            improver.provide_feedback(
                &prompt,
                feedback,
                if suggestions.is_empty() { None } else { Some(suggestions) },
            ).await?;
            
            println!("✅ Feedback recorded! The AI will learn from this.");
            
            let stats = improver.get_ai_stats().await;
            println!("\n📈 Current AI Performance:");
            println!("   Success rate: {:.1}%", stats.success_rate * 100.0);
            println!("   Total feedback: {}", stats.feedback_count);
        }
        
        Commands::Stats => {
            let improver = AIImageImprover::new(&cache_dir, None).await?;
            let stats = improver.get_ai_stats().await;
            
            println!("🤖 Think AI Art - Learning Statistics");
            println!("=====================================");
            println!("Total generations: {}", stats.total_generations);
            println!("Success rate: {:.1}%", stats.success_rate * 100.0);
            println!("Improvement rate: {:+.1}%", stats.improvement_rate * 100.0);
            println!("Excellent generations: {}", stats.excellent_generations);
            println!("Total feedback received: {}", stats.feedback_count);
            println!("\n📚 Learned Patterns: {}", stats.learned_patterns);
            println!("🎨 Active Styles: {}", stats.active_styles);
            
            if !stats.top_strategies.is_empty() {
                println!("\n🏆 Top Enhancement Strategies:");
                for (strategy, rate) in stats.top_strategies.iter().take(5) {
                    println!("   - {}: {:.1}% success", strategy, rate * 100.0);
                }
            }
        }
        
        Commands::Interactive { api_token } => {
            interactive_mode(&cache_dir, api_token).await?;
        }
        
        Commands::Train { data_dir } => {
            println!("🎓 Training mode not yet implemented");
            println!("   This will allow batch training from a directory of images with feedback");
        }
    }
    
    Ok(())
}

async fn interactive_mode(cache_dir: &PathBuf, api_token: Option<String>) -> Result<()> {
    use std::io::{self, Write};
    
    println!("🎨 Think AI Art - Interactive Mode");
    println!("==================================");
    println!("Commands:");
    println!("  generate <prompt> - Generate an image");
    println!("  feedback <rating> - Rate the last image");
    println!("  stats - Show AI learning stats");
    println!("  help - Show this help");
    println!("  quit - Exit\n");
    
    let improver = AIImageImprover::new(cache_dir, api_token).await?;
    let mut last_prompt = String::new();
    let mut generation_count = 0;
    
    loop {
        print!("> ");
        io::stdout().flush()?;
        
        let mut input = String::new();
        io::stdin().read_line(&mut input)?;
        let input = input.trim();
        
        let parts: Vec<&str> = input.split_whitespace().collect();
        if parts.is_empty() {
            continue;
        }
        
        match parts[0] {
            "generate" | "g" => {
                if parts.len() < 2 {
                    println!("Usage: generate <prompt>");
                    continue;
                }
                
                let prompt = parts[1..].join(" ");
                last_prompt = prompt.clone();
                generation_count += 1;
                
                println!("🎨 Generating...");
                match improver.generate_improved(&prompt, Some(512), Some(512)).await {
                    Ok((image_data, enhanced)) => {
                        let filename = format!("interactive_{:03}.png", generation_count);
                        fs::write(&filename, &image_data).await?;
                        
                        println!("✅ Saved to: {}", filename);
                        println!("🤖 Enhanced: {}", enhanced);
                        println!("💡 Rate this image with: feedback <excellent|good|average|poor>");
                    }
                    Err(e) => {
                        println!("❌ Generation failed: {}", e);
                    }
                }
            }
            
            "feedback" | "f" => {
                if parts.len() < 2 {
                    println!("Usage: feedback <excellent|good|average|poor>");
                    continue;
                }
                
                if last_prompt.is_empty() {
                    println!("❌ No image to rate. Generate one first!");
                    continue;
                }
                
                let feedback = match parts[1] {
                    "excellent" => UserFeedback::Excellent,
                    "good" => UserFeedback::Good,
                    "average" => UserFeedback::Average,
                    "poor" => UserFeedback::Poor,
                    _ => {
                        println!("❌ Invalid rating. Use: excellent, good, average, or poor");
                        continue;
                    }
                };
                
                improver.provide_feedback(&last_prompt, feedback, None).await?;
                println!("✅ Thanks! The AI is learning from your feedback.");
            }
            
            "stats" | "s" => {
                let stats = improver.get_ai_stats().await;
                println!("\n📊 AI Performance:");
                println!("   Generations: {}", stats.total_generations);
                println!("   Success rate: {:.1}%", stats.success_rate * 100.0);
                println!("   Improvement: {:+.1}%", stats.improvement_rate * 100.0);
                println!("   Feedback given: {}", stats.feedback_count);
            }
            
            "help" | "h" => {
                println!("\nCommands:");
                println!("  generate <prompt> - Generate an image");
                println!("  feedback <rating> - Rate the last image");
                println!("  stats - Show AI learning stats");
                println!("  quit - Exit");
            }
            
            "quit" | "q" | "exit" => {
                println!("👋 Thanks for helping the AI learn!");
                break;
            }
            
            _ => {
                println!("❓ Unknown command. Type 'help' for available commands.");
            }
        }
    }
    
    Ok(())
}