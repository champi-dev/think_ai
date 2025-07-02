#!/usr/bin/env rust-script

//! Cleanup utility to remove problematic abstract principles from knowledge storage

use std::sync::Arc;
use std::path::Path;
use std::fs;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🧹 Think AI Knowledge Cleanup Utility");
    println!("=====================================");
    println!();
    
    // Simple approach: Remove the problematic knowledge storage directories
    // This will force the system to reload only the good comprehensive knowledge
    
    let storage_paths = [
        "./trained_knowledge",
        "./knowledge_storage", 
        "trained_knowledge",
        "knowledge_storage"
    ];
    
    let mut removed_count = 0;
    
    for path in &storage_paths {
        if Path::new(path).exists() {
            match fs::remove_dir_all(path) {
                Ok(_) => {
                    println!("✅ Removed directory: {}", path);
                    removed_count += 1;
                },
                Err(e) => {
                    println!("⚠️  Could not remove {}: {}", path, e);
                }
            }
        }
    }
    
    if removed_count > 0 {
        println!();
        println!("🎉 Cleanup complete!");
        println!("   Removed {} storage directories containing problematic abstract principles.", removed_count);
        println!("   Think AI will now use only the comprehensive knowledge base,");
        println!("   which contains proper specific answers instead of generic abstractions.");
        println!();
        println!("💡 Next time you run Think AI, it will load fresh knowledge without the");
        println!("   problematic 'Abstract principle derived from X examples' responses.");
    } else {
        println!("ℹ️  No knowledge storage directories found to clean.");
    }
    
    Ok(())
}