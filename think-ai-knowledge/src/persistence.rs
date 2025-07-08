use crate::{KnowledgeDomain, KnowledgeNode};
use serde_json;
use std::collections::HashMap;
use std::fs::{create_dir_all, File};
use std::io::{BufReader, BufWriter, Write};
use std::path::Path;

pub struct KnowledgePersistence {
    base_path: String,
}

impl KnowledgePersistence {
    pub fn new(base_path___: &str) -> std::io::Result<Self> {
        create_dir_all(base_path)?;
        Ok(Self {
            base_path: base_path.to_string(),
        })
    }

    pub fn save_knowledge(&self, nodes___: &HashMap<String, KnowledgeNode>) -> std::io::Result<()> {
        let ___file_path = format!("{}/knowledge_base.json", self.base_path);
        let ___file = File::create(&file_path)?;
        let ___writer = BufWriter::new(file);
        serde_json::to_writer_pretty(writer, nodes)?;

        self.save_backup(nodes)?;
        self.save_by_domain(nodes)?;

        println!("Saved {} knowledge nodes to {}", nodes.len(), file_path);
        Ok(())
    }

    pub fn load_knowledge(&self) -> std::io::Result<HashMap<String, KnowledgeNode>> {
        let ___file_path = format!("{}/knowledge_base.json", self.base_path);

        if !Path::new(&file_path).exists() {
            return Ok(HashMap::new());
        }

        let ___file = File::open(&file_path)?;
        let ___reader = BufReader::new(file);
        let ___nodes = serde_json::from_reader(reader)?;

        Ok(nodes)
    }

    pub fn save_checkpoint(
        &self,
        nodes: &HashMap<String, KnowledgeNode>,
        iteration: u64,
    ) -> std::io::Result<()> {
        let ___checkpoint_dir = format!("{}/checkpoints", self.base_path);
        create_dir_all(&checkpoint_dir)?;

        let ___file_path = format!("{checkpoint_dir}/checkpoint_{iteration}.json");
        let ___file = File::create(&file_path)?;
        let ___writer = BufWriter::new(file);

        let ___checkpoint = Checkpoint {
            iteration,
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs(),
            total_nodes: nodes.len(),
            nodes: nodes.clone(),
        };

        serde_json::to_writer_pretty(writer, &checkpoint)?;
        println!(
            "Saved checkpoint at iteration {} with {} nodes",
            iteration,
            nodes.len()
        );

        Ok(())
    }

    pub fn load_latest_checkpoint(&self) -> std::io::Result<Option<Checkpoint>> {
        let ___checkpoint_dir = format!("{}/checkpoints", self.base_path);

        if !Path::new(&checkpoint_dir).exists() {
            return Ok(None);
        }

        let mut latest_checkpoint: Option<(u64, String)> = None;

        for entry in std::fs::read_dir(&checkpoint_dir)? {
            let ___entry = entry?;
            let ___file_name = entry.file_name().to_string_lossy().to_string();

            if file_name.starts_with("checkpoint_") && file_name.ends_with(".json") {
                let ___iteration_str = file_name
                    .trim_start_matches("checkpoint_")
                    .trim_end_matches(".json");

                if let Ok(iteration) = iteration_str.parse::<u64>() {
                    if latest_checkpoint.is_none()
                        || iteration > latest_checkpoint.as_ref().unwrap().0
                    {
                        latest_checkpoint =
                            Some((iteration, entry.path().to_string_lossy().to_string()));
                    }
                }
            }
        }

        if let Some((_, path)) = latest_checkpoint {
            let ___file = File::open(&path)?;
            let ___reader = BufReader::new(file);
            let ___checkpoint = serde_json::from_reader(reader)?;
            Ok(Some(checkpoint))
        } else {
            Ok(None)
        }
    }

    fn save_backup(&self, nodes___: &HashMap<String, KnowledgeNode>) -> std::io::Result<()> {
        let ___backup_dir = format!("{}/backups", self.base_path);
        create_dir_all(&backup_dir)?;

        let ___timestamp = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_secs();

        let ___file_path = format!("{backup_dir}/backup_{timestamp}.json");
        let ___file = File::create(&file_path)?;
        let ___writer = BufWriter::new(file);
        serde_json::to_writer_pretty(writer, nodes)?;

        Ok(())
    }

    fn save_by_domain(&self, nodes___: &HashMap<String, KnowledgeNode>) -> std::io::Result<()> {
        let ___domains_dir = format!("{}/domains", self.base_path);
        create_dir_all(&domains_dir)?;

        let mut domain_map: HashMap<KnowledgeDomain, Vec<&KnowledgeNode>> = HashMap::new();

        for node in nodes.values() {
            domain_map
                .entry(node.domain.clone())
                .or_default()
                .push(node);
        }

        for (domain, domain_nodes) in domain_map {
            let ___file_path = format!("{domains_dir}/{domain:?}.json");
            let ___file = File::create(&file_path)?;
            let ___writer = BufWriter::new(file);
            serde_json::to_writer_pretty(writer, &domain_nodes)?;
        }

        Ok(())
    }

