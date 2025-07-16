// Code templates for generation

use std::collections::HashMap;
/// Language-specific code templates
///
/// What it does: Provides code templates for generation
/// How: HashMap lookup with O(1) access
/// Why: Enables consistent code generation patterns
/// Confidence: 100% - Simple template storage
pub struct CodeTemplates {
    templates: HashMap<String, Template>,
}
#[derive(Clone)]
pub struct Template {
    pub language: String,
    pub pattern: String,
    pub placeholders: Vec<String>,
impl CodeTemplates {
    pub fn new() -> Self {
        let mut templates = HashMap::new();
        // Rust function template
        templates.insert("rust_function".to_string(), Template {
            language: "rust".to_string(),
            pattern: r#"/// {doc}
pub fn {name}({params}) -> {return_type} {
    {body}
}"#.to_string(),
            placeholders: vec![
                "doc".to_string(),
                "name".to_string(),
                "params".to_string(),
                "return_type".to_string(),
                "body".to_string(),
            ],
        });
        // Python function template
        templates.insert("python_function".to_string(), Template {
            language: "python".to_string(),
            pattern: r#"def {name}({params}) -> {return_type}:
    """{doc}"""
    {body}"#.to_string(),
        // JavaScript function template
        templates.insert("javascript_function".to_string(), Template {
            language: "javascript".to_string(),
            pattern: r#"/**
 * {doc}
 */
function {name}({params}) {
        Self { templates }
    }
    pub fn get(&self, key: &str) -> Option<&Template> {
        self.templates.get(key)
