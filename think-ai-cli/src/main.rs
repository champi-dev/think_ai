//! Think AI CLI - Command line interface

pub mod commands;
pub mod ui;

use clap::Parser;

#[derive(Parser, Debug)]
#[command(name = "think-ai")]
#[command(about = "Think AI - O(1) AI System", long_about = None)]
struct Args {
    #[command(subcommand)]
    command: Option<commands::Commands>,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Load .env file if it exists
    if let Ok(path) = std::env::current_dir() {
        let env_path = path.join(".env");
        if env_path.exists() {
            // Simple .env loader
            if let Ok(contents) = std::fs::read_to_string(&env_path) {
                for line in contents.lines() {
                    if !line.trim().is_empty() && !line.trim().starts_with('#') {
                        if let Some((key, value)) = line.split_once('=') {
                            std::env::set_var(key.trim(), value.trim());
                        }
                    }
                }
            }
        }
    }
    
    // Initialize logging
    think_ai_utils::logging::init_tracing();
    
    let args = Args::parse();
    
    if let Some(cmd) = args.command {
        commands::execute(cmd).await?;
    } else {
        // Show interactive UI
        let mut terminal = ui::init_terminal()?;
        ui::draw_frame(&mut terminal)?;
        println!("\nThink AI v0.1.0 - Use --help for commands");
    }
    
    Ok(())
}