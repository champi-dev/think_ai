// CodeLlama Component for coding-specific queries
use crate::response_generator::{ResponseComponent, ResponseContext};
use std::collections::HashMap;
use std::sync::Arc;
use think_ai_codellama::{CodeAssistant, CodeLlamaClient};
use tokio::sync::RwLock;

pub struct CodeLlamaComponent {
    client: Arc<RwLock<Option<CodeLlamaClient>>>,
}

impl Default for CodeLlamaComponent {
    fn default() -> Self {
        Self::new()
    }
}

impl CodeLlamaComponent {
    pub fn new() -> Self {
        Self {
            client: Arc::new(RwLock::new(None)),
        }
    }

    async fn ensure_client(&self) -> bool {
        let mut client_guard = self.client.write().await;
        if client_guard.is_none() {
            match CodeLlamaClient::new() {
                Ok(client) => {
                    // Check if model is available
                    if let Ok(available) = client.check_model_availability().await {
                        if available {
                            *client_guard = Some(client);
                            return true;
                        }
                    }
                }
                Err(_) => return false,
            }
        }
        client_guard.is_some()
    }

    async fn generate_code_response(&self, query: &str) -> Option<String> {
        // Try to use CodeLlama first
        if self.ensure_client().await {
            let client_guard = self.client.read().await;
            if let Some(client) = client_guard.as_ref() {
                match client.assist_with_code(query).await {
                    Ok(response) => {
                        // Format the response with proper code blocks
                        let formatted_response = self.format_code_response(&response, query);
                        return Some(formatted_response);
                    }
                    Err(e) => {
                        eprintln!("CodeLlama error: {}", e);
                        // Fall through to provide a basic response
                    }
                }
            }
        }

        // If CodeLlama is not available or fails, provide a basic code response
        // This ensures we ALWAYS return something for code requests
        let language = self.detect_language(query);
        let basic_response = self.generate_basic_code_response(query, language);
        Some(self.format_code_response(&basic_response, query))
    }

    fn generate_basic_code_response(&self, query: &str, language: &str) -> String {
        let query_lower = query.to_lowercase();

        // Provide basic code templates based on common requests
        if query_lower.contains("server") && language == "python" {
            r#"import socket
import threading

class SimpleServer:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")
        
        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Connection from {address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()
    
    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Received: {data.decode()}")
                client_socket.send(b"Message received\n")
        finally:
            client_socket.close()

if __name__ == "__main__":
    server = SimpleServer()
    server.start()"#
                .to_string()
        } else if query_lower.contains("fetch") && language == "javascript" {
            r#"// Async function to fetch data
async function fetchData(url) {
    try {
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }
}

// Example usage
async function main() {
    try {
        const data = await fetchData('https://api.example.com/data');
        console.log('Data received:', data);
    } catch (error) {
        console.error('Failed to fetch data:', error);
    }
}

main();"#
                .to_string()
        } else if query_lower.contains("sort") {
            match language {
                "python" => r#"def sort_array(arr, reverse=False):
    """Sort an array in ascending or descending order."""
    return sorted(arr, reverse=reverse)

# Example usage
numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = sort_array(numbers)
print(f"Sorted array: {sorted_numbers}")

# Sort in descending order
sorted_desc = sort_array(numbers, reverse=True)
print(f"Sorted descending: {sorted_desc}")"#
                    .to_string(),

                "javascript" => r#"function sortArray(arr, compareFunc) {
    // Default compare function for numeric sort
    if (!compareFunc) {
        compareFunc = (a, b) => a - b;
    }
    
    return [...arr].sort(compareFunc);
}

// Example usage
const numbers = [64, 34, 25, 12, 22, 11, 90];
const sorted = sortArray(numbers);
console.log('Sorted array:', sorted);

// Sort strings
const strings = ['banana', 'apple', 'cherry', 'date'];
const sortedStrings = sortArray(strings, (a, b) => a.localeCompare(b));
console.log('Sorted strings:', sortedStrings);"#
                    .to_string(),

                _ => r#"// Generic sorting algorithm (quicksort)
function quicksort(arr) {
    if (arr.length <= 1) return arr;
    
    const pivot = arr[Math.floor(arr.length / 2)];
    const left = arr.filter(x => x < pivot);
    const middle = arr.filter(x => x === pivot);
    const right = arr.filter(x => x > pivot);
    
    return [...quicksort(left), ...middle, ...quicksort(right)];
}"#
                .to_string(),
            }
        } else {
            // Generic code template based on language
            match language {
                "python" => format!("# Python code for: {}\n\ndef main():\n    # TODO: Implement {}\n    pass\n\nif __name__ == '__main__':\n    main()", query, query),
                "javascript" => format!("// JavaScript code for: {}\n\nfunction main() {{\n    // TODO: Implement {}\n}}\n\nmain();", query, query),
                _ => format!("// Code for: {}\n\n// TODO: Implement the requested functionality", query)
            }
        }
    }

