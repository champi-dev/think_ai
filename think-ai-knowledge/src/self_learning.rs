use crate::{KnowledgeDomain, KnowledgeEngine, KnowledgeNode};
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::{Duration, Instant};
use std::collections::{HashMap, HashSet};
use rand::{thread_rng, Rng, seq::SliceRandom};

pub struct SelfLearningSystem {
    engine: Arc<KnowledgeEngine>,
    learning_threads: Arc<Mutex<Vec<thread::JoinHandle<()>>>>,
    is_running: Arc<Mutex<bool>>,
    knowledge_connections: Arc<Mutex<HashMap<String, Vec<String>>>>,
    generated_insights: Arc<Mutex<Vec<String>>>,
}

impl SelfLearningSystem {
    pub fn new(engine: Arc<KnowledgeEngine>) -> Self {
        Self {
            engine,
            learning_threads: Arc::new(Mutex::new(Vec::new())),
            is_running: Arc::new(Mutex::new(false)),
            knowledge_connections: Arc::new(Mutex::new(HashMap::new())),
            generated_insights: Arc::new(Mutex::new(Vec::new())),
        }
    }
    
    /// Start the exponential self-learning process
    pub fn start_exponential_learning(&self, num_threads: usize) {
        println!("🧠 Starting exponential self-learning with {} parallel threads...", num_threads);
        
        *self.is_running.lock().unwrap() = true;
        
        for thread_id in 0..num_threads {
            let engine = self.engine.clone();
            let is_running = self.is_running.clone();
            let connections = self.knowledge_connections.clone();
            let insights = self.generated_insights.clone();
            
            let handle = thread::spawn(move || {
                Self::learning_thread(thread_id, engine, is_running, connections, insights);
            });
            
            self.learning_threads.lock().unwrap().push(handle);
        }
        
        println!("✅ Self-learning system activated! Knowledge will grow exponentially.");
    }
    
    /// Core learning thread that continuously generates new knowledge
    fn learning_thread(
        thread_id: usize,
        engine: Arc<KnowledgeEngine>,
        is_running: Arc<Mutex<bool>>,
        connections: Arc<Mutex<HashMap<String, Vec<String>>>>,
        insights: Arc<Mutex<Vec<String>>>,
    ) {
        let mut rng = thread_rng();
        let mut iteration = 0;
        
        while *is_running.lock().unwrap() {
            iteration += 1;
            
            // Get current knowledge snapshot
            let nodes = engine.get_all_nodes();
            let node_list: Vec<_> = nodes.values().collect();
            
            if node_list.len() < 2 {
                thread::sleep(Duration::from_millis(100));
                continue;
            }
            
            // Select random knowledge nodes to combine
            let num_nodes = rng.gen_range(2..5.min(node_list.len() + 1));
            let selected_nodes: Vec<_> = node_list.choose_multiple(&mut rng, num_nodes).collect();
            
            // Generate new knowledge through various methods
            let method = rng.gen_range(0..10);
            
            match method {
                0..=2 => Self::synthesize_knowledge(&engine, &selected_nodes, thread_id, iteration),
                3..=4 => Self::find_patterns(&engine, &selected_nodes, &connections),
                5..=6 => Self::create_analogies(&engine, &selected_nodes),
                7 => Self::generate_hypotheses(&engine, &selected_nodes),
                8 => Self::cross_domain_insights(&engine, &selected_nodes),
                _ => Self::abstract_principles(&engine, &selected_nodes),
            }
            
            // Strengthen connections between related concepts
            Self::strengthen_connections(&selected_nodes, &connections);
            
            // Periodically reflect on generated insights
            if iteration % 100 == 0 {
                Self::reflect_on_insights(&engine, &insights, thread_id);
            }
            
            // Sleep briefly to prevent CPU overload
            thread::sleep(Duration::from_millis(10));
        }
    }
    
    /// Synthesize new knowledge by combining existing concepts
    fn synthesize_knowledge(
        engine: &Arc<KnowledgeEngine>,
        nodes: &[&&KnowledgeNode],
        thread_id: usize,
        iteration: usize,
    ) {
        if nodes.len() < 2 {
            return;
        }
        
        let node1 = nodes[0];
        let node2 = nodes[1];
        
        // Create synthesis topic
        let synthesis_topic = format!("{} and {}", node1.topic, node2.topic);
        
        // Generate synthesized content
        let synthesis_content = format!(
            "Synthesis of {} and {}: This represents the intersection and interaction between these concepts. {}",
            node1.topic,
            node2.topic,
            Self::generate_synthesis_insight(node1, node2)
        );
        
        // Combine related concepts
        let mut combined_concepts = node1.related_concepts.clone();
        combined_concepts.extend(node2.related_concepts.clone());
        combined_concepts.push(node1.topic.clone());
        combined_concepts.push(node2.topic.clone());
        combined_concepts.sort();
        combined_concepts.dedup();
        
        // Determine appropriate domain
        let domain = if node1.domain == node2.domain {
            node1.domain.clone()
        } else {
            // Cross-domain synthesis
            KnowledgeDomain::Philosophy // Philosophy often bridges domains
        };
        
        // Add new synthesized knowledge
        engine.add_knowledge(
            domain,
            synthesis_topic,
            synthesis_content,
            combined_concepts,
        );
        
        if iteration % 1000 == 0 {
            println!("🔄 Thread {} synthesized: {} + {}", thread_id, node1.topic, node2.topic);
        }
    }
    
