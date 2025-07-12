use think_ai_webapp::server::run_server;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Starting Think AI Webapp...");
    run_server().await?;
    Ok(())
}