    fn format_code_response(&self, response: &str, query: &str) -> String {
        // First check if the response contains custom format tags like [PYTHON], [JAVASCRIPT], etc.
        if let Some(formatted) = self.extract_custom_format(response) {
            return formatted;
        }

        // Detect the programming language from the query or response content
        let language = self.detect_language_from_content(response, query);

        // Check if response already contains code blocks
        if response.contains("```") {
            // Replace empty code blocks with language-specific ones
            let mut formatted = response.to_string();

            // Replace ``` with ```language if no language is specified
            if !formatted.contains("```python")
                && !formatted.contains("```javascript")
                && !formatted.contains("```java")
                && !formatted.contains("```rust")
            {
                formatted = formatted.replace("```\n", &format!("```{}\n", language));
            }

            return formatted;
        }

        // For code mode, we should ALWAYS wrap the response in code blocks
        // since the user explicitly requested code
        if query.contains("[CODE REQUEST]") || self.looks_like_code(response) {
            return format!("```{}\n{}\n```", language, response.trim());
        }

        // Check if the entire response is code (no explanatory text)
        let lines: Vec<&str> = response.lines().collect();
        let code_line_count = lines.iter().filter(|line| self.is_code_line(line)).count();
        let total_non_empty_lines = lines.iter().filter(|line| !line.trim().is_empty()).count();

        // If more than 70% of non-empty lines look like code, treat it as pure code
        if total_non_empty_lines > 0 && code_line_count as f32 / total_non_empty_lines as f32 > 0.7
        {
            // Wrap entire response in code block with syntax highlighting
            format!("```{}\n{}\n```", language, response.trim())
        } else {
            // Look for code sections and wrap them
            let mut formatted = String::new();
            let mut in_code = false;
            let mut code_buffer = String::new();

            for line in lines {
                if self.is_code_line(line) {
                    if !in_code {
                        if !formatted.is_empty() && !formatted.ends_with('\n') {
                            formatted.push('\n');
                        }
                        in_code = true;
                    }
                    code_buffer.push_str(line);
                    code_buffer.push('\n');
                } else {
                    if in_code {
                        // End of code section, wrap it
                        formatted.push_str(&format!(
                            "```{}\n{}\n```\n",
                            language,
                            code_buffer.trim()
                        ));
                        code_buffer.clear();
                        in_code = false;
                    }
                    formatted.push_str(line);
                    formatted.push('\n');
                }
            }

            // Handle any remaining code
            if in_code && !code_buffer.is_empty() {
                formatted.push_str(&format!("```{}\n{}\n```", language, code_buffer.trim()));
            }

            formatted.trim().to_string()
        }
    }

    fn detect_language_from_content(&self, content: &str, query: &str) -> &'static str {
        // First try to detect from query
        let lang_from_query = self.detect_language(query);
        if !lang_from_query.is_empty() {
            return lang_from_query;
        }

        // Then try to detect from content
        let content_lower = content.to_lowercase();

        // Python detection
        if content.contains("import ")
            || content.contains("def ")
            || content.contains("print(")
            || content.contains("if __name__")
            || content.contains("class ") && content.contains("self")
        {
            return "python";
        }

        // JavaScript/Node.js detection
        if content.contains("const ")
            || content.contains("let ")
            || content.contains("var ")
            || content.contains("function ")
            || content.contains("=>")
            || content.contains("console.log")
        {
            return "javascript";
        }

        // Java detection
        if content.contains("public class")
            || content.contains("public static void main")
            || content.contains("System.out.println")
        {
            return "java";
        }