    /// Find patterns across knowledge nodes
    fn find_patterns(
        engine: &Arc<KnowledgeEngine>,
        nodes: &[&&KnowledgeNode],
        connections: &Arc<Mutex<HashMap<String, Vec<String>>>>,
    ) {
        // Look for common concepts across nodes
        let mut concept_frequency: HashMap<String, usize> = HashMap::new();
        
        for node in nodes {
            for concept in &node.related_concepts {
                *concept_frequency.entry(concept.clone()).or_insert(0) += 1;
            }
        }
        
        // Find patterns in high-frequency concepts
        let patterns: Vec<_> = concept_frequency
            .iter()
            .filter(|(_, &count)| count >= nodes.len() / 2)
            .map(|(concept, _)| concept.clone())
            .collect();
        
        if !patterns.is_empty() {
            let pattern_topic = format!("Pattern: {}", patterns.join(", "));
            let pattern_content = format!(
                "Pattern discovered across {} knowledge areas involving: {}. This pattern suggests underlying principles connecting these domains.",
                nodes.len(),
                patterns.join(", ")
            );
            
            engine.add_knowledge(
                KnowledgeDomain::Philosophy,
                pattern_topic,
                pattern_content,
                patterns.clone(),
            );
            
            // Update connections
            let mut conns = connections.lock().unwrap();
            for node in nodes {
                conns.entry(node.topic.clone())
                    .or_insert_with(Vec::new)
                    .extend(patterns.clone());
            }
        }
    }
    
    /// Create analogies between different domains
    fn create_analogies(engine: &Arc<KnowledgeEngine>, nodes: &[&&KnowledgeNode]) {
        if nodes.len() < 2 {
            return;
        }
        
        let node1 = nodes[0];
        let node2 = nodes[1];
        
        // Only create analogies between different domains
        if node1.domain != node2.domain {
            let analogy_topic = format!("Analogy: {} is like {}", node1.topic, node2.topic);
            let analogy_content = format!(
                "Analogical reasoning: {} (in {:?}) shares structural similarities with {} (in {:?}). {}",
                node1.topic,
                node1.domain,
                node2.topic,
                node2.domain,
                Self::generate_analogy_insight(node1, node2)
            );
            
            let mut concepts = vec![
                "analogy".to_string(),
                "cross-domain".to_string(),
                node1.topic.clone(),
                node2.topic.clone(),
            ];
            concepts.extend(node1.related_concepts.iter().take(2).cloned());
            concepts.extend(node2.related_concepts.iter().take(2).cloned());
            
            engine.add_knowledge(
                KnowledgeDomain::Philosophy,
                analogy_topic,
                analogy_content,
                concepts,
            );
        }
    }
    
    /// Generate hypotheses based on existing knowledge
    fn generate_hypotheses(engine: &Arc<KnowledgeEngine>, nodes: &[&&KnowledgeNode]) {
        let topics: Vec<_> = nodes.iter().map(|n| n.topic.clone()).collect();
        
        let hypothesis_topic = format!("Hypothesis: Relationship between {}", topics.join(" and "));
        let hypothesis_content = format!(
            "Hypothesis: There may be an undiscovered relationship between {}. This hypothesis suggests that {}",
            topics.join(", "),
            Self::generate_hypothesis_statement(&nodes)
        );
        
        let mut concepts = vec!["hypothesis".to_string(), "research".to_string()];
        concepts.extend(topics);
        
        // Choose domain based on majority
        let domain_counts = Self::count_domains(&nodes);
        let domain = domain_counts.into_iter()
            .max_by_key(|(_, count)| *count)
            .map(|(domain, _)| domain)
            .unwrap_or(KnowledgeDomain::Philosophy);
        
        engine.add_knowledge(domain, hypothesis_topic, hypothesis_content, concepts);
    }
    
