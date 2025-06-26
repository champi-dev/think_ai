use crate::{KnowledgeDomain, KnowledgeEngine};
use std::sync::Arc;

pub struct RealKnowledgeGenerator;

impl RealKnowledgeGenerator {
    pub fn populate_comprehensive_knowledge(engine: &Arc<KnowledgeEngine>) {
        // Computer Science - Programming Languages
        Self::add_programming_knowledge(engine);
        
        // Mathematics
        Self::add_mathematics_knowledge(engine);
        
        // Physics
        Self::add_physics_knowledge(engine);
        
        // Philosophy
        Self::add_philosophy_knowledge(engine);
        
        // History
        Self::add_history_knowledge(engine);
        
        // Biology
        Self::add_biology_knowledge(engine);
        
        // Art and Culture
        Self::add_art_knowledge(engine);
    }
    
    fn add_programming_knowledge(engine: &Arc<KnowledgeEngine>) {
        // JavaScript
        engine.add_knowledge(
            KnowledgeDomain::ComputerScience,
            "JavaScript".to_string(),
            "JavaScript is a high-level, interpreted programming language that enables interactive web pages. It's a dynamic, weakly typed, prototype-based language with first-class functions. JavaScript runs in browsers and on servers via Node.js, supporting event-driven, functional, and object-oriented programming paradigms.".to_string(),
            vec!["programming".to_string(), "web development".to_string(), "ECMAScript".to_string(), "Node.js".to_string()],
        );
        
        // Python
        engine.add_knowledge(
            KnowledgeDomain::ComputerScience,
            "Python".to_string(),
            "Python is a high-level, interpreted programming language known for its simplicity and readability. Created by Guido van Rossum in 1991, it emphasizes code readability with significant whitespace. Python supports multiple paradigms including procedural, object-oriented, and functional programming. It's widely used in data science, machine learning, web development, and automation.".to_string(),
            vec!["programming".to_string(), "data science".to_string(), "machine learning".to_string(), "scripting".to_string()],
        );
        
        // Rust
        engine.add_knowledge(
            KnowledgeDomain::ComputerScience,
            "Rust".to_string(),
            "Rust is a systems programming language focused on safety, speed, and concurrency. It achieves memory safety without garbage collection through its ownership system. Rust prevents data races at compile time and offers zero-cost abstractions. It's ideal for systems programming, embedded devices, web assembly, and performance-critical applications.".to_string(),
            vec!["systems programming".to_string(), "memory safety".to_string(), "ownership".to_string(), "performance".to_string()],
        );
        
        // Data Structures
        engine.add_knowledge(
            KnowledgeDomain::ComputerScience,
            "Hash Tables".to_string(),
            "Hash tables are data structures that implement associative arrays, mapping keys to values. They use a hash function to compute an index into an array of buckets. Average time complexity for search, insert, and delete is O(1). Hash tables handle collisions through chaining or open addressing. They're fundamental to databases, caches, and symbol tables.".to_string(),
            vec!["data structures".to_string(), "O(1) complexity".to_string(), "algorithms".to_string(), "key-value storage".to_string()],
        );
        
        // Algorithms
        engine.add_knowledge(
            KnowledgeDomain::ComputerScience,
            "Binary Search".to_string(),
            "Binary search is an efficient algorithm for finding items in sorted arrays. It works by repeatedly dividing the search interval in half. Time complexity is O(log n), making it much faster than linear search for large datasets. The algorithm compares the target with the middle element, eliminating half of the remaining elements with each comparison.".to_string(),
            vec!["algorithms".to_string(), "searching".to_string(), "O(log n)".to_string(), "divide and conquer".to_string()],
        );
        
        // Web Technologies
        engine.add_knowledge(
            KnowledgeDomain::ComputerScience,
            "REST API".to_string(),
            "REST (Representational State Transfer) is an architectural style for designing networked applications. It relies on stateless, client-server communication using standard HTTP methods (GET, POST, PUT, DELETE). RESTful APIs use resources identified by URIs, support multiple data formats (JSON, XML), and emphasize scalability and simplicity.".to_string(),
            vec!["web services".to_string(), "HTTP".to_string(), "API design".to_string(), "client-server".to_string()],
        );
        
        // Databases
        engine.add_knowledge(
            KnowledgeDomain::ComputerScience,
            "SQL Databases".to_string(),
            "SQL databases are relational database management systems that use Structured Query Language. They organize data in tables with rows and columns, enforcing ACID properties (Atomicity, Consistency, Isolation, Durability). Popular SQL databases include PostgreSQL, MySQL, and SQLite. They excel at complex queries, transactions, and maintaining data integrity.".to_string(),
            vec!["databases".to_string(), "ACID".to_string(), "relational model".to_string(), "transactions".to_string()],
        );
        
        // Machine Learning
        engine.add_knowledge(
            KnowledgeDomain::ComputerScience,
            "Neural Networks".to_string(),
            "Neural networks are computing systems inspired by biological neural networks. They consist of interconnected nodes (neurons) organized in layers. Through training with backpropagation, they learn to recognize patterns and make predictions. Deep neural networks with many hidden layers power modern AI applications like image recognition, natural language processing, and game playing.".to_string(),
            vec!["machine learning".to_string(), "AI".to_string(), "deep learning".to_string(), "pattern recognition".to_string()],
        );
    }
    
