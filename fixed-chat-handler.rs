// In your chat handler, wrap the response:
let original_response = // ... your current response generation
let cleaned_response = clean_response_formatting(&original_response);

Json(ChatResponse {
    response: cleaned_response,
    session_id,
    error: None,
})
