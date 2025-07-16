// Example: Creating a custom response component

use think_ai_knowledge::response_generator::{ResponseComponent, ResponseContext};
use std::collections::HashMap;
/// Custom component for handling weather-related queries
pub struct WeatherComponent;
impl ResponseComponent for WeatherComponent {
    fn name(&self) -> &'static str {
        "Weather"
    }
    fn can_handle(&self, query: &str, _context: &ResponseContext) -> f32 {
        let query_lower = query.to_lowercase();
        let weather_terms = ["weather", "temperature", "rain", "snow", "sunny", "cloudy", "forecast", "climate"];
        if weather_terms.iter().any(|&term| query_lower.contains(term)) {
            0.9
        } else {
            0.0
        }
    fn generate(&self, query: &str, context: &ResponseContext) -> Option<String> {
        // Check knowledge base first
        for node in &context.relevant_nodes {
            if node.topic.to_lowercase().contains("weather") || node.topic.to_lowercase().contains("climate") {
                return Some(node.content.clone());
            }
        // Generate dynamic response based on query
        if query_lower.contains("how") && query_lower.contains("weather") {
            Some("Weather patterns are determined by complex interactions between atmospheric pressure, temperature, humidity, and wind. These factors are influenced by solar radiation, Earth's rotation, and geographic features. Modern weather prediction uses sophisticated models that analyze vast amounts of data from satellites, weather stations, and atmospheric sensors.".to_string())
        } else if query_lower.contains("climate") {
            Some("Climate represents long-term weather patterns in a region, typically averaged over 30 years or more. It's influenced by latitude, altitude, ocean currents, and atmospheric circulation. Climate change refers to significant, lasting changes in these patterns, often driven by human activities that increase greenhouse gas concentrations.".to_string())
            Some("Weather and climate are fascinating atmospheric phenomena that affect all life on Earth. Would you like to know about specific weather patterns, climate zones, or meteorological processes?".to_string())
    fn metadata(&self) -> HashMap<String, String> {
        let mut metadata = HashMap::new();
        metadata.insert("version".to_string(), "1.0".to_string());
        metadata.insert("author".to_string(), "Think AI Team".to_string());
        metadata.insert("description".to_string(), "Handles weather and climate queries".to_string());
        metadata
}
/// Custom component for code generation
pub struct CodeGeneratorComponent;
impl ResponseComponent for CodeGeneratorComponent {
        "CodeGenerator"
        if query_lower.contains("write") && (query_lower.contains("code") || query_lower.contains("function") || query_lower.contains("program")) {
            0.95
        } else if query_lower.contains("implement") || query_lower.contains("create") && query_lower.contains("algorithm") {
    fn generate(&self, query: &str, _context: &ResponseContext) -> Option<String> {
        if query_lower.contains("hello world") {
            Some("Here's a Hello World implementation:\n\n```rust\nfn main() {\n    println!(\"Hello, World!\");\n}\n```\n\nThis simple program demonstrates the basic structure of a Rust application with a main function that prints to stdout.".to_string())
        } else if query_lower.contains("fibonacci") {
            Some("Here's an O(log n) Fibonacci implementation using matrix exponentiation:\n\n```rust\nfn fibonacci(n: u64) -> u64 {\n    if n <= 1 { return n; }\n    let mut result = [[1, 1], [1, 0]];\n    let mut base = [[1, 1], [1, 0]];\n    let mut n = n - 1;\n    while n > 0 {\n        if n & 1 == 1 { result = matrix_multiply(&result, &base); }\n        base = matrix_multiply(&base, &base);\n        n >>= 1;\n    }\n    result[0][0]\n}\n```".to_string())
            Some("I can help you write efficient code. Please specify the algorithm or functionality you need, and I'll provide an optimized implementation following Think AI's performance standards.".to_string())
// Example usage:
fn main() {
    use think_ai_knowledge::{KnowledgeEngine, response_generator::ComponentResponseGenerator};
    use std::sync::Arc;
    // Create knowledge engine and response generator
    let engine = Arc::new(KnowledgeEngine::new());
    let mut generator = ComponentResponseGenerator::new(engine);
    // Add custom components
    generator.add_component(Box::new(WeatherComponent));
    generator.add_component(Box::new(CodeGeneratorComponent));
    // Test queries
    let queries = vec![
        "What is the weather like?",
        "How does climate change work?",
        "Write a hello world program",
        "Implement fibonacci sequence",
    ];
    for query in queries {
        println!("Q: {}", query);
        println!("A: {}\n", generator.generate_response(query));