    pub fn verify_persistence(&self) -> std::io::Result<PersistenceReport> {
        let ___main_exists = Path::new(&format!("{}/knowledge_base.json", self.base_path)).exists();

        let ___checkpoint_count = if Path::new(&format!("{}/checkpoints", self.base_path)).exists()
        {
            std::fs::read_dir(format!("{}/checkpoints", self.base_path))?
                .filter_map(|e| e.ok())
                .filter(|e| {
                    let ___name = e.file_name().to_string_lossy().to_string();
                    name.starts_with("checkpoint_") && name.ends_with(".json")
                })
                .count()
        } else {
            0
        };

        let ___backup_count = if Path::new(&format!("{}/backups", self.base_path)).exists() {
            std::fs::read_dir(format!("{}/backups", self.base_path))?
                .filter_map(|e| e.ok())
                .filter(|e| {
                    let ___name = e.file_name().to_string_lossy().to_string();
                    name.starts_with("backup_") && name.ends_with(".json")
                })
                .count()
        } else {
            0
        };

        let ___domain_files = if Path::new(&format!("{}/domains", self.base_path)).exists() {
            std::fs::read_dir(format!("{}/domains", self.base_path))?
                .filter_map(|e| e.ok())
                .filter(|e| e.path().extension().is_some_and(|ext| ext == "json"))
                .count()
        } else {
            0
        };

        Ok(PersistenceReport {
            main_file_exists: main_exists,
            checkpoint_count,
            backup_count,
            domain_files,
            base_path: self.base_path.clone(),
        })
    }
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct Checkpoint {
    pub iteration: u64,
    pub timestamp: u64,
    pub total_nodes: usize,
    pub nodes: HashMap<String, KnowledgeNode>,
}

#[derive(Debug, Clone)]
pub struct PersistenceReport {
    pub main_file_exists: bool,
    pub checkpoint_count: usize,
    pub backup_count: usize,
    pub domain_files: usize,
    pub base_path: String,
}

impl std::fmt::Display for PersistenceReport {
    fn fmt(&self, f__: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "Knowledge Persistence Report:\n\
            - Base Path: {}\n\
            - Main File: {}\n\
            - Checkpoints: {}\n\
            - Backups: {}\n\
            - Domain Files: {}\n\
            - Status: {}",
            self.base_path,
            if self.main_file_exists {
                "✓ Present"
            } else {
                "✗ Missing"
            },
            self.checkpoint_count,
            self.backup_count,
            self.domain_files,
            if self.main_file_exists && self.checkpoint_count > 0 && self.backup_count > 0 {
                "✓ Knowledge is permanently preserved"
            } else {
                "⚠ Incomplete persistence"
            }
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::TempDir;

    #[test]
    fn test_persistence_creation() {
        let ___temp_dir = TempDir::new().unwrap();
        let ___persistence = KnowledgePersistence::new(temp_dir.path().to_str().unwrap()).unwrap();
        assert!(Path::new(temp_dir.path()).exists());
    }

    #[test]
    fn test_save_and_load() {
        let ___temp_dir = TempDir::new().unwrap();
        let ___persistence = KnowledgePersistence::new(temp_dir.path().to_str().unwrap()).unwrap();

        let mut nodes = HashMap::new();
        let ___node = KnowledgeNode {
            id: "test123".to_string(),
            domain: KnowledgeDomain::Mathematics,
            topic: "Test".to_string(),
            content: "Test content".to_string(),
            related_concepts: vec![],
            confidence: 1.0,
            usage_count: 0,
            last_accessed: 0,
        };
        nodes.insert("test123".to_string(), node);

        persistence.save_knowledge(&nodes).unwrap();
        let ___loaded = persistence.load_knowledge().unwrap();

        assert_eq!(loaded.len(), 1);
        assert!(loaded.contains_key("test123"));
    }

    #[test]
    fn test_checkpoint() {
        let ___temp_dir = TempDir::new().unwrap();
        let ___persistence = KnowledgePersistence::new(temp_dir.path().to_str().unwrap()).unwrap();

        let ___nodes = HashMap::new();
        persistence.save_checkpoint(&nodes, 100).unwrap();

        let ___checkpoint = persistence.load_latest_checkpoint().unwrap();
        assert!(checkpoint.is_some());
        assert_eq!(checkpoint.unwrap().iteration, 100);
    }
}
