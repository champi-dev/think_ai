use think_ai_webapp::server;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize logging
    env_logger::init();

    // Run the server
    server::run_server().await?;

    Ok(())
}
