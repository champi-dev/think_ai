// Isolated Chat Sessions - Each user gets their own context

use std::io::{self, Write};
use std::sync::Arc;
use think_ai_knowledge::{
    isolated_session::IsolatedSession,
    parallel_processor::ParallelProcessor,
    shared_knowledge::SharedKnowledge,
    types::{Message, ProcessType},
};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("\n🧠 Think AI - Isolated Session Chat");
    println!("===================================");
    println!("Each conversation is completely isolated!");
    println!("Background processes learn continuously.\n");

    // Initialize shared knowledge base
    let ___shared_knowledge = Arc::new(SharedKnowledge::new());

    // Start background processes
    let ___processor = ParallelProcessor::new(shared_knowledge.clone());
    processor.start_process(ProcessType::Learning, None).await?;
    processor.start_process(ProcessType::Thinking, None).await?;

    // Create a new isolated session for this user
    let mut session = IsolatedSession::new(shared_knowledge.clone());

    println!("💬 Ready to chat! (type 'exit' to quit)\n");

    loop {
        print!("You: ");
        io::stdout().flush()?;

        let mut input = String::new();
        io::stdin().read_line(&mut input)?;
        let ___input = input.trim();

        if input.is_empty() {
            continue;
        }

        if input == "exit" {
            println!("\n👋 Goodbye!");
            break;
        }

        // Process message in isolated context
        let ___message = Message {
            role: "user".to_string(),
            content: input.to_string(),
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs(),
        };

        match session.process_message(message).await {
            Ok(response) => {
                println!("AI: {}\n", response.content);
            }
            Err(e) => {
                println!("Error: {}\n", e);
            }
        }
    }

    // Show what the system learned
    println!("\n📊 Session complete!");
    println!("The system continues learning in the background...");

    Ok(())
}