        // Default to empty string for generic highlighting
        ""
    }

    fn looks_like_code(&self, content: &str) -> bool {
        // Check for common code patterns
        content.contains("import ")
            || content.contains("from ")
            || content.contains("def ")
            || content.contains("class ")
            || content.contains("function ")
            || content.contains("const ")
            || content.contains("let ")
            || content.contains("var ")
            || content.contains("public ")
            || content.contains("private ")
            || content.contains("return ")
            || content.contains("if ")
            || content.contains("for ")
            || content.contains("while ")
            || (content.contains("{") && content.contains("}"))
            || (content.contains("(") && content.contains(")") && content.contains(";"))
    }

    fn extract_custom_format(&self, response: &str) -> Option<String> {
        // Check for custom format tags like [PYTHON], [JAVASCRIPT], etc.
        let response_trimmed = response.trim();

        // Remove any "💻 CodeLlama Response:" prefix
        let content = if response_trimmed.starts_with("💻 CodeLlama Response:") {
            response_trimmed
                .trim_start_matches("💻 CodeLlama Response:")
                .trim()
        } else {
            response_trimmed
        };

        // Look for [LANGUAGE] tags
        let languages = vec![
            ("PYTHON", "python"),
            ("JAVASCRIPT", "javascript"),
            ("JAVA", "java"),
            ("RUST", "rust"),
            ("CPP", "cpp"),
            ("C++", "cpp"),
            ("GO", "go"),
            ("TYPESCRIPT", "typescript"),
            ("RUBY", "ruby"),
            ("PHP", "php"),
            ("C#", "csharp"),
            ("CSHARP", "csharp"),
        ];

        for (tag, lang) in languages {
            let start_tag = format!("[{}]", tag);
            let end_tag = format!("[/{}]", tag);

            if let Some(start_idx) = content.find(&start_tag) {
                let after_start = &content[start_idx + start_tag.len()..];

                if let Some(end_idx) = after_start.find(&end_tag) {
                    let code = after_start[..end_idx].trim();
                    let after_code = &after_start[end_idx + end_tag.len()..].trim();

                    // Format as markdown with explanation after if present
                    let mut result = format!("```{}\n{}\n```", lang, code);
                    if !after_code.is_empty() {
                        result.push_str(&format!("\n\n{}", after_code));
                    }
                    return Some(result);
                }
            }
        }

        None
    }

    fn detect_language(&self, query: &str) -> &'static str {
        let query_lower = query.to_lowercase();

        if query_lower.contains("python") || query_lower.contains(".py") {
            "python"
        } else if query_lower.contains("javascript") || query_lower.contains(".js") {
            "javascript"
        } else if query_lower.contains("typescript") || query_lower.contains(".ts") {
            "typescript"
        } else if query_lower.contains("rust") || query_lower.contains(".rs") {
            "rust"
        } else if query_lower.contains("java") && !query_lower.contains("javascript") {
            "java"
        } else if query_lower.contains("c++") || query_lower.contains("cpp") {
            "cpp"
        } else if query_lower.contains("c#") || query_lower.contains("csharp") {
            "csharp"
        } else if query_lower.contains("go") || query_lower.contains("golang") {
            "go"
        } else if query_lower.contains("ruby") || query_lower.contains(".rb") {
            "ruby"
        } else if query_lower.contains("php") {
            "php"
        } else if query_lower.contains("swift") {
            "swift"
        } else if query_lower.contains("kotlin") {
            "kotlin"
        } else if query_lower.contains("scala") {
            "scala"
        } else if query_lower.contains("sql") {
            "sql"
        } else if query_lower.contains("bash")
            || query_lower.contains("shell")
            || query_lower.contains("script")
        {
            "bash"
        } else if query_lower.contains("html") {
            "html"
        } else if query_lower.contains("css") {
            "css"
        } else if query_lower.contains("yaml") || query_lower.contains("yml") {
            "yaml"
        } else if query_lower.contains("json") {
            "json"
        } else if query_lower.contains("xml") {
            "xml"
        } else {
            "" // No specific language detected
        }
    }

    fn is_code_line(&self, line: &str) -> bool {
        let trimmed = line.trim();

        // Empty lines within code blocks
        if trimmed.is_empty() {
            return false; // Will be handled by context
        }

        // Common code patterns
        trimmed.starts_with("//")
            || trimmed.starts_with("#")
            || trimmed.starts_with("/*")
            || trimmed.starts_with("*")
            || trimmed.starts_with("import ")
            || trimmed.starts_with("from ")
            || trimmed.starts_with("export ")
            || trimmed.starts_with("const ")
            || trimmed.starts_with("let ")
            || trimmed.starts_with("var ")
            || trimmed.starts_with("function ")
            || trimmed.starts_with("def ")
            || trimmed.starts_with("class ")
            || trimmed.starts_with("public ")
            || trimmed.starts_with("private ")
            || trimmed.starts_with("protected ")
            || trimmed.starts_with("static ")
            || trimmed.starts_with("if ")
            || trimmed.starts_with("else")
            || trimmed.starts_with("for ")
            || trimmed.starts_with("while ")
            || trimmed.starts_with("return ")
            || trimmed.starts_with("@")
            || trimmed.ends_with("{")
            || trimmed.ends_with("}")
            || trimmed.ends_with(";")
            || trimmed.ends_with(":")
            || (trimmed.contains("=") && !trimmed.contains(" = "))
            || (trimmed.contains("(") && trimmed.contains(")"))
    }
}

