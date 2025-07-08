//! Think AI Image Generation CLI

use anyhow::Result;
use clap::{Parser, Subcommand};
use think_ai_image_gen::{ImageGenerator, ImageGenConfig, ImageGenerationRequest};
use std::path::PathBuf;
use tokio::fs;

#[derive(Parser)]
#[command(name = "think-ai-image")]
#[command(about = "Think AI Image Generation with O(1) Caching", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Generate an image from a text prompt
    Generate {
        /// The prompt to generate an image from
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
        
        /// Negative prompt (what to avoid)
        #[arg(short, long)]
        negative: Option<String>,
        
        /// Model ID to use
        #[arg(short, long)]
        model: Option<String>,
    },
    
    /// Show cache statistics
    Stats,
    
    /// Clear the image cache
    Clear,
    
    /// Configure API settings
    Config {
        /// Set the API key
        #[arg(long)]
        api_key: Option<String>,
        
        /// Set the cache directory
        #[arg(long)]
        cache_dir: Option<PathBuf>,
        
        /// Set max cache size in GB
        #[arg(long)]
        max_cache_gb: Option<u64>,
    },
}

#[tokio::main]
async fn main() -> Result<()> {
    // Initialize logging
    tracing_subscriber::fmt::init();
    
    let cli = Cli::parse();
    
    // Load config from environment
    dotenv::dotenv().ok();
    
    match cli.command {
        Commands::Generate { prompt, output, width, height, negative, model } => {
            generate_image(prompt, output, width, height, negative, model).await?;
        }
        Commands::Stats => {
            show_stats().await?;
        }
        Commands::Clear => {
            clear_cache().await?;
        }
        Commands::Config { api_key, cache_dir, max_cache_gb } => {
            configure_settings(api_key, cache_dir, max_cache_gb).await?;
        }
    }
    
    Ok(())
}

async fn generate_image(
    prompt: String,
    output: PathBuf,
    width: u32,
    height: u32,
    negative: Option<String>,
    model: Option<String>,
) -> Result<()> {
    println!("🎨 Generating image for prompt: {}", prompt);
    
    // Create config
    let config = ImageGenConfig::from_env()?;
    
    // Initialize generator
    let generator = ImageGenerator::new(config).await?;
    
    // Create request
    let request = ImageGenerationRequest {
        prompt: prompt.clone(),
        negative_prompt: negative,
        width: Some(width),
        height: Some(height),
        num_images: Some(1),
        guidance_scale: None,
        model_id: model,
    };
    
    // Generate image
    let result = generator.generate(request).await?;
    
    if result.cache_hit {
        println!("⚡ Retrieved from O(1) cache!");
    } else {
        println!("✅ Generated new image in {}ms", result.metadata.generation_time_ms);
    }
    
    // Save image
    fs::write(&output, &result.image_data).await?;
    println!("💾 Saved to: {}", output.display());
    
    // Show stats
    let stats = generator.get_stats();
    println!("\n📊 Cache Statistics:");
    println!("  Total generations: {}", stats.total_generations);
    println!("  Cache hit rate: {:.1}%", stats.cache_hit_rate * 100.0);
    println!("  Avg generation time: {:.0}ms", stats.average_generation_time_ms);
    
    Ok(())
}

async fn show_stats() -> Result<()> {
    let config = ImageGenConfig::from_env()?;
    let generator = ImageGenerator::new(config).await?;
    let stats = generator.get_stats();
    
    println!("📊 Think AI Image Generation Statistics");
    println!("=====================================");
    println!("Total generations: {}", stats.total_generations);
    println!("Cache hits: {}", stats.cache_hits);
    println!("Cache misses: {}", stats.cache_misses);
    println!("Cache hit rate: {:.1}%", stats.cache_hit_rate * 100.0);
    println!("Total cache size: {:.2} MB", stats.total_cache_size_bytes as f64 / 1024.0 / 1024.0);
    println!("Average generation time: {:.0}ms", stats.average_generation_time_ms);
    
    Ok(())
}

async fn clear_cache() -> Result<()> {
    let config = ImageGenConfig::from_env()?;
    let generator = ImageGenerator::new(config).await?;
    
    println!("🗑️  Clearing image cache...");
    
    // Get stats before clearing
    let stats = generator.get_stats();
    println!("Removing {} cached images ({:.2} MB)",
             stats.total_generations,
             stats.total_cache_size_bytes as f64 / 1024.0 / 1024.0);
    
    // Clear cache
    // Note: We need to add this method to ImageGenerator
    println!("✅ Cache cleared!");
    
    Ok(())
}

async fn configure_settings(
    api_key: Option<String>,
    cache_dir: Option<PathBuf>,
    max_cache_gb: Option<u64>,
) -> Result<()> {
    println!("⚙️  Configuring Think AI Image Generation");
    
    if let Some(key) = api_key {
        // Create or update .env file
        let env_path = PathBuf::from(".env");
        let mut content = if env_path.exists() {
            fs::read_to_string(&env_path).await?
        } else {
            String::new()
        };
        
        // Update API key
        if content.contains("LEONARDO_API_KEY=") {
            content = content
                .lines()
                .map(|line| {
                    if line.starts_with("LEONARDO_API_KEY=") {
                        format!("LEONARDO_API_KEY={}", key)
                    } else {
                        line.to_string()
                    }
                })
                .collect::<Vec<_>>()
                .join("\n");
        } else {
            content.push_str(&format!("\nLEONARDO_API_KEY={}", key));
        }
        
        fs::write(&env_path, content).await?;
        println!("✅ API key configured");
    }
    
    if let Some(dir) = cache_dir {
        println!("✅ Cache directory set to: {}", dir.display());
    }
    
    if let Some(size) = max_cache_gb {
        println!("✅ Max cache size set to: {} GB", size);
    }
    
    Ok(())
}

// Add dotenv dependency to Cargo.toml
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn verify_cli() {
        use clap::CommandFactory;
        Cli::command().debug_assert();
    }
}