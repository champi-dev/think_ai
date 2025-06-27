//! Dynamic Knowledge Loader - Loads knowledge from files at runtime

use crate::{KnowledgeDomain, KnowledgeEngine};
use std::fs;
use std::path::{Path, PathBuf};
use std::collections::HashMap;
use serde::{Deserialize, Serialize};
use std::sync::Arc;

#[derive(Debug, Serialize, Deserialize)]
pub struct KnowledgeFile {
    pub domain: String,
    pub entries: Vec<KnowledgeEntry>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct KnowledgeEntry {
    pub topic: String,
    pub content: String,
    pub related_concepts: Vec<String>,
    pub metadata: Option<KnowledgeMetadata>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct KnowledgeMetadata {
    pub conversational_patterns: Option<Vec<String>>,
    pub evaluation_score: Option<f64>,
    #[serde(flatten)]
    pub additional_fields: HashMap<String, serde_json::Value>,
}

pub struct DynamicKnowledgeLoader {
    knowledge_dir: PathBuf,
}

impl DynamicKnowledgeLoader {
    pub fn new<P: AsRef<Path>>(knowledge_dir: P) -> Self {
        Self {
            knowledge_dir: knowledge_dir.as_ref().to_path_buf(),
        }
    }
    
    /// Load all knowledge files from the directory
    pub fn load_all(&self, engine: &Arc<KnowledgeEngine>) -> Result<usize, Box<dyn std::error::Error>> {
        let mut total_loaded = 0;
        
        // Create directory if it doesn't exist
        if !self.knowledge_dir.exists() {
            fs::create_dir_all(&self.knowledge_dir)?;
        }

        // Create default files if the directory is empty
        if self.knowledge_dir.read_dir()?.next().is_none() {
            self.create_default_knowledge_files()?;
        }
        
        // Read all JSON files from the knowledge directory
        for entry in fs::read_dir(&self.knowledge_dir)? {
            let entry = entry?;
            let path = entry.path();
            
            if path.extension().and_then(|s| s.to_str()) == Some("json") {
                match self.load_file(&path, engine) {
                    Ok(count) => {
                        total_loaded += count;
                        println!("📚 Loaded {} entries from {:?}", count, path.file_name().unwrap());
                    }
                    Err(e) => {
                        eprintln!("⚠️  Failed to load {:?}: {}", path.file_name().unwrap(), e);
                    }
                }
            }
        }
        
        // Also try loading from YAML files
        for entry in fs::read_dir(&self.knowledge_dir)? {
            let entry = entry?;
            let path = entry.path();
            
            if path.extension().and_then(|s| s.to_str()) == Some("yaml") || 
               path.extension().and_then(|s| s.to_str()) == Some("yml") {
                match self.load_yaml_file(&path, engine) {
                    Ok(count) => {
                        total_loaded += count;
                        println!("📚 Loaded {} entries from {:?}", count, path.file_name().unwrap());
                    }
                    Err(e) => {
                        eprintln!("⚠️  Failed to load {:?}: {}", path.file_name().unwrap(), e);
                    }
                }
            }
        }
        
        Ok(total_loaded)
    }
    
    /// Load a single JSON knowledge file
    fn load_file(&self, path: &Path, engine: &Arc<KnowledgeEngine>) -> Result<usize, Box<dyn std::error::Error>> {
        let content = fs::read_to_string(path)?;
        let knowledge_file: KnowledgeFile = serde_json::from_str(&content)?;
        
        let domain = self.parse_domain(&knowledge_file.domain)?;
        let mut count = 0;
        
        for entry in knowledge_file.entries {
            engine.add_knowledge(
                domain.clone(),
                entry.topic,
                entry.content,
                entry.related_concepts,
            );
            count += 1;
        }
        
        Ok(count)
    }
    
    /// Load a YAML knowledge file
    fn load_yaml_file(&self, path: &Path, engine: &Arc<KnowledgeEngine>) -> Result<usize, Box<dyn std::error::Error>> {
        let content = fs::read_to_string(path)?;
        let knowledge_file: KnowledgeFile = serde_yaml::from_str(&content)?;
        
        let domain = self.parse_domain(&knowledge_file.domain)?;
        let mut count = 0;
        
        for entry in knowledge_file.entries {
            engine.add_knowledge(
                domain.clone(),
                entry.topic,
                entry.content,
                entry.related_concepts,
            );
            count += 1;
        }
        
        Ok(count)
    }
    
    /// Parse domain string to KnowledgeDomain enum
    fn parse_domain(&self, domain_str: &str) -> Result<KnowledgeDomain, String> {
        match domain_str.to_lowercase().as_str() {
            "mathematics" | "math" => Ok(KnowledgeDomain::Mathematics),
            "physics" => Ok(KnowledgeDomain::Physics),
            "chemistry" | "chem" => Ok(KnowledgeDomain::Chemistry),
            "biology" | "bio" => Ok(KnowledgeDomain::Biology),
            "computerscience" | "computer_science" | "cs" => Ok(KnowledgeDomain::ComputerScience),
            "engineering" | "eng" => Ok(KnowledgeDomain::Engineering),
            "medicine" | "med" => Ok(KnowledgeDomain::Medicine),
            "psychology" | "psych" => Ok(KnowledgeDomain::Psychology),
            "sociology" | "soc" => Ok(KnowledgeDomain::Sociology),
            "economics" | "econ" => Ok(KnowledgeDomain::Economics),
            "philosophy" | "phil" => Ok(KnowledgeDomain::Philosophy),
            "ethics" => Ok(KnowledgeDomain::Ethics),
            "art" => Ok(KnowledgeDomain::Art),
            "music" => Ok(KnowledgeDomain::Music),
            "literature" | "lit" => Ok(KnowledgeDomain::Literature),
            "history" | "hist" => Ok(KnowledgeDomain::History),
            "geography" | "geo" => Ok(KnowledgeDomain::Geography),
            "linguistics" | "ling" => Ok(KnowledgeDomain::Linguistics),
            "logic" => Ok(KnowledgeDomain::Logic),
            "astronomy" | "astro" => Ok(KnowledgeDomain::Astronomy),
            _ => Err(format!("Unknown domain: {}", domain_str)),
        }
    }
    
    /// Create default knowledge files if none exist
    fn create_default_knowledge_files(&self) -> Result<(), Box<dyn std::error::Error>> {
        // Create a sample astronomy knowledge file
        let astronomy_knowledge = KnowledgeFile {
            domain: "astronomy".to_string(),
            entries: vec![
                KnowledgeEntry {
                    topic: "Andromeda Galaxy".to_string(),
                    content: "The Andromeda Galaxy (M31) is the nearest major galaxy to the Milky Way and is on a collision course with our galaxy. Located 2.5 million light-years away, it contains roughly one trillion stars. The collision will occur in about 4.5 billion years, eventually forming a giant elliptical galaxy. Andromeda is visible to the naked eye from Earth and has been known since ancient times.".to_string(),
                    related_concepts: vec!["galaxy".to_string(), "Milky Way".to_string(), "M31".to_string(), "Local Group".to_string()],
                    metadata: None,
                },
                KnowledgeEntry {
                    topic: "Black Hole".to_string(),
                    content: "A black hole is a region of spacetime where gravity is so strong that nothing—not even light—can escape once it crosses the event horizon. They form when massive stars collapse at the end of their lives. Black holes have three main parts: the singularity (infinitely dense center), the event horizon (point of no return), and the accretion disk (swirling matter being pulled in). Supermassive black holes exist at the centers of most galaxies.".to_string(),
                    related_concepts: vec!["gravity".to_string(), "event horizon".to_string(), "singularity".to_string(), "spacetime".to_string()],
                    metadata: None,
                },
            ],
        };
        
        let astronomy_path = self.knowledge_dir.join("astronomy.json");
        let json = serde_json::to_string_pretty(&astronomy_knowledge)?;
        fs::write(astronomy_path, json)?;
        
        // Create a sample technology knowledge file
        let tech_knowledge = KnowledgeFile {
            domain: "computer_science".to_string(),
            entries: vec![
                KnowledgeEntry {
                    topic: "Quantum Computing".to_string(),
                    content: "Quantum computing harnesses quantum mechanical phenomena like superposition and entanglement to process information. Unlike classical bits (0 or 1), quantum bits (qubits) can exist in superposition of both states simultaneously. This enables quantum computers to solve certain problems exponentially faster than classical computers, particularly in cryptography, drug discovery, and optimization. Current challenges include maintaining quantum coherence and error correction.".to_string(),
                    related_concepts: vec!["qubit".to_string(), "superposition".to_string(), "entanglement".to_string(), "quantum supremacy".to_string()],
                    metadata: None,
                },
                KnowledgeEntry {
                    topic: "Neural Networks".to_string(),
                    content: "Neural networks are computing systems inspired by biological neural networks in animal brains. They consist of interconnected nodes (neurons) organized in layers: input, hidden, and output. Through training on data, they adjust connection weights to learn patterns. Deep learning uses networks with many hidden layers. Applications include image recognition, natural language processing, and game playing. Key concepts include backpropagation, activation functions, and gradient descent.".to_string(),
                    related_concepts: vec!["deep learning".to_string(), "artificial intelligence".to_string(), "machine learning".to_string(), "backpropagation".to_string()],
                    metadata: None,
                },
            ],
        };
        
        let tech_path = self.knowledge_dir.join("technology.json");
        let json = serde_json::to_string_pretty(&tech_knowledge)?;
        fs::write(tech_path, json)?;
        
        println!("📝 Created default knowledge files in {:?}", self.knowledge_dir);
        
        Ok(())
    }
    
    /// Watch for changes in knowledge files (for hot reloading)
    pub fn watch_for_changes(&self, engine: Arc<KnowledgeEngine>) -> Result<(), Box<dyn std::error::Error>> {
        // This would use a file watcher like notify crate
        // For now, just a placeholder
        println!("👁️  Watching {:?} for changes...", self.knowledge_dir);
        Ok(())
    }
    
    /// Export current knowledge to files
    pub fn export_knowledge(&self, engine: &Arc<KnowledgeEngine>) -> Result<(), Box<dyn std::error::Error>> {
        let all_nodes = engine.get_all_nodes();
        let mut domain_map: HashMap<KnowledgeDomain, Vec<KnowledgeEntry>> = HashMap::new();
        
        for (_, node) in all_nodes {
            let entry = KnowledgeEntry {
                topic: node.topic,
                content: node.content,
                related_concepts: node.related_concepts,
                metadata: None,
            };
            
            domain_map.entry(node.domain)
                .or_insert_with(Vec::new)
                .push(entry);
        }
        
        for (domain, entries) in domain_map {
            let knowledge_file = KnowledgeFile {
                domain: format!("{:?}", domain).to_lowercase(),
                entries,
            };
            
            let filename = format!("{}_export.json", knowledge_file.domain);
            let path = self.knowledge_dir.join(filename);
            let json = serde_json::to_string_pretty(&knowledge_file)?;
            fs::write(path, json)?;
        }
        
        println!("📤 Exported knowledge to {:?}", self.knowledge_dir);
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::tempdir;
    
    #[test]
    fn test_dynamic_loader() {
        let dir = tempdir().unwrap();
        let loader = DynamicKnowledgeLoader::new(dir.path());
        let engine = Arc::new(KnowledgeEngine::new());
        
        // Should create default files
        let count = loader.load_all(&engine).unwrap();
        assert!(count > 0);
        
        // Check that knowledge was loaded
        let stats = engine.get_stats();
        assert!(stats.total_nodes > 0);
    }
}