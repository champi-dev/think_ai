use std::sync::Arc;
use think_ai_knowledge::{KnowledgeEngine, KnowledgeDomain, persistence::KnowledgePersistence};

fn main() {
    println!("🚀 Direct Knowledge Training System");
    println!("===================================\n");

    let engine = Arc::new(KnowledgeEngine::new());
    
    // Train with high-quality Q&A pairs
    train_programming_qa(&engine);
    train_debugging_qa(&engine);
    train_conversational_qa(&engine);
    train_general_knowledge(&engine);
    
    // Save the knowledge
    let all_nodes = engine.get_all_nodes();
    println!("\n💾 Saving {} knowledge items...", all_nodes.len());
    
    match KnowledgePersistence::new("direct_training") {
        Ok(persistence) => {
            match persistence.save_checkpoint(&all_nodes, 1000) {
                Ok(_) => println!("✅ Knowledge saved successfully!"),
                Err(e) => println!("❌ Failed to save: {}", e),
            }
        }
        Err(e) => println!("❌ Failed to create persistence: {}", e),
    }
    
    let stats = engine.get_stats();
    println!("\n📊 Training Complete:");
    println!("   - Total Knowledge: {}", stats.total_nodes);
    println!("   - Domains: {}", stats.domain_distribution.len());
}

fn train_programming_qa(engine: &Arc<KnowledgeEngine>) {
    println!("🔧 Training Programming Q&A...");
    
    // JavaScript
    engine.add_knowledge(
        KnowledgeDomain::ComputerScience,
        "JavaScript".to_string(),
        "JavaScript is a high-level, interpreted programming language that enables interactive web pages and is an essential part of web applications. Created by Brendan Eich in 1995, it has evolved from a simple scripting language to a powerful, versatile language supporting object-oriented, imperative, and functional programming styles. Key features include dynamic typing, prototype-based object orientation, first-class functions, and closures. Modern JavaScript (ES6+) includes classes, modules, arrow functions, promises, async/await, and destructuring.".to_string(),
        vec!["programming".to_string(), "web development".to_string(), "ECMAScript".to_string()],
    );
    
    // Debugging techniques
    engine.add_knowledge(
        KnowledgeDomain::ComputerScience,
        "How to debug code".to_string(),
        "To debug code effectively: 1) Use console.log() or print statements to trace execution flow and variable values. 2) Set breakpoints in your IDE or browser DevTools to pause execution and inspect state. 3) Use the debugger statement (JavaScript) or pdb (Python) for interactive debugging. 4) Read error messages carefully - they often point to the exact line and issue. 5) Isolate the problem by commenting out code sections. 6) Use version control to compare working vs broken code. 7) Write unit tests to verify individual functions. 8) Use linting tools to catch syntax errors. 9) Check logs for runtime errors. 10) Use network inspector for API issues.".to_string(),
        vec!["debugging".to_string(), "troubleshooting".to_string(), "development".to_string()],
    );
    
    // Python
    engine.add_knowledge(
        KnowledgeDomain::ComputerScience,
        "Python".to_string(),
        "Python is a high-level, interpreted, general-purpose programming language emphasizing code readability and simplicity. Created by Guido van Rossum in 1991, it supports multiple programming paradigms including procedural, object-oriented, and functional programming. Python features dynamic typing, automatic memory management, a comprehensive standard library, and significant whitespace. It excels in data science (NumPy, Pandas, Scikit-learn), web development (Django, Flask), automation, machine learning (TensorFlow, PyTorch), and scientific computing.".to_string(),
        vec!["programming".to_string(), "data science".to_string(), "machine learning".to_string()],
    );
    
    // React
    engine.add_knowledge(
        KnowledgeDomain::ComputerScience,
        "React".to_string(),
        "React is a JavaScript library for building user interfaces, developed by Facebook. It uses a component-based architecture where UIs are built from reusable components. React introduces a virtual DOM for efficient updates, JSX syntax for writing components, and unidirectional data flow. Key concepts include props, state, lifecycle methods, hooks (useState, useEffect, useContext), and the reconciliation algorithm. React's ecosystem includes React Router for navigation, Redux/Context API for state management, and React Native for mobile development.".to_string(),
        vec!["javascript".to_string(), "frontend".to_string(), "UI library".to_string()],
    );
    
    // Git
    engine.add_knowledge(
        KnowledgeDomain::ComputerScience,
        "Git".to_string(),
        "Git is a distributed version control system created by Linus Torvalds in 2005. It tracks changes in source code during software development and enables multiple developers to work together. Key concepts include repositories, commits, branches, merging, and remote repositories. Common commands: git init (create repo), git add (stage changes), git commit (save changes), git push (upload), git pull (download), git branch (manage branches), git merge (combine branches). Git enables collaboration through platforms like GitHub, GitLab, and Bitbucket.".to_string(),
        vec!["version control".to_string(), "collaboration".to_string(), "development tools".to_string()],
    );
    
    // How to optimize code
    engine.add_knowledge(
        KnowledgeDomain::ComputerScience,
        "How to optimize code".to_string(),
        "Code optimization strategies: 1) Profile first to identify bottlenecks - don't guess, measure! 2) Use efficient data structures (HashMap for O(1) lookups, not arrays). 3) Minimize algorithmic complexity - prefer O(log n) over O(n), O(n) over O(n²). 4) Cache computed results to avoid recalculation. 5) Use lazy loading and pagination for large datasets. 6) Optimize database queries with indexes and query planning. 7) Minimize network requests by batching. 8) Use CDNs and compression for web assets. 9) Implement debouncing/throttling for frequent events. 10) Consider parallel processing for CPU-intensive tasks.".to_string(),
        vec!["performance".to_string(), "optimization".to_string(), "best practices".to_string()],
    );
}

