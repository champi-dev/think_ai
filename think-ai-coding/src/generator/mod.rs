//! Code generation engine

use crate::templates::{CodeTemplates, Template};
use std::collections::HashMap;

/// Generate code from template and parameters
/// 
/// What it does: Generates code by filling templates
/// How: Simple string replacement with O(1) lookups
/// Why: Provides consistent code generation
/// Confidence: 95% - Well-tested pattern
pub fn generate_from_template(
    template: &Template,
    params: HashMap<String, String>,
) -> Result<String, String> {
    let mut code = template.pattern.clone();
    
    // Validate all placeholders have values
    for placeholder in &template.placeholders {
        if !params.contains_key(placeholder) {
            return Err(format!("Missing parameter: {}", placeholder));
        }
    }
    
    // Replace placeholders
    for (key, value) in params {
        let placeholder = format!("{{{}}}", key);
        code = code.replace(&placeholder, &value);
    }
    
    Ok(code)
}

/// Generate a complete function
pub fn generate_function(
    language: &str,
    name: &str,
    params: &str,
    return_type: &str,
    body: &str,
    doc: &str,
) -> Result<String, String> {
    let templates = CodeTemplates::new();
    let template_key = format!("{}_function", language);
    
    let template = templates.get(&template_key)
        .ok_or_else(|| format!("No template for language: {}", language))?;
    
    let mut params_map = HashMap::new();
    params_map.insert("name".to_string(), name.to_string());
    params_map.insert("params".to_string(), params.to_string());
    params_map.insert("return_type".to_string(), return_type.to_string());
    params_map.insert("body".to_string(), body.to_string());
    params_map.insert("doc".to_string(), doc.to_string());
    
    generate_from_template(template, params_map)
}