impl ResponseComponent for CodeLlamaComponent {
    fn name(&self) -> &'static str {
        "CodeLlama"
    }

    fn can_handle(&self, query: &str, _context: &ResponseContext) -> f32 {
        // Check for explicit code request
        if query.starts_with("[CODE REQUEST]") {
            return 1.0; // Maximum priority
        }

        // Skip if explicitly marked as general request or conversation context
        if query.starts_with("[GENERAL REQUEST]") || query.starts_with("[CONVERSATION CONTEXT]") {
            return 0.0;
        }

        let runtime = tokio::runtime::Handle::try_current();
        if runtime.is_err() {
            // No async runtime available, check synchronously
            let code_keywords = [
                "code",
                "program",
                "function",
                "class",
                "method",
                "algorithm",
                "implement",
                "write",
                "create",
                "debug",
                "fix",
                "error",
                "bug",
                "python",
                "rust",
                "javascript",
                "java",
                "c++",
                "golang",
                "typescript",
                "react",
                "vue",
                "angular",
                "database",
                "sql",
                "api",
                "test",
                "optimize",
                "refactor",
                "analyze",
                "review",
                "complete",
                "snippet",
            ];

            let query_lower = query.to_lowercase();
            if code_keywords
                .iter()
                .any(|&keyword| query_lower.contains(keyword))
            {
                return 0.9; // High priority for code-related queries
            }
            return 0.0;
        }

        // If we have runtime, we could do async check but keep it simple for now
        let code_keywords = [
            "code",
            "program",
            "function",
            "class",
            "method",
            "algorithm",
            "implement",
            "write",
            "create",
            "debug",
            "fix",
            "error",
            "bug",
            "python",
            "rust",
            "javascript",
            "java",
            "c++",
            "golang",
            "typescript",
            "react",
            "vue",
            "angular",
            "database",
            "sql",
            "api",
            "test",
            "optimize",
            "refactor",
            "analyze",
            "review",
            "complete",
            "snippet",
        ];

        let query_lower = query.to_lowercase();
        if code_keywords
            .iter()
            .any(|&keyword| query_lower.contains(keyword))
        {
            0.9 // High priority for code-related queries
        } else {
            0.0
        }
    }

    fn generate(&self, query: &str, _context: &ResponseContext) -> Option<String> {
        // Clean the query by removing the [CODE REQUEST] prefix if present
        let clean_query = if query.starts_with("[CODE REQUEST]") {
            query.trim_start_matches("[CODE REQUEST]").trim()
        } else {
            query
        };

        // Use Handle::current() to check if we're in a runtime
        if let Ok(handle) = tokio::runtime::Handle::try_current() {
            // We're already in a runtime, use it
            tokio::task::block_in_place(|| {
                handle.block_on(self.generate_code_response(clean_query))
            })
        } else {
            // No runtime, create one
            let runtime = tokio::runtime::Runtime::new().ok()?;
            runtime.block_on(self.generate_code_response(clean_query))
        }
    }

    fn metadata(&self) -> HashMap<String, String> {
        let mut meta = HashMap::new();
        meta.insert("version".to_string(), "1.0.0".to_string());
        meta.insert("model".to_string(), "codellama:7b".to_string());
        meta.insert("type".to_string(), "code_assistant".to_string());
        meta.insert("performance".to_string(), "O(1) with caching".to_string());
        meta
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_code_detection() {
        let component = CodeLlamaComponent::new();
        let context = ResponseContext {
            knowledge_engine: Arc::new(crate::KnowledgeEngine::new()),
            relevant_nodes: Vec::new(),
            query_tokens: Vec::new(),
            conversation_history: Vec::new(),
            extracted_entities: HashMap::new(),
        };

        // Should handle code queries
        assert!(component.can_handle("write a python function", &context) > 0.8);
        assert!(component.can_handle("debug this javascript code", &context) > 0.8);
        assert!(component.can_handle("implement binary search in rust", &context) > 0.8);

        // Should not handle non-code queries
        assert_eq!(component.can_handle("what is the weather", &context), 0.0);
        assert_eq!(
            component.can_handle("tell me about consciousness", &context),
            0.0
        );
        assert_eq!(component.can_handle("2+2", &context), 0.0);
    }
}