fn train_debugging_qa(engine: &Arc<KnowledgeEngine>) {
    println!("🐛 Training Debugging Knowledge...");
    
    engine.add_knowledge(
        KnowledgeDomain::ComputerScience,
        "Common JavaScript errors".to_string(),
        "Common JavaScript errors and fixes: 1) 'undefined is not a function' - check if function exists and is spelled correctly. 2) 'Cannot read property of undefined' - add null checks or optional chaining (?.). 3) 'Unexpected token' - syntax error, check brackets/parentheses. 4) 'ReferenceError: X is not defined' - variable not declared or out of scope. 5) CORS errors - configure server headers or use proxy. 6) 'Maximum call stack exceeded' - infinite recursion, add base case. 7) Promise rejections - add .catch() or try/catch with async/await.".to_string(),
        vec!["javascript".to_string(), "errors".to_string(), "debugging".to_string()],
    );
    
    engine.add_knowledge(
        KnowledgeDomain::ComputerScience,
        "Memory leak debugging".to_string(),
        "To debug memory leaks: 1) Use browser DevTools Memory Profiler to take heap snapshots. 2) Look for detached DOM nodes and event listeners. 3) Check for circular references in closures. 4) Remove event listeners when components unmount. 5) Clear intervals/timeouts properly. 6) Avoid storing large data in closures. 7) Use WeakMap/WeakSet for object references. 8) In Node.js, use --inspect flag and Chrome DevTools. 9) Monitor memory usage over time. 10) Use tools like heapdump for Node.js applications.".to_string(),
        vec!["memory management".to_string(), "performance".to_string(), "debugging".to_string()],
    );
}

