// In your chat handler or response generator, add:
use think_ai_knowledge::response_cleaner::clean_response_text;

// Then wrap your response:
let raw_response = // ... existing response generation
let cleaned_response = clean_response_text(&raw_response);