    fn add_mathematics_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Mathematics,
            "Calculus".to_string(),
            "Calculus is the mathematical study of continuous change. It has two major branches: differential calculus (concerning rates of change and slopes) and integral calculus (concerning accumulation and areas). Key concepts include limits, derivatives, integrals, and the fundamental theorem of calculus. Applications span physics, engineering, economics, and computer graphics.".to_string(),
            vec!["derivatives".to_string(), "integrals".to_string(), "limits".to_string(), "analysis".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Mathematics,
            "Linear Algebra".to_string(),
            "Linear algebra studies vector spaces and linear transformations between them. Core concepts include matrices, determinants, eigenvalues, and vector spaces. It's fundamental to computer graphics, machine learning, quantum mechanics, and engineering. Matrix operations enable efficient computation and solving systems of linear equations.".to_string(),
            vec!["matrices".to_string(), "vectors".to_string(), "eigenvalues".to_string(), "transformations".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Mathematics,
            "Prime Numbers".to_string(),
            "Prime numbers are natural numbers greater than 1 that have no positive divisors other than 1 and themselves. They're fundamental to number theory and cryptography. The distribution of primes follows patterns described by the prime number theorem. Famous unsolved problems include the Riemann hypothesis and twin prime conjecture.".to_string(),
            vec!["number theory".to_string(), "cryptography".to_string(), "factorization".to_string(), "mathematics".to_string()],
        );
    }
    
    fn add_physics_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Physics,
            "Quantum Mechanics".to_string(),
            "Quantum mechanics describes nature at the smallest scales of energy levels of atoms and subatomic particles. Key principles include wave-particle duality, uncertainty principle, and superposition. Quantum states are described by wave functions, and measurements cause wave function collapse. It's essential for understanding chemistry, materials science, and quantum computing.".to_string(),
            vec!["wave function".to_string(), "uncertainty principle".to_string(), "superposition".to_string(), "quantum physics".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Physics,
            "General Relativity".to_string(),
            "Einstein's general relativity describes gravity not as a force but as curvature of spacetime caused by mass and energy. It predicts phenomena like gravitational waves, black holes, and the expansion of the universe. The theory revolutionized our understanding of space, time, and gravity, replacing Newton's law of universal gravitation for extreme conditions.".to_string(),
            vec!["Einstein".to_string(), "spacetime".to_string(), "gravity".to_string(), "black holes".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Physics,
            "Thermodynamics".to_string(),
            "Thermodynamics studies heat, work, temperature, and energy. The four laws govern energy conservation, entropy increase, absolute zero, and thermal equilibrium. Key concepts include enthalpy, free energy, and phase transitions. Applications range from engines and refrigerators to chemical reactions and cosmology.".to_string(),
            vec!["entropy".to_string(), "energy".to_string(), "heat".to_string(), "statistical mechanics".to_string()],
        );
    }
    
