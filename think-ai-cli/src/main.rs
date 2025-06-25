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