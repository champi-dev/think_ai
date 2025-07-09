use anyhow::Result;
use colored::*;
use std::io::{self, Write};
use think_ai_knowledge::{
    isolated_session::IsolatedSession,
    types::{ProcessState, ProcessType},
};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!(
        "{}",
        "🤖 Think AI Isolated Chat Interface".bright_blue().bold()
    );
    println!("{}", "Type 'exit' to quit\n".bright_black());

    // Create isolated session
    let mut session = IsolatedSession::new();

    // Initialize session
    println!("{}", "Initializing isolated session...".yellow());
    session.initialize().await?;
    println!("{}", "Session ready!\n".green());

    loop {
        // Print prompt
        print!("{}", "You: ".bright_cyan());
        io::stdout().flush()?;

        // Read input
        let mut input = String::new();
        io::stdin().read_line(&mut input)?;
        let input = input.trim();

        if input == "exit" {
            println!("{}", "\nGoodbye!".bright_magenta());
            break;
        }

        if input.is_empty() {
            continue;
        }

        // Process query
        print!("{}", "AI: ".bright_green());
        io::stdout().flush()?;

        match session.process_query(input).await {
            Ok(response) => {
                println!("{}\n", response);
            }
            Err(e) => {
                println!("Error: {}\n", e);
            }
        }
    }

    Ok(())
}