    fn add_philosophy_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Philosophy,
            "Consciousness".to_string(),
            "Consciousness refers to subjective experience and awareness. The 'hard problem' asks how physical processes give rise to subjective experience. Theories range from materialist (consciousness emerges from brain activity) to dualist (mind and matter are separate). Key questions involve qualia, self-awareness, and whether artificial consciousness is possible.".to_string(),
            vec!["mind".to_string(), "awareness".to_string(), "qualia".to_string(), "philosophy of mind".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Philosophy,
            "Ethics".to_string(),
            "Ethics is the branch of philosophy concerning moral principles and values. Major approaches include deontology (duty-based ethics), consequentialism (outcome-based ethics), and virtue ethics (character-based ethics). Applied ethics addresses specific issues like bioethics, environmental ethics, and AI ethics. Core questions involve moral truth, free will, and justice.".to_string(),
            vec!["morality".to_string(), "values".to_string(), "justice".to_string(), "applied ethics".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Philosophy,
            "Epistemology".to_string(),
            "Epistemology studies knowledge, truth, and justified belief. It asks: What is knowledge? How is knowledge acquired? What makes beliefs justified? Key concepts include empiricism vs rationalism, skepticism, and the Gettier problem. Modern epistemology addresses scientific knowledge, testimony, and social dimensions of knowledge.".to_string(),
            vec!["knowledge".to_string(), "truth".to_string(), "justification".to_string(), "belief".to_string()],
        );
    }
    
    fn add_history_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::History,
            "Industrial Revolution".to_string(),
            "The Industrial Revolution (1760-1840) transformed manufacturing, transportation, and society. Beginning in Britain, it featured mechanization, factory systems, and steam power. Key innovations included the steam engine, railways, and textile machinery. It led to urbanization, new social classes, and eventually spread worldwide, fundamentally changing human civilization.".to_string(),
            vec!["technology".to_string(), "society".to_string(), "economics".to_string(), "modernization".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::History,
            "Renaissance".to_string(),
            "The Renaissance (14th-17th century) was a period of cultural rebirth in Europe. It featured renewed interest in classical learning, humanism, and artistic innovation. Key figures include Leonardo da Vinci, Michelangelo, and Galileo. The period saw advances in art, science, exploration, and political thought, laying foundations for the modern world.".to_string(),
            vec!["art".to_string(), "humanism".to_string(), "culture".to_string(), "Europe".to_string()],
        );
    }
    
    fn add_biology_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Biology,
            "DNA".to_string(),
            "DNA (Deoxyribonucleic acid) is the hereditary material in humans and almost all other organisms. It consists of two strands forming a double helix, with bases adenine, thymine, guanine, and cytosine. DNA stores genetic instructions for development, functioning, growth, and reproduction. The genetic code is universal across life forms.".to_string(),
            vec!["genetics".to_string(), "heredity".to_string(), "double helix".to_string(), "genetic code".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Biology,
            "Evolution".to_string(),
            "Evolution is the change in heritable characteristics of biological populations over successive generations. Natural selection, proposed by Darwin, is the primary mechanism. Evidence comes from fossils, comparative anatomy, molecular biology, and direct observation. Evolution explains the diversity of life and continues to shape all living organisms.".to_string(),
            vec!["natural selection".to_string(), "Darwin".to_string(), "adaptation".to_string(), "species".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Biology,
            "Photosynthesis".to_string(),
            "Photosynthesis is the process by which plants and other organisms convert light energy into chemical energy. It occurs in chloroplasts using chlorophyll. The process produces glucose and oxygen from carbon dioxide and water. Photosynthesis is crucial for life on Earth, producing oxygen and forming the base of most food chains.".to_string(),
            vec!["plants".to_string(), "chlorophyll".to_string(), "energy conversion".to_string(), "oxygen production".to_string()],
        );
    }
    
    fn add_art_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Art,
            "Impressionism".to_string(),
            "Impressionism was a 19th-century art movement characterized by small, visible brushstrokes, open composition, and emphasis on light and its changing qualities. Key artists include Monet, Renoir, and Degas. The movement rejected academic painting traditions, focusing on capturing momentary effects of light and color in everyday scenes.".to_string(),
            vec!["painting".to_string(), "Monet".to_string(), "light".to_string(), "19th century".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Art,
            "Abstract Art".to_string(),
            "Abstract art uses visual language of shape, form, color, and line to create compositions independent from visual references. Pioneered by artists like Kandinsky, Mondrian, and Pollock, it emerged in the early 20th century. Abstract art can be geometric or gestural, emphasizing the formal qualities of art over representational content.".to_string(),
            vec!["modern art".to_string(), "non-representational".to_string(), "20th century".to_string(), "expressionism".to_string()],
        );
    }
}