fn train_conversational_qa(engine: &Arc<KnowledgeEngine>) {
    println!("💬 Training Conversational Responses...");
    
    engine.add_knowledge(
        KnowledgeDomain::Philosophy,
        "greeting response".to_string(),
        "Hello! I'm Think AI, equipped with comprehensive knowledge across programming, science, mathematics, philosophy, and more. I'm here to provide helpful, accurate, and actionable answers to your questions. Whether you need debugging help, want to understand a concept, or explore ideas, I'm ready to assist. What would you like to know today?".to_string(),
        vec!["greeting".to_string(), "introduction".to_string(), "hello".to_string()],
    );
    
    engine.add_knowledge(
        KnowledgeDomain::Philosophy,
        "capabilities".to_string(),
        "I can help you with: Programming (debugging, optimization, best practices), Computer Science (algorithms, data structures, system design), Web Development (frontend, backend, databases), Science (physics, chemistry, biology), Mathematics (calculus, algebra, statistics), Machine Learning & AI, Philosophy & Ethics, History & Culture, and much more. I provide detailed explanations, practical examples, step-by-step guides, and actionable solutions tailored to your needs.".to_string(),
        vec!["help".to_string(), "capabilities".to_string(), "what can you do".to_string()],
    );
}

fn train_general_knowledge(engine: &Arc<KnowledgeEngine>) {
    println!("🌍 Training General Knowledge...");
    
    // Science
    engine.add_knowledge(
        KnowledgeDomain::Physics,
        "quantum mechanics".to_string(),
        "Quantum mechanics is the fundamental theory describing nature at the smallest scales. Key principles include: 1) Wave-particle duality - particles exhibit both wave and particle properties. 2) Uncertainty principle - position and momentum cannot both be precisely known. 3) Superposition - particles exist in multiple states until observed. 4) Entanglement - particles can be correlated regardless of distance. 5) Wave function collapse - observation determines the state. Applications include quantum computing, cryptography, and advanced materials. Famous experiments: double-slit, Schrödinger's cat, Bell's theorem.".to_string(),
        vec!["physics".to_string(), "quantum".to_string(), "science".to_string()],
    );
    
    // Philosophy
    engine.add_knowledge(
        KnowledgeDomain::Philosophy,
        "consciousness".to_string(),
        "Consciousness is the state of being aware of and able to think about one's existence, sensations, thoughts, and surroundings. Major theories include: 1) Dualism - mind and body are separate (Descartes). 2) Materialism - consciousness emerges from physical processes. 3) Panpsychism - consciousness is a fundamental property of matter. 4) Integrated Information Theory - consciousness corresponds to integrated information. The 'hard problem' asks how subjective experience arises from objective processes. Related concepts: qualia, self-awareness, theory of mind, neural correlates of consciousness.".to_string(),
        vec!["philosophy".to_string(), "mind".to_string(), "cognition".to_string()],
    );
    
    // Mathematics
    engine.add_knowledge(
        KnowledgeDomain::Mathematics,
        "calculus".to_string(),
        "Calculus is the mathematical study of continuous change, divided into differential and integral calculus. Differential calculus deals with rates of change and slopes (derivatives), while integral calculus deals with accumulation and areas under curves. Key concepts: limits, derivatives, integrals, fundamental theorem of calculus. Applications include physics (motion, forces), engineering (optimization), economics (marginal analysis), and machine learning (gradient descent). Created independently by Newton and Leibniz in the 17th century.".to_string(),
        vec!["mathematics".to_string(), "analysis".to_string(), "derivatives".to_string()],
    );
    
    // The Sun
    engine.add_knowledge(
        KnowledgeDomain::Astronomy,
        "What is the sun made of".to_string(),
        "The Sun is primarily composed of hydrogen (about 73% by mass) and helium (about 25% by mass), with trace amounts of heavier elements (2%) including oxygen, carbon, nitrogen, and iron. At its core, temperatures reach 15 million degrees Celsius, enabling nuclear fusion where hydrogen atoms combine to form helium, releasing enormous energy. The Sun has several layers: the core (fusion occurs), radiative zone (energy travels as photons), convection zone (hot plasma rises), photosphere (visible surface), chromosphere, and corona (outer atmosphere). This fusion process has been ongoing for 4.6 billion years and will continue for another 5 billion years.".to_string(),
        vec!["astronomy".to_string(), "sun".to_string(), "stars".to_string(), "space".to_string()],
    );
}