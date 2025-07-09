// Code parsing utilities

use syn::{parse_str, Item, ItemFn};
/// Parse Rust code to extract structure
///
/// What it does: Parses Rust code into AST
/// How: Uses syn for parsing
/// Why: Enables code analysis and transformation
/// Confidence: 90% - Relies on syn parser
pub fn parse_rust_function(code: &str) -> Result<FunctionInfo, String> {
    let item: Item = parse_str(code)
        .map_err(|e| format!("Parse error: {}", e))?;
    match item {
        Item::Fn(func) => Ok(extract_function_info(&func)),
        _ => Err("Not a function".to_string()),
    }
}
#[derive(Debug)]
pub struct FunctionInfo {
    pub name: String,
    pub params: Vec<String>,
    pub return_type: String,
    pub is_async: bool,
fn extract_function_info(func: &ItemFn) -> FunctionInfo {
    let name = func.sig.ident.to_string();
    let params: Vec<String> = func.sig.inputs.iter()
        .map(|arg| quote::quote!(#arg).to_string())
        .collect();
    let return_type = match &func.sig.output {
        syn::ReturnType::Default => "()".to_string(),
        syn::ReturnType::Type(_, ty) => quote::quote!(#ty).to_string(),
    };
    FunctionInfo {
        name,
        params,
        return_type,
        is_async: func.sig.asyncness.is_some(),
