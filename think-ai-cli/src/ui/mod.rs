//! Terminal UI components

use ratatui::{
    backend::CrosstermBackend,
    widgets::{Block, Borders, Paragraph},
    Terminal,
};
use std::io;

/// Initialize terminal UI
/// 
/// What it does: Sets up rich terminal interface
/// How: Uses ratatui for cross-platform terminal UI
/// Why: Provides better UX than plain text output
/// Confidence: 90% - Standard terminal UI setup
pub fn init_terminal() -> io::Result<Terminal<CrosstermBackend<io::Stdout>>> {
    let backend = CrosstermBackend::new(io::stdout());
    Terminal::new(backend)
}

/// Draw main UI frame
pub fn draw_frame(terminal: &mut Terminal<CrosstermBackend<io::Stdout>>) -> io::Result<()> {
    terminal.draw(|f| {
        let area = f.area();
        
        let block = Block::default()
            .title("Think AI - O(1) Performance")
            .borders(Borders::ALL);
            
        let paragraph = Paragraph::new("Ready for input...")
            .block(block);
            
        f.render_widget(paragraph, area);
    })?;
    
    Ok(())
}