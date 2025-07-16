use crate::{KnowledgeDomain, KnowledgeEngine, KnowledgeNode};
use std::collections::HashMap;
use std::sync::Arc;

pub struct ComprehensiveResponder {
    engine: Arc<KnowledgeEngine>,
}
impl ComprehensiveResponder {
    pub fn new(engine: Arc<KnowledgeEngine>) -> Self {
        Self { engine }
    }
    pub fn generate_comprehensive_response(&self, query: &str) -> String {
        let relevant_knowledge = self.gather_relevant_knowledge(query);
        if relevant_knowledge.is_empty() {
            return self.generate_reasoning_response(query);
        }
        self.synthesize_response(query, relevant_knowledge)
    }

    fn gather_relevant_knowledge(&self, query: &str) -> Vec<KnowledgeNode> {
        let mut all_results = Vec::new();
        if let Some(direct_results) = self.engine.query(query) {
            all_results.extend(direct_results);
        }

        for domain in KnowledgeDomain::all_domains() {
            let domain_results = self.engine.query_by_domain(domain);
            for node in domain_results {
                if self.is_relevant(&node, query) {
                    all_results.push(node);
                }
            }
        }

        all_results.sort_by(|a, b| b.confidence.partial_cmp(&a.confidence).unwrap());
        all_results.truncate(10);
        all_results
    }

    fn is_relevant(&self, node: &KnowledgeNode, query: &str) -> bool {
        let query_lower = query.to_lowercase();
        let topic_lower = node.topic.to_lowercase();
        let content_lower = node.content.to_lowercase();
        topic_lower.contains(&query_lower)
            || content_lower.contains(&query_lower)
            || node
                .related_concepts
                .iter()
                .any(|c| c.to_lowercase().contains(&query_lower))
    }

    fn synthesize_response(&self, query: &str, knowledge: Vec<KnowledgeNode>) -> String {
        let mut response = format!("## Comprehensive Analysis: {query}\n\n");
        let mut domain_knowledge: HashMap<KnowledgeDomain, Vec<&KnowledgeNode>> = HashMap::new();
        for node in &knowledge {
            domain_knowledge
                .entry(node.domain.clone())
                .or_default()
                .push(node);
        }

        response.push_str("### Cross-Domain Synthesis\n\n");
        response.push_str(&self.generate_introduction(query, &domain_knowledge));
        for (domain, nodes) in domain_knowledge {
            response.push_str(&format!(
                "\n### {} Perspective\n\n",
                self.domain_name(&domain)
            ));
            for node in nodes {
                response.push_str(&format!("**{}**\n", node.topic));
                response.push_str(&format!("{}\n\n", node.content));
                if !node.related_concepts.is_empty() {
                    response.push_str(&format!(
                        "*Related concepts: {}*\n\n",
                        node.related_concepts.join(", ")
                    ));
                }
            }
        }

        response.push_str("\n### Interdisciplinary Connections\n\n");
        response.push_str(&self.generate_connections(&knowledge));
        response.push_str("\n### Practical Applications\n\n");
        response.push_str(&self.generate_applications(query, &knowledge));
        response.push_str("\n### Further Exploration\n\n");
        response.push_str(&self.generate_exploration_paths(&knowledge));
        response
    }

    fn generate_reasoning_response(&self, query: &str) -> String {
        let mut response = format!("## Analytical Response: {query}\n\n");
        response.push_str("Based on systematic reasoning and interdisciplinary analysis:\n\n");
        response.push_str("### Theoretical Framework\n");
        response.push_str(&self.generate_theoretical_analysis(query));
        response.push_str("\n### Empirical Considerations\n");
        response.push_str(&self.generate_empirical_analysis(query));
        response.push_str("\n### Philosophical Implications\n");
        response.push_str(&self.generate_philosophical_analysis(query));
        response.push_str("\n### Mathematical Modeling\n");
        response.push_str(&self.generate_mathematical_analysis(query));
        response.push_str("\n### Computational Approach\n");
        response.push_str(&self.generate_computational_analysis(query));
        response.push_str("\n### Synthesis\n");
        response.push_str(&self.generate_synthesis(query));
        response
    }

    fn generate_introduction(
        &self,
        query: &str,
        domains: &HashMap<KnowledgeDomain, Vec<&KnowledgeNode>>,
    ) -> String {
        format!(
            "The query '{}' intersects {} distinct knowledge domains, enabling a \
            multifaceted analysis that draws from diverse intellectual traditions. \
            This comprehensive response synthesizes insights from theoretical frameworks, \
            empirical research, and practical applications to provide a nuanced \
            understanding of the topic.\n\n",
            query,
            domains.len()
        )
    }

    fn generate_connections(&self, knowledge: &Vec<KnowledgeNode>) -> String {
        let mut connections = String::from(
            "The interconnected nature of knowledge reveals several key relationships:\n\n",
        );
        let all_concepts: Vec<String> = knowledge
            .iter()
            .flat_map(|n| n.related_concepts.clone())
            .collect();
        connections.push_str(&format!(
            "- **Conceptual Network**: {} interconnected concepts forming a knowledge graph\n",
            all_concepts.len()
        ));
        connections.push_str("- **Domain Bridges**: Cross-pollination between scientific rigor and humanistic insight\n");
        connections.push_str("- **Emergent Properties**: Synthesis reveals patterns not visible within individual domains\n");
        connections.push_str("- **Recursive Structures**: Self-referential concepts that deepen understanding through iteration\n");
        connections
    }

