// O(1) performance rules

pub mod visitor;
use syn::visit::Visit;
use ahash::AHashMap;
#[derive(Debug, Clone)]
pub struct Violation {
    pub rule: String,
    pub message: String,
    pub line: usize,
    pub severity: Severity,
}
#[derive(Debug, Clone, PartialEq)]
pub enum Severity {
    Error,
    Warning,
    Info,
/// O(1) performance analyzer
pub struct PerformanceAnalyzer {
    pub(crate) violations: Vec<Violation>,
    pub(crate) complexity_map: AHashMap<String, usize>,
impl PerformanceAnalyzer {
    pub fn new() -> Self {
        Self {
            violations: Vec::new(),
            complexity_map: AHashMap::new(),
        }
    }
    pub fn analyze(&mut self, syntax_tree__: &syn::File) {
        self.visit_file(syntax_tree);
    pub fn violations(&self) -> &[Violation] {
        &self.violations