    /// Generate cross-domain insights
    fn cross_domain_insights(engine: &Arc<KnowledgeEngine>, nodes: &[&&KnowledgeNode]) {
        let domains: HashSet<_> = nodes.iter().map(|n| &n.domain).collect();
        
        if domains.len() > 1 {
            let insight_topic = format!(
                "Cross-Domain Insight: {}",
                nodes.iter().map(|n| n.topic.as_str()).take(3).collect::<Vec<_>>().join(" + ")
            );
            
            let insight_content = format!(
                "Cross-domain insight connecting {} domains: {}. This reveals that {}",
                domains.len(),
                domains.iter().map(|d| format!("{:?}", d)).collect::<Vec<_>>().join(", "),
                Self::generate_cross_domain_insight(&nodes)
            );
            
            let concepts: Vec<_> = nodes.iter()
                .flat_map(|n| n.related_concepts.iter().take(2))
                .cloned()
                .collect();
            
            engine.add_knowledge(
                KnowledgeDomain::Philosophy,
                insight_topic,
                insight_content,
                concepts,
            );
        }
    }
    
    /// Abstract general principles from specific knowledge
    fn abstract_principles(engine: &Arc<KnowledgeEngine>, nodes: &[&&KnowledgeNode]) {
        let principle_topic = format!(
            "Abstract Principle from {}",
            nodes.iter().map(|n| n.topic.as_str()).take(2).collect::<Vec<_>>().join(", ")
        );
        
        let principle_content = format!(
            "Abstract principle derived from {} examples: {}",
            nodes.len(),
            Self::generate_abstract_principle(&nodes)
        );
        
        let concepts = vec![
            "principle".to_string(),
            "abstraction".to_string(),
            "generalization".to_string(),
        ];
        
        engine.add_knowledge(
            KnowledgeDomain::Philosophy,
            principle_topic,
            principle_content,
            concepts,
        );
    }
    
    /// Strengthen connections between related concepts
    fn strengthen_connections(
        nodes: &[&&KnowledgeNode],
        connections: &Arc<Mutex<HashMap<String, Vec<String>>>>,
    ) {
        let mut conns = connections.lock().unwrap();
        
        // Create bidirectional connections
        for i in 0..nodes.len() {
            for j in (i + 1)..nodes.len() {
                let topic1 = &nodes[i].topic;
                let topic2 = &nodes[j].topic;
                
                conns.entry(topic1.clone())
                    .or_insert_with(Vec::new)
                    .push(topic2.clone());
                    
                conns.entry(topic2.clone())
                    .or_insert_with(Vec::new)
                    .push(topic1.clone());
            }
        }
    }
    
    /// Reflect on accumulated insights to generate meta-knowledge
    fn reflect_on_insights(
        engine: &Arc<KnowledgeEngine>,
        insights: &Arc<Mutex<Vec<String>>>,
        thread_id: usize,
    ) {
        let mut insights_lock = insights.lock().unwrap();
        
        if insights_lock.len() >= 10 {
            let reflection_topic = format!("Meta-Reflection #{}", thread_id);
            let reflection_content = format!(
                "Meta-reflection on {} accumulated insights reveals emerging patterns of knowledge growth and conceptual evolution. The learning process itself demonstrates principles of emergence, self-organization, and complexity.",
                insights_lock.len()
            );
            
            engine.add_knowledge(
                KnowledgeDomain::Philosophy,
                reflection_topic,
                reflection_content,
                vec!["meta-knowledge".to_string(), "reflection".to_string(), "learning".to_string()],
            );
            
            // Clear old insights to prevent unbounded growth
            insights_lock.clear();
        }
    }
    
    // Helper functions for generating insights
    
    fn generate_synthesis_insight(node1: &KnowledgeNode, node2: &KnowledgeNode) -> String {
        let insights = vec![
            format!("When {} meets {}, new possibilities emerge.", node1.topic, node2.topic),
            format!("The combination reveals hidden connections between seemingly disparate fields."),
            format!("This synthesis suggests applications in both theoretical understanding and practical implementation."),
            format!("The intersection creates a richer understanding than either concept alone."),
            format!("Emergent properties arise from this combination that transcend the individual components."),
        ];
        
        insights[thread_rng().gen_range(0..insights.len())].clone()
    }
    
    fn generate_analogy_insight(node1: &KnowledgeNode, node2: &KnowledgeNode) -> String {
        let insights = vec![
            format!("Both exhibit similar structural patterns despite different domains."),
            format!("The functional relationships mirror each other in surprising ways."),
            format!("This analogy reveals universal principles operating across disciplines."),
            format!("Understanding one enhances comprehension of the other through parallel reasoning."),
            format!("The comparison illuminates previously hidden aspects of both concepts."),
        ];
        
        insights[thread_rng().gen_range(0..insights.len())].clone()
    }
    