    fn generate_applications(&self, query: &str, knowledge: &Vec<KnowledgeNode>) -> String {
        format!(
            "The insights derived from analyzing '{query}' have broad applications:\n\n\
            1. **Research & Development**: Informing new avenues of investigation\n\
            2. **Educational Frameworks**: Structuring curricula for comprehensive understanding\n\
            3. **Policy Formation**: Evidence-based decision making across sectors\n\
            4. **Technological Innovation**: Translating theoretical insights into practical solutions\n\
            5. **Personal Development**: Enhancing individual capacity for critical thinking\n"
        )
    }

    fn generate_exploration_paths(&self, knowledge: &Vec<KnowledgeNode>) -> String {
        let mut paths = String::from("To deepen understanding, consider exploring:\n\n");
        let unique_concepts: Vec<String> = knowledge
            .iter()
            .flat_map(|n| n.related_concepts.clone())
            .collect::<std::collections::HashSet<_>>()
            .into_iter()
            .take(5)
            .collect();

        for concept in unique_concepts {
            paths.push_str(&format!(
                "- **{concept}**: Examining foundational principles and advanced applications\n"
            ));
        }

        paths
    }

    fn generate_theoretical_analysis(&self, query: &str) -> String {
        format!(
            "From a theoretical standpoint, '{query}' can be understood through multiple \
            analytical lenses. The foundational principles involve abstract reasoning, \
            logical deduction, and systematic categorization. This theoretical framework \
            provides the conceptual scaffolding necessary for deeper investigation."
        )
    }

    fn generate_empirical_analysis(&self, query: &str) -> String {
        format!(
            "Empirical investigation of '{query}' requires careful observation, controlled \
            experimentation, and statistical analysis. The measurable aspects include \
            quantifiable variables, reproducible phenomena, and verifiable predictions \
            that can be tested against real-world data."
        )
    }

    fn generate_philosophical_analysis(&self, query: &str) -> String {
        format!(
            "The philosophical dimensions of '{query}' raise fundamental questions about \
            knowledge, existence, and meaning. This involves examining epistemological \
            foundations, ontological categories, and ethical implications that shape \
            our understanding of the topic's deeper significance."
        )
    }

    fn generate_mathematical_analysis(&self, query: &str) -> String {
        format!(
            "Mathematical modeling of '{query}' employs formal systems, quantitative \
            relationships, and abstract structures. This includes differential equations, \
            statistical distributions, topological spaces, and algebraic frameworks \
            that capture the essential patterns and relationships."
        )
    }

    fn generate_computational_analysis(&self, query: &str) -> String {
        format!(
            "Computational approaches to '{query}' leverage algorithmic thinking, data \
            structures, and complexity analysis. This involves designing efficient \
            algorithms, optimizing performance characteristics, and implementing \
            scalable solutions that can handle large-scale problems."
        )
    }

    fn generate_synthesis(&self, query: &str) -> String {
        format!(
            "Synthesizing these multidisciplinary perspectives on '{query}' reveals a \
            rich tapestry of interconnected knowledge. The convergence of theoretical \
            insight, empirical evidence, philosophical reflection, mathematical rigor, \
            and computational power creates a comprehensive understanding that \
            transcends individual domains while respecting their unique contributions."
        )
    }

    fn domain_name(&self, domain: &KnowledgeDomain) -> &'static str {
        match domain {
            KnowledgeDomain::Mathematics => "Mathematical",
            KnowledgeDomain::Physics => "Physical Sciences",
            KnowledgeDomain::Chemistry => "Chemical Sciences",
            KnowledgeDomain::Biology => "Biological Sciences",
            KnowledgeDomain::ComputerScience => "Computer Science",
            KnowledgeDomain::Engineering => "Engineering",
            KnowledgeDomain::Medicine => "Medical Sciences",
            KnowledgeDomain::Psychology => "Psychological Sciences",
            KnowledgeDomain::Sociology => "Social Sciences",
            KnowledgeDomain::Economics => "Economic Sciences",
            KnowledgeDomain::Philosophy => "Philosophy",
            KnowledgeDomain::Ethics => "Ethical Studies",
            KnowledgeDomain::Art => "Arts & Aesthetics",
            KnowledgeDomain::Music => "Musical Studies",
            KnowledgeDomain::Literature => "Literary Studies",
            KnowledgeDomain::History => "Historical Studies",
            KnowledgeDomain::Geography => "Geographic Sciences",
            KnowledgeDomain::Linguistics => "Linguistic Sciences",
            KnowledgeDomain::Logic => "Logical Systems",
            KnowledgeDomain::Astronomy => "Astronomical Sciences",
            KnowledgeDomain::General => "General Knowledge",
            KnowledgeDomain::Technology => "Technology & Innovation",
            KnowledgeDomain::ArtificialIntelligence => "Artificial Intelligence",
            KnowledgeDomain::QuantumMechanics => "Quantum Mechanics",
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_responder_creation() {
        let engine = Arc::new(KnowledgeEngine::new());
        let responder = ComprehensiveResponder::new(engine);
        let response = responder.generate_comprehensive_response("test query");
        assert!(response.contains("test query"));
    }

    #[test]
    fn test_comprehensive_response_with_knowledge() {
        let engine = Arc::new(KnowledgeEngine::new());
        engine.add_knowledge(
            KnowledgeDomain::Mathematics,
            "Test Theorem".to_string(),
            "A fundamental mathematical principle".to_string(),
            vec!["algebra".to_string()],
        );

        let responder = ComprehensiveResponder::new(engine.clone());
        let response = responder.generate_comprehensive_response("Test Theorem");
        assert!(response.contains("Mathematical Perspective"));
        assert!(response.contains("fundamental mathematical principle"));
    }
}