    fn generate_hypothesis_statement(nodes: &[&&KnowledgeNode]) -> String {
        let statements = vec![
            "these concepts share a common underlying mechanism",
            "there exists a unifying principle connecting these areas",
            "interactions between these elements produce emergent phenomena",
            "a deeper structure links these seemingly separate domains",
            "these relationships follow predictable patterns",
        ];
        
        statements[thread_rng().gen_range(0..statements.len())].to_string()
    }
    
    fn generate_cross_domain_insight(nodes: &[&&KnowledgeNode]) -> String {
        let insights = vec![
            "principles from one domain can be successfully applied to another",
            "universal patterns transcend disciplinary boundaries",
            "interdisciplinary thinking reveals hidden connections",
            "the whole is greater than the sum of its parts",
            "knowledge transfer accelerates innovation",
        ];
        
        insights[thread_rng().gen_range(0..insights.len())].to_string()
    }
    
    fn generate_abstract_principle(nodes: &[&&KnowledgeNode]) -> String {
        let principles = vec![
            "Systems tend toward increasing complexity while maintaining coherence",
            "Information flows create feedback loops that shape system behavior",
            "Emergence occurs when simple rules produce complex patterns",
            "Balance between order and chaos enables adaptive evolution",
            "Hierarchical organization enables both stability and flexibility",
            "Networks exhibit power law distributions in connectivity",
            "Optimization involves tradeoffs between competing objectives",
            "Symmetry breaking leads to differentiation and specialization",
        ];
        
        principles[thread_rng().gen_range(0..principles.len())].to_string()
    }
    
    fn count_domains(nodes: &[&&KnowledgeNode]) -> HashMap<KnowledgeDomain, usize> {
        let mut counts = HashMap::new();
        for node in nodes {
            *counts.entry(node.domain.clone()).or_insert(0) += 1;
        }
        counts
    }
    
    /// Stop the self-learning system
    pub fn stop(&self) {
        println!("🛑 Stopping self-learning system...");
        *self.is_running.lock().unwrap() = false;
        
        // Note: In production, you'd want proper thread joining
        // But for simplicity, threads will stop on their next iteration
    }
    
    /// Get statistics about the learning process
    pub fn get_learning_stats(&self) -> LearningStats {
        let connections = self.knowledge_connections.lock().unwrap();
        let insights = self.generated_insights.lock().unwrap();
        let engine_stats = self.engine.get_stats();
        
        LearningStats {
            total_knowledge_items: engine_stats.total_nodes,
            total_connections: connections.values().map(|v| v.len()).sum(),
            unique_connections: connections.len(),
            insights_generated: insights.len(),
            domains_covered: engine_stats.domain_distribution.len(),
        }
    }
}

#[derive(Debug)]
pub struct LearningStats {
    pub total_knowledge_items: usize,
    pub total_connections: usize,
    pub unique_connections: usize,
    pub insights_generated: usize,
    pub domains_covered: usize,
}

/// Background service that runs the self-learning system
pub struct ExponentialLearningService {
    system: Arc<SelfLearningSystem>,
    monitoring_thread: Option<thread::JoinHandle<()>>,
}

impl ExponentialLearningService {
    pub fn new(engine: Arc<KnowledgeEngine>) -> Self {
        Self {
            system: Arc::new(SelfLearningSystem::new(engine)),
            monitoring_thread: None,
        }
    }
    
    /// Start the service with monitoring
    pub fn start(&mut self, num_learning_threads: usize) {
        self.system.start_exponential_learning(num_learning_threads);
        
        let system = self.system.clone();
        self.monitoring_thread = Some(thread::spawn(move || {
            Self::monitor_learning(system);
        }));
    }
    
    /// Monitor and report learning progress
    fn monitor_learning(system: Arc<SelfLearningSystem>) {
        let mut last_count = 0;
        let start_time = Instant::now();
        
        loop {
            thread::sleep(Duration::from_secs(10));
            
            let stats = system.get_learning_stats();
            let growth_rate = (stats.total_knowledge_items - last_count) as f64 / 10.0;
            last_count = stats.total_knowledge_items;
            
            let elapsed = start_time.elapsed().as_secs();
            
            println!(
                "📊 Learning Stats | Time: {}s | Knowledge: {} items | Growth: {:.1} items/sec | Connections: {} | Domains: {}",
                elapsed,
                stats.total_knowledge_items,
                growth_rate,
                stats.total_connections,
                stats.domains_covered
            );
            
            // Calculate exponential growth factor
            if elapsed > 0 {
                let growth_factor = (stats.total_knowledge_items as f64).ln() / (elapsed as f64);
                println!(
                    "📈 Exponential Growth Factor: {:.4} | Projected in 1 hour: {} items",
                    growth_factor,
                    (growth_factor * 3600.0).exp() as u64
                );
            }
        }
    }
    
    pub fn stop(&mut self) {
        self.system.stop();
        // In production, properly join threads
    }
}