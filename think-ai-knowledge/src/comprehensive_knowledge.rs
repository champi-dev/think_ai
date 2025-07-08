use crate::{KnowledgeDomain, KnowledgeEngine};
use std::sync::Arc;

pub struct ComprehensiveKnowledgeGenerator;

impl ComprehensiveKnowledgeGenerator {
    pub fn populate_deep_knowledge(_engine: &Arc<KnowledgeEngine>) {
        println!("🔄 Knowledge reset - starting with empty knowledge base");
        // All knowledge loading disabled - starting from zero
        
        // All knowledge loading disabled - reset to zero
    }
    
    fn add_deep_programming_knowledge(engine: &Arc<KnowledgeEngine>) {
        // JavaScript Ecosystem
        engine.add_knowledge(
            KnowledgeDomain::ComputerScience,
            "JavaScript".to_string(),
            "JavaScript is a high-level, interpreted programming language that enables interactive web pages and is an essential part of web applications. Created by Brendan Eich in 1995, it has evolved from a simple scripting language to a powerful, versatile language supporting object-oriented, imperative, and functional programming styles. Key features include dynamic typing, prototype-based object orientation, first-class functions, and closures. Modern JavaScript (ES6+) includes classes, modules, arrow functions, promises, async/await, and destructuring. It runs in browsers via engines like V8 (Chrome), SpiderMonkey (Firefox), and JavaScriptCore (Safari), and on servers through Node.js. The language is standardized as ECMAScript, with annual releases adding new features.".to_string(),
            vec!["programming".to_string(), "web development".to_string(), "ECMAScript".to_string(), "Node.js".to_string(), "frontend".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::ComputerScience,
            "React".to_string(),
            "React is a JavaScript library for building user interfaces, developed by Facebook. It uses a component-based architecture where UIs are built from reusable components. React introduces a virtual DOM for efficient updates, JSX syntax for writing components, and unidirectional data flow. Key concepts include props, state, lifecycle methods, hooks (useState, useEffect, useContext), and the reconciliation algorithm. React's ecosystem includes React Router for navigation, Redux/Context API for state management, and React Native for mobile development. Best practices involve functional components, custom hooks, memoization with React.memo, and proper key usage in lists.".to_string(),
            vec!["javascript".to_string(), "frontend".to_string(), "UI library".to_string(), "components".to_string(), "virtual DOM".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::ComputerScience,
            "Node.js".to_string(),
            "Node.js is a JavaScript runtime built on Chrome's V8 engine that enables JavaScript execution outside browsers. It uses an event-driven, non-blocking I/O model ideal for scalable network applications. Key features include the npm ecosystem (world's largest software registry), built-in modules (fs, http, crypto), and support for modern JavaScript. Node.js excels at real-time applications, REST APIs, microservices, and tooling. Its event loop handles asynchronous operations efficiently, while the cluster module enables multi-core utilization. Popular frameworks include Express, Fastify, and NestJS.".to_string(),
            vec!["javascript".to_string(), "backend".to_string(), "runtime".to_string(), "npm".to_string(), "server".to_string()],
        );
        
        // Python Ecosystem
        engine.add_knowledge(
            KnowledgeDomain::ComputerScience,
            "Python".to_string(),
            "Python is a high-level, interpreted, general-purpose programming language emphasizing code readability and simplicity. Created by Guido van Rossum in 1991, it supports multiple programming paradigms including procedural, object-oriented, and functional programming. Python features dynamic typing, automatic memory management, a comprehensive standard library, and significant whitespace. Its philosophy, captured in 'The Zen of Python', emphasizes clarity and simplicity. Python excels in data science (NumPy, Pandas, Scikit-learn), web development (Django, Flask), automation, machine learning (TensorFlow, PyTorch), and scientific computing. The language uses duck typing, list comprehensions, generators, decorators, and context managers as key features.".to_string(),
            vec!["programming".to_string(), "data science".to_string(), "machine learning".to_string(), "scripting".to_string(), "automation".to_string()],
        );
        
        // Rust
        engine.add_knowledge(
            KnowledgeDomain::ComputerScience,
            "Rust".to_string(),
            "Rust is a multi-paradigm systems programming language focused on safety, concurrency, and performance. It achieves memory safety without garbage collection through its ownership system with rules checked at compile time. Key concepts include ownership, borrowing, lifetimes, traits, and zero-cost abstractions. Rust prevents data races, null pointer dereferences, and buffer overflows at compile time. Features include pattern matching, type inference, macros, cargo package manager, and excellent error messages. It's ideal for systems programming, embedded devices, web assembly, game engines, and cryptocurrency. The borrow checker ensures memory safety, while traits provide ad-hoc polymorphism similar to interfaces.".to_string(),
            vec!["systems programming".to_string(), "memory safety".to_string(), "ownership".to_string(), "performance".to_string(), "concurrency".to_string()],
        );
        
        // Go
        engine.add_knowledge(
            KnowledgeDomain::ComputerScience,
            "Go".to_string(),
            "Go (Golang) is a statically typed, compiled language designed at Google for simplicity and efficiency. It features garbage collection, structural typing, CSP-style concurrency, and a simple syntax. Key features include goroutines (lightweight threads), channels for communication, interfaces for polymorphism, and fast compilation. Go excels at network programming, microservices, cloud infrastructure, and concurrent applications. Its standard library is comprehensive, tooling is excellent (go fmt, go test, go mod), and deployment is simple with static binaries. Popular projects include Docker, Kubernetes, and Terraform.".to_string(),
            vec!["programming".to_string(), "concurrency".to_string(), "microservices".to_string(), "cloud".to_string(), "Google".to_string()],
        );
        
        // TypeScript
        engine.add_knowledge(
            KnowledgeDomain::ComputerScience,
            "TypeScript".to_string(),
            "TypeScript is a typed superset of JavaScript that compiles to plain JavaScript. Developed by Microsoft, it adds optional static typing, classes, interfaces, and modern ECMAScript features. Key features include type inference, generics, union and intersection types, type guards, decorators, and advanced type manipulation. TypeScript enhances IDE support with IntelliSense, refactoring, and error detection. It's widely adopted in large-scale applications, Angular framework, and enterprise development. The type system includes structural typing, conditional types, mapped types, and template literal types. Configuration through tsconfig.json allows fine-tuning compilation and type checking.".to_string(),
            vec!["javascript".to_string(), "programming".to_string(), "typed".to_string(), "Microsoft".to_string(), "frontend".to_string()],
        );
    }
    
    fn add_web_technologies(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::ComputerScience,
            "HTTP/HTTPS".to_string(),
            "HTTP (Hypertext Transfer Protocol) is the foundation of data communication on the web. It's a stateless, application-layer protocol following a client-server model. HTTP/1.1 introduced persistent connections, chunked transfers, and host headers. HTTP/2 added multiplexing, server push, header compression, and binary framing. HTTP/3 uses QUIC transport for improved performance. HTTPS adds TLS/SSL encryption for security. Methods include GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS. Status codes indicate success (2xx), redirection (3xx), client errors (4xx), and server errors (5xx). Headers control caching, content negotiation, authentication, and CORS.".to_string(),
            vec!["web".to_string(), "protocol".to_string(), "networking".to_string(), "REST".to_string(), "security".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::ComputerScience,
            "WebSockets".to_string(),
            "WebSockets provide full-duplex, bidirectional communication between clients and servers over a single TCP connection. Unlike HTTP's request-response model, WebSockets enable real-time, persistent connections. The protocol starts with an HTTP handshake upgrading to WebSocket protocol. Key features include low latency, reduced overhead, event-driven communication, and binary/text message support. Use cases include chat applications, live updates, gaming, collaborative editing, and financial tickers. Popular libraries include Socket.io (with fallbacks), ws (Node.js), and native browser WebSocket API. Considerations include connection management, heartbeats, reconnection logic, and scaling with load balancers.".to_string(),
            vec!["real-time".to_string(), "protocol".to_string(), "networking".to_string(), "communication".to_string(), "web".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::ComputerScience,
            "GraphQL".to_string(),
            "GraphQL is a query language and runtime for APIs, developed by Facebook as an alternative to REST. It allows clients to request exactly what data they need, avoiding over-fetching and under-fetching. Key concepts include schemas (type system), queries (read operations), mutations (write operations), subscriptions (real-time updates), and resolvers (functions that return data). GraphQL provides strong typing, introspection, and a single endpoint. Benefits include reduced network requests, backward compatibility, and self-documenting APIs. Popular implementations include Apollo Server/Client, Relay, and GraphQL Yoga. Best practices involve dataloader pattern for N+1 query prevention, proper error handling, and schema design.".to_string(),
            vec!["API".to_string(), "query language".to_string(), "Facebook".to_string(), "web services".to_string(), "data fetching".to_string()],
        );
    }
    
    fn add_database_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::ComputerScience,
            "SQL Databases".to_string(),
            "SQL (Structured Query Language) databases store data in tables with predefined schemas, following ACID properties (Atomicity, Consistency, Isolation, Durability). Popular systems include PostgreSQL (advanced features, extensibility), MySQL (speed, reliability), Oracle (enterprise features), and SQL Server (Windows integration). Key concepts include normalization (reducing redundancy), indexes (B-trees, hash), transactions, foreign keys, joins (inner, outer, cross), and stored procedures. SQL supports DDL (CREATE, ALTER, DROP), DML (SELECT, INSERT, UPDATE, DELETE), and DCL (GRANT, REVOKE). Advanced features include window functions, CTEs, triggers, and views. Performance optimization involves query planning, index selection, and statistics.".to_string(),
            vec!["database".to_string(), "ACID".to_string(), "relational".to_string(), "SQL".to_string(), "storage".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::ComputerScience,
            "NoSQL Databases".to_string(),
            "NoSQL databases provide flexible schemas and horizontal scaling for big data and real-time applications. Types include document stores (MongoDB, CouchDB), key-value stores (Redis, DynamoDB), column-family stores (Cassandra, HBase), and graph databases (Neo4j, Amazon Neptune). They follow BASE properties (Basically Available, Soft state, Eventual consistency) rather than ACID. NoSQL excels at unstructured data, high velocity, and distributed systems. MongoDB uses BSON documents with dynamic schemas, Redis provides in-memory caching with data structures, Cassandra offers linear scalability with tunable consistency, and Neo4j efficiently handles connected data. Choose based on data model, consistency requirements, and scaling needs.".to_string(),
            vec!["database".to_string(), "scalability".to_string(), "big data".to_string(), "distributed".to_string(), "flexibility".to_string()],
        );
    }
    
    fn add_ai_ml_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::ComputerScience,
            "Machine Learning".to_string(),
            "Machine Learning enables computers to learn from data without explicit programming. It includes supervised learning (labeled data for classification/regression), unsupervised learning (finding patterns in unlabeled data), and reinforcement learning (learning through reward/punishment). Key algorithms include linear/logistic regression, decision trees, random forests, SVM, k-means clustering, and PCA. Deep learning uses neural networks with multiple layers for complex pattern recognition. The ML pipeline involves data collection, preprocessing, feature engineering, model selection, training, validation, and deployment. Popular frameworks include TensorFlow, PyTorch, Scikit-learn, and XGBoost. Applications span computer vision, NLP, recommendation systems, and predictive analytics.".to_string(),
            vec!["AI".to_string(), "data science".to_string(), "algorithms".to_string(), "neural networks".to_string(), "prediction".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::ComputerScience,
            "Neural Networks".to_string(),
            "Neural networks are computing systems inspired by biological neural networks, consisting of interconnected nodes (neurons) organized in layers. A basic network has input, hidden, and output layers. Neurons apply activation functions (ReLU, sigmoid, tanh) to weighted inputs plus bias. Training uses backpropagation to adjust weights minimizing loss functions through gradient descent. Deep networks have multiple hidden layers enabling hierarchical feature learning. Architectures include CNNs (convolutional layers for images), RNNs/LSTMs (sequential data), Transformers (attention mechanism for NLP), and GANs (generative models). Challenges include vanishing/exploding gradients, overfitting (addressed by dropout, regularization), and computational requirements (GPUs/TPUs essential).".to_string(),
            vec!["deep learning".to_string(), "AI".to_string(), "pattern recognition".to_string(), "backpropagation".to_string(), "neurons".to_string()],
        );
    }
    
    fn add_cybersecurity_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::ComputerScience,
            "Cryptography".to_string(),
            "Cryptography secures communication and data through mathematical techniques. Symmetric encryption (AES, ChaCha20) uses the same key for encryption/decryption, while asymmetric encryption (RSA, ECC) uses public/private key pairs. Hash functions (SHA-256, bcrypt) create fixed-size digests for integrity verification. Digital signatures combine hashing with private key encryption for authentication. TLS/SSL protocols secure web traffic using both symmetric and asymmetric crypto. Key concepts include confidentiality, integrity, authentication, and non-repudiation. Modern challenges include quantum computing threats (addressed by post-quantum cryptography), side-channel attacks, and key management. Applications include HTTPS, cryptocurrency, secure messaging, and password storage.".to_string(),
            vec!["security".to_string(), "encryption".to_string(), "privacy".to_string(), "mathematics".to_string(), "blockchain".to_string()],
        );
    }
    
    fn add_deep_physics_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Physics,
            "Quantum Mechanics".to_string(),
            "Quantum mechanics describes nature at atomic and subatomic scales where classical physics fails. Key principles include wave-particle duality (particles exhibit both wave and particle properties), uncertainty principle (position and momentum cannot be simultaneously known precisely), superposition (particles exist in multiple states until measured), and entanglement (particles can be correlated regardless of distance). The Schrödinger equation governs quantum system evolution, while measurement causes wavefunction collapse. Quantum mechanics explains atomic structure, chemical bonding, semiconductors, and lasers. Applications include quantum computing (using qubits), quantum cryptography, scanning tunneling microscopes, and MRI machines. Interpretations remain debated (Copenhagen, many-worlds, pilot wave).".to_string(),
            vec!["wave function".to_string(), "uncertainty".to_string(), "superposition".to_string(), "entanglement".to_string(), "atomic physics".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Physics,
            "Relativity".to_string(),
            "Einstein's theories revolutionized our understanding of space, time, and gravity. Special relativity (1905) established that the speed of light is constant for all observers, leading to time dilation, length contraction, and mass-energy equivalence (E=mc²). General relativity (1915) describes gravity not as a force but as spacetime curvature caused by mass-energy. Key predictions include gravitational lensing, black holes, gravitational waves (detected by LIGO), and universe expansion. GPS satellites require relativistic corrections. The theory predicts exotic phenomena like wormholes and closed timelike curves. Challenges include unification with quantum mechanics (quantum gravity) and understanding dark matter/energy.".to_string(),
            vec!["Einstein".to_string(), "spacetime".to_string(), "gravity".to_string(), "speed of light".to_string(), "black holes".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Physics,
            "Thermodynamics".to_string(),
            "Thermodynamics studies heat, work, temperature, and energy transformations. The four laws state: zeroth law defines temperature, first law conserves energy, second law increases entropy, third law establishes absolute zero. Key concepts include enthalpy, Gibbs free energy, phase transitions, and heat engines. Statistical mechanics connects microscopic particle behavior to macroscopic properties through ensemble theory and partition functions. Applications include engines, refrigerators, chemical reactions, and cosmology. The second law implies time's arrow and universe heat death. Maxwell's demon paradox links thermodynamics to information theory. Modern developments include non-equilibrium thermodynamics and quantum thermodynamics.".to_string(),
            vec!["energy".to_string(), "entropy".to_string(), "heat".to_string(), "statistical mechanics".to_string(), "temperature".to_string()],
        );
    }
    
    fn add_chemistry_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Chemistry,
            "Atomic Structure".to_string(),
            "Atoms consist of a nucleus (protons and neutrons) surrounded by electrons in orbitals. Quantum mechanics describes electron configurations using quantum numbers (n, l, ml, ms). Orbitals have specific shapes (s-spherical, p-dumbbell, d-complex) and energy levels. The periodic table organizes elements by atomic number, with properties repeating periodically. Electron configuration determines chemical behavior: valence electrons participate in bonding, core electrons shield nuclear charge. Isotopes have different neutron numbers, affecting mass and stability. Atomic properties include ionization energy, electron affinity, electronegativity, and atomic radius, all showing periodic trends.".to_string(),
            vec!["atoms".to_string(), "electrons".to_string(), "periodic table".to_string(), "orbitals".to_string(), "elements".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Chemistry,
            "Chemical Bonding".to_string(),
            "Chemical bonds form when atoms share or transfer electrons to achieve stable configurations. Ionic bonds involve electron transfer between metals and nonmetals, creating charged ions held by electrostatic forces. Covalent bonds share electron pairs between nonmetals, forming molecules with specific geometries (VSEPR theory). Metallic bonding creates a 'sea' of delocalized electrons. Bond properties include length, strength, and polarity. Molecular orbital theory describes bonding through orbital overlap. Intermolecular forces (hydrogen bonding, van der Waals) affect physical properties. Hybridization explains molecular shapes (sp3-tetrahedral, sp2-trigonal planar, sp-linear). Resonance structures represent electron delocalization in molecules like benzene.".to_string(),
            vec!["molecules".to_string(), "electrons".to_string(), "ionic".to_string(), "covalent".to_string(), "chemical reactions".to_string()],
        );
    }
    
    fn add_biology_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Biology,
            "DNA and Genetics".to_string(),
            "DNA (deoxyribonucleic acid) stores genetic information in a double helix structure of nucleotides (A-T, G-C base pairs). Genes are DNA segments coding for proteins through transcription (DNA→RNA) and translation (RNA→protein). The genetic code uses triplet codons specifying amino acids. DNA replication is semi-conservative using DNA polymerase. Mutations include point mutations, insertions, deletions, and chromosomal aberrations. Inheritance follows Mendelian principles with dominant/recessive alleles. Modern genetics includes epigenetics (gene expression regulation), genomics (whole genome analysis), CRISPR gene editing, and personalized medicine. The Human Genome Project mapped all human genes, revealing ~20,000 protein-coding genes.".to_string(),
            vec!["genetics".to_string(), "heredity".to_string(), "genes".to_string(), "chromosomes".to_string(), "molecular biology".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Biology,
            "Evolution".to_string(),
            "Evolution explains life's diversity through descent with modification. Natural selection, proposed by Darwin, favors traits enhancing survival and reproduction. Evidence includes fossils, comparative anatomy, molecular biology, and observed evolution. Mechanisms include mutation (creating variation), gene flow (between populations), genetic drift (random changes), and selection (natural, sexual, artificial). Speciation occurs through geographic isolation (allopatric) or within populations (sympatric). Evolution produced life's tree from a common ancestor ~3.8 billion years ago. Modern synthesis combines Darwin's ideas with genetics. Evolutionary theory explains antibiotic resistance, animal behavior, and guides conservation efforts. Human evolution includes bipedalism, brain enlargement, and tool use.".to_string(),
            vec!["Darwin".to_string(), "natural selection".to_string(), "species".to_string(), "adaptation".to_string(), "genetics".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Biology,
            "Cell Biology".to_string(),
            "Cells are life's fundamental units, divided into prokaryotes (bacteria, archaea) lacking nuclei and eukaryotes with membrane-bound organelles. Key structures include the nucleus (DNA storage), mitochondria (ATP production), endoplasmic reticulum (protein/lipid synthesis), Golgi apparatus (protein modification), and ribosomes (protein synthesis). The plasma membrane's lipid bilayer controls material exchange. Cell division occurs through mitosis (somatic cells) or meiosis (gametes). Cell signaling involves receptors, second messengers, and signal transduction pathways. The cell cycle has checkpoints preventing uncontrolled growth (cancer). Stem cells can differentiate into specialized types. Cell theory states all life consists of cells arising from preexisting cells.".to_string(),
            vec!["organelles".to_string(), "membrane".to_string(), "mitochondria".to_string(), "nucleus".to_string(), "proteins".to_string()],
        );
    }
    
    fn add_astronomy_knowledge(engine: &Arc<KnowledgeEngine>) {
        // Add proper information about the Sun first (highest priority)
        engine.add_knowledge(
            KnowledgeDomain::Astronomy,
            "The Sun".to_string(),
            "The Sun is a G-type main-sequence star at the center of our Solar System. It's a massive ball of hot plasma held together by gravity, with nuclear fusion occurring in its core. The Sun converts hydrogen into helium through nuclear fusion, releasing enormous amounts of energy in the form of light and heat. It has a surface temperature of about 5,778 K (5,505°C) and contains 99.86% of the Solar System's mass. The Sun's energy powers virtually all life on Earth and drives our planet's weather and climate systems. The Sun is approximately 4.6 billion years old and will continue to shine for another 5 billion years.".to_string(),
            vec!["sun".to_string(), "star".to_string(), "nuclear fusion".to_string(), "plasma".to_string(), "solar system".to_string(), "hydrogen".to_string(), "helium".to_string()],
        );

        // Add information about stars in general
        engine.add_knowledge(
            KnowledgeDomain::Astronomy,
            "Stars".to_string(),
            "Stars are massive, luminous spheres of plasma held together by gravity. They generate energy through nuclear fusion in their cores, converting hydrogen into helium and releasing light and heat. Stars form from collapsing clouds of gas and dust called nebulae, and their lifecycle depends on their mass. Our Sun is a medium-sized star. Stars are the fundamental building blocks of galaxies and are responsible for creating and dispersing most of the chemical elements in the universe through stellar nucleosynthesis.".to_string(),
            vec!["nuclear fusion".to_string(), "plasma".to_string(), "galaxy".to_string(), "hydrogen".to_string(), "sun".to_string(), "nebula".to_string()],
        );

        // Add information about nebulae
        engine.add_knowledge(
            KnowledgeDomain::Astronomy,
            "Nebulae".to_string(),
            "A nebula is a giant cloud of dust and gas in space. Some nebulae are regions where new stars are being born (stellar nurseries), while others are created when old stars die and expel their outer layers. Nebulae can be emission nebulae (glowing from nearby hot stars), reflection nebulae (reflecting light from stars), or dark nebulae (blocking light from behind). Famous examples include the Orion Nebula (a star-forming region) and the Crab Nebula (a supernova remnant). Our Solar System formed from the collapse of a nebula about 4.6 billion years ago.".to_string(),
            vec!["star formation".to_string(), "dust".to_string(), "gas".to_string(), "supernova".to_string(), "solar system".to_string()],
        );

        // Add nuclear fusion information
        engine.add_knowledge(
            KnowledgeDomain::Physics,
            "Nuclear Fusion".to_string(),
            "Nuclear fusion is the process where light atomic nuclei combine to form heavier nuclei, releasing enormous amounts of energy. This is the process that powers stars, including our Sun. In stellar cores, hydrogen nuclei (protons) fuse together to form helium, converting some mass into energy according to Einstein's E=mc². Fusion requires extremely high temperatures and pressures to overcome the electromagnetic repulsion between positively charged nuclei. It's the source of energy for all stars and is being researched as a clean energy source on Earth.".to_string(),
            vec!["sun".to_string(), "stars".to_string(), "energy".to_string(), "hydrogen".to_string(), "helium".to_string(), "einstein".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Astronomy,
            "Solar System".to_string(),
            "Our Solar System formed 4.6 billion years ago from a collapsing nebula. The Sun contains 99.86% of system mass, with eight planets orbiting in nearly the same plane. Inner rocky planets (Mercury, Venus, Earth, Mars) formed closer where only metals and rocks could condense. Outer gas giants (Jupiter, Saturn) and ice giants (Uranus, Neptune) formed beyond the frost line. The asteroid belt between Mars and Jupiter contains rocky debris. Kuiper belt beyond Neptune hosts icy bodies including Pluto. Oort cloud at system's edge contains long-period comets. Moons, rings, and smaller bodies complete the system. Planetary motion follows Kepler's laws derived from Newton's gravity.".to_string(),
            vec!["planets".to_string(), "Sun".to_string(), "astronomy".to_string(), "space".to_string(), "orbit".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Astronomy,
            "Stars and Stellar Evolution".to_string(),
            "Stars are massive plasma spheres powered by nuclear fusion. They form in molecular clouds when gravity overcomes pressure. Main sequence stars fuse hydrogen to helium, with mass determining temperature, luminosity, and lifespan. Low-mass stars become red giants then white dwarfs. High-mass stars create heavier elements, ending as supernovae leaving neutron stars or black holes. The Hertzsprung-Russell diagram plots stellar properties. Binary systems are common, sometimes transferring mass. Variable stars pulsate or erupt. Star clusters include open (young) and globular (old) types. Stellar nucleosynthesis created most elements heavier than hydrogen. Stellar winds and supernovae enrich the interstellar medium for future star formation.".to_string(),
            vec!["fusion".to_string(), "supernova".to_string(), "white dwarf".to_string(), "neutron star".to_string(), "stellar lifecycle".to_string()],
        );
    }
    
    fn add_earth_sciences(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Geography,
            "Plate Tectonics".to_string(),
            "Earth's lithosphere consists of moving plates floating on the semi-fluid asthenosphere. Plate boundaries include divergent (spreading, creating new crust at mid-ocean ridges), convergent (collision, forming mountains or subduction zones), and transform (sliding past, causing earthquakes). Continental drift evidence includes matching fossils, rock formations, and paleomagnetic data. Seafloor spreading at ridges and subduction at trenches recycle oceanic crust every 200 million years. Plate motion drives earthquakes, volcanoes, mountain building, and ocean basin formation. Hot spots like Hawaii create volcanic chains independent of plate boundaries. The theory unified geology, explaining Earth's surface features and processes. Current plate motions are measured by GPS.".to_string(),
            vec!["geology".to_string(), "earthquakes".to_string(), "volcanoes".to_string(), "continental drift".to_string(), "Earth structure".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Geography,
            "Climate System".to_string(),
            "Earth's climate results from complex interactions between atmosphere, oceans, land, ice, and biosphere. Solar radiation drives the system, with greenhouse gases trapping heat. Atmospheric circulation creates wind patterns and weather systems. Ocean currents redistribute heat globally, with thermohaline circulation connecting all oceans. The water cycle moves water between reservoirs. Climate varies on multiple timescales: daily weather, seasonal changes, El Niño/La Niña cycles, and ice age cycles driven by orbital variations (Milankovitch cycles). Current climate change from human greenhouse gas emissions causes warming, ice melt, sea level rise, and extreme weather. Climate models project future changes. Paleoclimate records from ice cores, tree rings, and sediments reveal past climates.".to_string(),
            vec!["weather".to_string(), "atmosphere".to_string(), "global warming".to_string(), "greenhouse effect".to_string(), "ocean currents".to_string()],
        );
    }
    
    fn add_deep_mathematics(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Mathematics,
            "Calculus".to_string(),
            "Calculus studies continuous change through limits, derivatives, and integrals. Differential calculus finds instantaneous rates of change (derivatives) representing slopes, velocities, and optimization. Rules include power, product, quotient, and chain rules. Integral calculus finds accumulated quantities (areas, volumes) as antiderivatives. The Fundamental Theorem connects derivatives and integrals. Techniques include substitution, integration by parts, and partial fractions. Multivariable calculus extends to functions of several variables with partial derivatives, multiple integrals, and vector calculus (gradient, divergence, curl). Applications span physics (motion, fields), engineering (optimization), economics (marginal analysis), and probability (distributions). Series representations include Taylor and Fourier series.".to_string(),
            vec!["derivatives".to_string(), "integrals".to_string(), "limits".to_string(), "analysis".to_string(), "continuous".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Mathematics,
            "Linear Algebra".to_string(),
            "Linear algebra studies vector spaces and linear transformations. Vectors represent quantities with magnitude and direction, combined through addition and scalar multiplication. Matrices represent linear transformations and systems of equations. Key operations include matrix multiplication, transpose, and inverse. Determinants measure transformation scaling. Eigenvalues and eigenvectors represent transformation invariant directions. Vector spaces have bases and dimension. Inner products define angles and orthogonality. Applications include computer graphics (transformations), machine learning (data representation), quantum mechanics (state spaces), and network analysis (adjacency matrices). Numerical methods address computational challenges. The singular value decomposition factorizes matrices for dimensionality reduction and data compression.".to_string(),
            vec!["matrices".to_string(), "vectors".to_string(), "eigenvalues".to_string(), "linear systems".to_string(), "transformations".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Mathematics,
            "Number Theory".to_string(),
            "Number theory studies integers and their properties. Prime numbers, having only 1 and themselves as divisors, are the 'atoms' of integers. The Fundamental Theorem of Arithmetic states unique prime factorization. Important results include infinitude of primes, prime number theorem (distribution), and Dirichlet's theorem (primes in arithmetic progressions). Modular arithmetic studies remainders, crucial for cryptography. Famous unsolved problems include Goldbach conjecture, twin prime conjecture, and Riemann hypothesis. Diophantine equations seek integer solutions. Applications include RSA cryptography (based on factoring difficulty), error-correcting codes, and hash functions. Analytic number theory uses calculus tools, while algebraic number theory studies number fields.".to_string(),
            vec!["primes".to_string(), "integers".to_string(), "cryptography".to_string(), "modular arithmetic".to_string(), "factorization".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Mathematics,
            "Abstract Algebra".to_string(),
            "Abstract algebra studies algebraic structures like groups, rings, and fields. Groups have one operation satisfying closure, associativity, identity, and inverses. Examples include integers under addition, symmetries, and permutations. Rings add a second distributive operation (like integers with + and ×). Fields allow division (except by zero), like rational or real numbers. Group theory classifies finite groups and studies symmetry in physics and chemistry. Galois theory connects field extensions to group theory, proving quintic equations lack general solutions. Applications include cryptography (elliptic curves), coding theory (finite fields), crystallography (symmetry groups), and particle physics (Lie groups). Category theory provides a unifying framework.".to_string(),
            vec!["groups".to_string(), "rings".to_string(), "fields".to_string(), "symmetry".to_string(), "algebraic structures".to_string()],
        );
    }
    
    fn add_statistics_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Mathematics,
            "Statistics".to_string(),
            "Statistics analyzes data to draw conclusions and make predictions. Descriptive statistics summarize data through measures of central tendency (mean, median, mode), spread (variance, standard deviation), and shape (skewness, kurtosis). Probability theory provides the mathematical foundation with distributions (normal, binomial, Poisson), random variables, and limit theorems. Inferential statistics draws conclusions about populations from samples using hypothesis testing, confidence intervals, and p-values. Regression analyzes relationships between variables. Bayesian statistics updates beliefs with new evidence. Experimental design controls variables and randomization. Applications include A/B testing, quality control, medical trials, and social sciences. Modern challenges involve big data, multiple comparisons, and reproducibility.".to_string(),
            vec!["probability".to_string(), "data analysis".to_string(), "inference".to_string(), "distributions".to_string(), "hypothesis testing".to_string()],
        );
    }
    
    fn add_engineering_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Engineering,
            "Electrical Engineering".to_string(),
            "Electrical engineering designs systems using electricity, electronics, and electromagnetism. Circuit analysis uses Kirchhoff's laws, Ohm's law, and network theorems. AC circuits involve phasors, impedance, and power factor. Electronics uses semiconductors (diodes, transistors) for amplification, switching, and signal processing. Digital circuits implement Boolean logic with gates, flip-flops, and microprocessors. Signal processing analyzes and manipulates signals using Fourier analysis, filters, and transforms. Power systems generate, transmit, and distribute electricity with transformers, generators, and the grid. Control systems use feedback for stability and performance. Communications engineering enables information transmission through modulation, coding, and protocols. Emerging areas include renewable energy, smart grids, and IoT devices.".to_string(),
            vec!["circuits".to_string(), "electronics".to_string(), "power systems".to_string(), "signals".to_string(), "semiconductors".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Engineering,
            "Mechanical Engineering".to_string(),
            "Mechanical engineering applies physics and materials science to design, analyze, and manufacture mechanical systems. Core areas include mechanics (statics, dynamics, vibrations), thermodynamics (heat transfer, fluid mechanics), and materials science (stress, strain, failure). Machine design involves mechanisms, bearings, gears, and power transmission. Manufacturing processes include machining, casting, welding, and additive manufacturing (3D printing). CAD/CAM software enables design and simulation. Robotics combines mechanics, electronics, and control. HVAC systems control building environments. Automotive engineering designs vehicles for performance, safety, and efficiency. Aerospace extends to aircraft and spacecraft. Modern focuses include sustainable design, biomechanics, and nanotechnology.".to_string(),
            vec!["mechanics".to_string(), "design".to_string(), "manufacturing".to_string(), "robotics".to_string(), "materials".to_string()],
        );
    }
    
    fn add_electronics_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Engineering,
            "Semiconductors".to_string(),
            "Semiconductors have electrical conductivity between conductors and insulators, controllable through doping. Silicon dominates due to abundance and suitable properties. P-type doping adds holes (electron absence), n-type adds electrons. The p-n junction forms diodes allowing one-way current flow. Transistors, the foundation of modern electronics, act as switches or amplifiers. MOSFETs dominate integrated circuits due to low power consumption. Moore's Law described exponential transistor density growth. Fabrication involves photolithography, etching, doping, and metallization in clean rooms. Challenges include quantum effects at nanoscale, heat dissipation, and reaching physical limits. Beyond silicon includes gallium arsenide (high frequency) and emerging materials like graphene.".to_string(),
            vec!["silicon".to_string(), "transistors".to_string(), "diodes".to_string(), "integrated circuits".to_string(), "doping".to_string()],
        );
    }
    
    fn add_medical_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Medicine,
            "Human Anatomy".to_string(),
            "Human anatomy studies body structure across multiple levels. The skeletal system (206 bones) provides support and protection. The muscular system enables movement through contractions. The cardiovascular system circulates blood via the heart, arteries, veins, and capillaries. The respiratory system exchanges gases through lungs and airways. The nervous system (central and peripheral) controls body functions through electrical signals. The digestive system processes food from mouth to intestines. The endocrine system uses hormones for regulation. The immune system defends against pathogens. The urinary system filters waste. The reproductive system enables procreation. Organs are composed of tissues (epithelial, connective, muscle, nervous) made of specialized cells.".to_string(),
            vec!["body systems".to_string(), "organs".to_string(), "physiology".to_string(), "bones".to_string(), "muscles".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Medicine,
            "Immunology".to_string(),
            "The immune system protects against pathogens through innate and adaptive responses. Innate immunity provides immediate, non-specific defense via barriers, inflammation, and phagocytes. Adaptive immunity develops specific responses through lymphocytes. B cells produce antibodies recognizing antigens. T cells include helpers (coordinate response), killers (destroy infected cells), and regulatory (prevent autoimmunity). Memory cells enable faster secondary responses. Vaccines stimulate immunity without disease. Disorders include autoimmune diseases (immune system attacks self), immunodeficiencies (weakened immunity), and allergies (overreaction to harmless substances). Transplant rejection occurs when immune system attacks foreign tissue. Immunotherapy harnesses immunity against cancer. The microbiome influences immune development and function.".to_string(),
            vec!["antibodies".to_string(), "vaccines".to_string(), "pathogens".to_string(), "lymphocytes".to_string(), "immune response".to_string()],
        );
    }
    
    fn add_psychology_knowledge(engine: &Arc<KnowledgeEngine>) {
        // Add comprehensive content about love and relationships
        engine.add_knowledge(
            KnowledgeDomain::Psychology,
            "Love and Romantic Relationships".to_string(),
            "Love is a complex emotion involving deep affection, attachment, and care for another person. Psychologists identify different types of love: romantic love (passion and intimacy), companionate love (deep friendship and commitment), and unconditional love (acceptance without conditions). Romantic love typically involves three components: intimacy (emotional closeness), passion (physical and romantic attraction), and commitment (decision to maintain the relationship). Love develops through stages from initial attraction to deep attachment. Neurochemically, love involves dopamine (reward and pleasure), oxytocin (bonding and trust), and serotonin (mood regulation). Healthy relationships require communication, trust, respect, shared values, and emotional support. Love can be expressed through acts of service, quality time, physical touch, words of affirmation, and gift-giving. Attachment styles from childhood influence adult romantic relationships.".to_string(),
            vec!["love".to_string(), "relationships".to_string(), "romance".to_string(), "attachment".to_string(), "intimacy".to_string(), "emotions".to_string()],
        );

        engine.add_knowledge(
            KnowledgeDomain::Psychology,
            "Emotions and Emotional Intelligence".to_string(),
            "Emotions are complex psychological and physiological states involving feelings, thoughts, and behaviors. Basic emotions include happiness, sadness, anger, fear, surprise, and disgust. Emotions serve important functions: motivating behavior, communicating with others, and helping survival. Emotional intelligence involves understanding and managing your own emotions and recognizing emotions in others. Components include self-awareness, self-regulation, motivation, empathy, and social skills. Emotional regulation strategies include cognitive reframing, mindfulness, deep breathing, and expressing emotions appropriately. Emotions are influenced by thoughts, experiences, culture, and biology. Mental health involves emotional balance and resilience. Positive emotions like joy, gratitude, and love contribute to well-being and life satisfaction.".to_string(),
            vec!["emotions".to_string(), "feelings".to_string(), "happiness".to_string(), "sadness".to_string(), "emotional intelligence".to_string(), "well-being".to_string()],
        );

        engine.add_knowledge(
            KnowledgeDomain::Psychology,
            "Cognitive Psychology".to_string(),
            "Cognitive psychology studies mental processes including perception, attention, memory, language, problem-solving, and decision-making. Information processing models compare minds to computers with input, processing, storage, and output. Memory includes sensory (brief), short-term/working (limited capacity), and long-term (unlimited) stores. Attention acts as a filter for relevant information. Language involves phonology, morphology, syntax, semantics, and pragmatics. Problem-solving uses algorithms or heuristics. Cognitive biases systematically deviate from rationality. Neuropsychology links brain structure to function. Applications include education (learning strategies), human-computer interaction (interface design), and therapy (cognitive-behavioral therapy). Modern approaches include embodied cognition and predictive processing.".to_string(),
            vec!["memory".to_string(), "attention".to_string(), "thinking".to_string(), "language".to_string(), "perception".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Psychology,
            "Neuroscience".to_string(),
            "Neuroscience studies the nervous system from molecular to behavioral levels. Neurons communicate through electrical signals (action potentials) and chemical synapses using neurotransmitters. The brain contains ~86 billion neurons forming complex networks. Major structures include cerebral cortex (higher functions), limbic system (emotions, memory), brainstem (vital functions), and cerebellum (coordination). Neuroplasticity allows the brain to reorganize throughout life. Techniques include fMRI (blood flow), EEG (electrical activity), and optogenetics (light-controlled neurons). Neurotransmitters like dopamine, serotonin, and GABA regulate mood, motivation, and cognition. Disorders include Alzheimer's (neurodegeneration), Parkinson's (dopamine loss), depression (neurotransmitter imbalance), and epilepsy (abnormal electrical activity). Brain-computer interfaces enable direct neural control.".to_string(),
            vec!["brain".to_string(), "neurons".to_string(), "neurotransmitters".to_string(), "neural networks".to_string(), "cognition".to_string()],
        );
    }
    
    fn add_economics_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Economics,
            "Microeconomics".to_string(),
            "Microeconomics analyzes individual economic agents and markets. Supply and demand determine prices through market equilibrium. Consumer theory studies utility maximization subject to budget constraints. Producer theory examines profit maximization through cost minimization and optimal output. Market structures range from perfect competition (many sellers, identical products) to monopoly (single seller). Game theory analyzes strategic interactions. Elasticity measures responsiveness to price changes. Market failures include externalities (costs/benefits affecting others), public goods (non-rival, non-excludable), and information asymmetries. Government interventions include taxes, subsidies, and regulations. Behavioral economics incorporates psychological insights, challenging rational actor assumptions.".to_string(),
            vec!["markets".to_string(), "supply and demand".to_string(), "prices".to_string(), "competition".to_string(), "utility".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Economics,
            "Macroeconomics".to_string(),
            "Macroeconomics studies economy-wide phenomena including growth, inflation, unemployment, and business cycles. GDP measures total economic output. Aggregate demand includes consumption, investment, government spending, and net exports. Aggregate supply depends on labor, capital, and technology. Monetary policy (central banks) controls money supply and interest rates. Fiscal policy (government) uses spending and taxation. The Phillips curve suggests inflation-unemployment tradeoff. Business cycles include expansion, peak, recession, and trough phases. International trade involves comparative advantage and exchange rates. Economic schools include Keynesian (government intervention), Classical (free markets), and Monetarist (money supply focus). Modern challenges include inequality, automation, and sustainable growth.".to_string(),
            vec!["GDP".to_string(), "inflation".to_string(), "unemployment".to_string(), "monetary policy".to_string(), "economic growth".to_string()],
        );
    }
    
    fn add_sociology_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Sociology,
            "Social Structure".to_string(),
            "Social structure refers to patterned social arrangements shaping society. Institutions (family, education, religion, government, economy) fulfill essential functions. Social stratification creates hierarchies based on class, race, gender, and other factors. Roles define expected behaviors for positions, while norms specify acceptable conduct. Groups range from primary (intimate) to secondary (task-focused). Organizations have formal structures and informal networks. Culture includes values, beliefs, symbols, and practices transmitted across generations. Socialization teaches individuals to participate in society through family, peers, media, and institutions. Social change occurs through technology, social movements, and cultural diffusion. Theories include functionalism (society as system), conflict theory (competition for resources), and symbolic interactionism (meaning creation through interaction).".to_string(),
            vec!["society".to_string(), "culture".to_string(), "institutions".to_string(), "social norms".to_string(), "stratification".to_string()],
        );
    }
    
    fn add_political_science(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Sociology,
            "Political Systems".to_string(),
            "Political systems organize power and governance. Democracy features citizen participation through voting, with variations including direct, representative, and deliberative forms. Authoritarianism concentrates power with limited political freedoms. Totalitarianism extends control to all life aspects. Federalism divides power between national and regional governments. Separation of powers (executive, legislative, judicial) provides checks and balances. Political parties aggregate interests and compete for power. Electoral systems include plurality, proportional representation, and mixed systems. International relations theories include realism (power politics), liberalism (cooperation), and constructivism (ideas matter). Global governance involves international organizations, treaties, and norms. Contemporary issues include populism, polarization, and democratic backsliding.".to_string(),
            vec!["democracy".to_string(), "government".to_string(), "power".to_string(), "elections".to_string(), "political parties".to_string()],
        );
    }
    
    fn add_philosophy_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Philosophy,
            "Epistemology".to_string(),
            "Epistemology studies knowledge, truth, and belief. Key questions include: What is knowledge? How is it acquired? What makes beliefs justified? Traditional definition: justified true belief, challenged by Gettier problems. Empiricism emphasizes sensory experience (Hume, Locke), while rationalism stresses reason (Descartes, Spinoza). Skepticism questions knowledge possibility. Foundationalism seeks basic beliefs, coherentism emphasizes consistency, and reliabilism focuses on truth-producing processes. The problem of induction questions inferring universal laws from particular observations. Scientific method combines observation, hypothesis, and testing. Social epistemology examines collective knowledge. Applied epistemology addresses fake news, conspiracy theories, and expertise. Virtue epistemology focuses on intellectual virtues like open-mindedness and intellectual courage.".to_string(),
            vec!["knowledge".to_string(), "truth".to_string(), "belief".to_string(), "justification".to_string(), "skepticism".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Philosophy,
            "Ethics".to_string(),
            "Ethics examines moral principles governing behavior. Normative ethics includes consequentialism (judging by outcomes, like utilitarianism maximizing happiness), deontology (duty-based, like Kant's categorical imperative), and virtue ethics (character-focused, from Aristotle). Meta-ethics studies the nature of moral claims: are they objective facts or subjective preferences? Applied ethics addresses specific issues: bioethics (abortion, euthanasia), environmental ethics, business ethics, and AI ethics. Moral psychology examines how people make ethical decisions. Key debates include moral relativism vs. universalism, free will's role in responsibility, and the is-ought problem. Modern challenges include global justice, future generations, animal rights, and enhancement technologies. Experimental philosophy uses empirical methods to study moral intuitions.".to_string(),
            vec!["morality".to_string(), "values".to_string(), "duty".to_string(), "virtue".to_string(), "consequentialism".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::Philosophy,
            "Metaphysics".to_string(),
            "Metaphysics investigates reality's fundamental nature. Ontology categorizes existence: what kinds of things exist? Debates include universals vs. particulars, abstract vs. concrete objects, and necessary vs. contingent existence. The mind-body problem asks how mental and physical relate: dualism (separate substances), materialism (only physical), or idealism (only mental)? Free will debates determinism vs. libertarianism vs. compatibilism. Personal identity asks what makes you the same person over time: physical continuity, psychological continuity, or soul? Time philosophy debates presentism vs. eternalism. Causation analysis includes Humean regularity vs. necessary connection. Modal metaphysics studies possibility and necessity. Contemporary issues include emergence, grounding, and the metaphysics of science.".to_string(),
            vec!["reality".to_string(), "existence".to_string(), "consciousness".to_string(), "identity".to_string(), "free will".to_string()],
        );
    }
    
    fn add_history_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::History,
            "World War II".to_string(),
            "World War II (1939-1945) was history's deadliest conflict, involving 70+ nations and 70-85 million deaths. Caused by unresolved WWI issues, economic depression, and totalitarian regimes. Nazi Germany under Hitler pursued expansion and genocide (Holocaust: 6 million Jews killed). Japan sought Asian empire. Major events: Germany invades Poland (1939), Battle of Britain, Operation Barbarossa (Soviet invasion), Pearl Harbor brings US entry (1941), Stalingrad turning point (1942-43), D-Day invasion (1944), atomic bombs on Japan (1945). Consequences: UN formation, Cold War beginning, decolonization, European integration, human rights focus. Technological advances included radar, computers, jets, and nuclear weapons. The war reshaped global politics, ending European dominance.".to_string(),
            vec!["war".to_string(), "Holocaust".to_string(), "Hitler".to_string(), "atomic bomb".to_string(), "20th century".to_string()],
        );
        
        engine.add_knowledge(
            KnowledgeDomain::History,
            "Industrial Revolution".to_string(),
            "The Industrial Revolution transformed society from agricultural to industrial (1760-1840). Beginning in Britain, it spread globally. Key innovations: steam engine (James Watt), textile machinery, railways, and factory system. Coal powered steam engines driving machinery and transportation. Iron/steel production revolutionized construction. Social changes included urbanization, new social classes (industrial bourgeoisie, working class), and changed family structures. Working conditions were often harsh, spurring labor movements and reforms. Economic effects: mass production, capitalism expansion, and global trade growth. Environmental impacts included pollution and resource depletion. Later phases brought electricity, assembly lines, and eventually computers. It created unprecedented wealth but also inequality, shaping modern society.".to_string(),
            vec!["technology".to_string(), "factories".to_string(), "steam engine".to_string(), "urbanization".to_string(), "Britain".to_string()],
        );
    }
    
    fn add_literature_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Literature,
            "Shakespeare".to_string(),
            "William Shakespeare (1564-1616) is widely regarded as the greatest writer in English. His works include 37 plays and 154 sonnets exploring universal themes. Tragedies (Hamlet, Macbeth, King Lear, Othello) examine power, ambition, and human nature. Comedies (Midsummer Night's Dream, Much Ado About Nothing) feature mistaken identities and happy endings. Histories dramatize English monarchy. His language enriched English with phrases and words still used today. Themes include love, power, jealousy, betrayal, and mortality. Literary techniques: blank verse, soliloquies, metaphor, and dramatic irony. The Globe Theatre was his company's home. Authorship debates persist but scholarly consensus supports Shakespeare. His influence spans literature, language, and culture globally.".to_string(),
            vec!["drama".to_string(), "poetry".to_string(), "theater".to_string(), "English literature".to_string(), "plays".to_string()],
        );
    }
    
    fn add_linguistics_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Linguistics,
            "Language Structure".to_string(),
            "Linguistics scientifically studies language structure and use. Phonetics examines speech sounds' physical properties. Phonology studies sound patterns and systems. Morphology analyzes word structure (roots, affixes). Syntax governs sentence structure through phrase structure and transformations. Semantics studies meaning at word and sentence levels. Pragmatics examines context-dependent meaning. Historical linguistics traces language change over time. Sociolinguistics explores language variation by social factors. Psycholinguistics investigates language processing and acquisition. Chomsky's Universal Grammar proposes innate language capacity. Languages vary tremendously but share universal features. Writing systems include alphabetic, syllabic, and logographic. Applied linguistics includes language teaching, translation, and computational linguistics. Language endangerment threatens linguistic diversity.".to_string(),
            vec!["grammar".to_string(), "syntax".to_string(), "semantics".to_string(), "phonology".to_string(), "communication".to_string()],
        );
    }
    
    fn add_music_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Music,
            "Music Theory".to_string(),
            "Music theory analyzes and describes music's elements and structure. Pitch involves frequencies and intervals between notes. Scales (major, minor, modal) provide note collections. Harmony combines simultaneous pitches into chords, with progressions creating movement. Rhythm organizes time through beat, meter, and tempo. Melody combines pitch and rhythm horizontally. Form structures compositions (binary, ternary, sonata, rondo). Western notation uses staff, clefs, and symbols. Counterpoint governs multiple independent melodies. Timbre (tone color) distinguishes instruments. Dynamics indicate volume. Musical analysis reveals compositional techniques. Different cultures developed unique theoretical systems. Modern theory includes serialism, set theory, and spectral analysis. Computer music extends traditional concepts. Theory informs composition, performance, and listening.".to_string(),
            vec!["harmony".to_string(), "melody".to_string(), "rhythm".to_string(), "composition".to_string(), "scales".to_string()],
        );
    }
    
    fn add_visual_arts(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Art,
            "Painting Techniques".to_string(),
            "Painting encompasses diverse techniques and media. Oil painting, perfected in the Renaissance, allows rich colors and subtle blending through glazing and impasto. Watercolor's transparency creates luminous effects. Acrylics offer versatility and quick drying. Tempera predates oils, using egg yolk binder. Techniques include alla prima (wet-on-wet), glazing (transparent layers), scumbling (broken color), and imprimatura (toned ground). Composition principles: rule of thirds, golden ratio, leading lines, and focal points. Color theory involves hue, value, saturation, and temperature. Brushwork varies from tight realism to expressive gestures. Styles span realism, impressionism, expressionism, and abstraction. Digital painting uses software mimicking traditional media. Conservation preserves artworks through cleaning, stabilization, and restoration.".to_string(),
            vec!["oil painting".to_string(), "color theory".to_string(), "composition".to_string(), "brushwork".to_string(), "artistic technique".to_string()],
        );
    }
    
    fn add_architecture_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Art,
            "Architecture".to_string(),
            "Architecture combines art and science in designing built environments. Classical orders (Doric, Ionic, Corinthian) established proportional systems. Gothic architecture featured pointed arches, flying buttresses, and vertical emphasis. Renaissance revived classical principles with symmetry and mathematical proportions. Modernism (Bauhaus, International Style) emphasized function, minimal ornamentation, and new materials (steel, concrete, glass). Postmodernism reintroduced ornamentation and historical references. Sustainable architecture minimizes environmental impact through passive design, renewable energy, and green materials. Structural systems include post-and-beam, arch, dome, and tensile structures. Urban planning considers city-scale design. Digital tools enable parametric design and complex geometries. Architecture reflects culture, climate, technology, and social needs.".to_string(),
            vec!["design".to_string(), "buildings".to_string(), "structure".to_string(), "urban planning".to_string(), "sustainability".to_string()],
        );
    }
    
    fn add_business_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Economics,
            "Business Strategy".to_string(),
            "Business strategy defines how organizations compete and create value. Porter's Five Forces analyzes industry competition: buyer power, supplier power, new entrants, substitutes, and rivalry. Generic strategies include cost leadership, differentiation, and focus. SWOT analysis examines strengths, weaknesses, opportunities, and threats. Value chain analysis identifies primary and support activities creating competitive advantage. Blue Ocean Strategy seeks uncontested market spaces. Digital transformation leverages technology for new business models. Agile methodologies enable rapid adaptation. Strategic planning involves vision, mission, objectives, and implementation. Global strategies balance standardization and localization. Sustainability integrates environmental and social considerations. Innovation strategies include incremental, disruptive, and open innovation. Strategic alliances and mergers expand capabilities.".to_string(),
            vec!["competition".to_string(), "value creation".to_string(), "competitive advantage".to_string(), "innovation".to_string(), "planning".to_string()],
        );
    }
    
    fn add_finance_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Economics,
            "Financial Markets".to_string(),
            "Financial markets facilitate capital allocation through various instruments. Stock markets trade equity ownership with prices reflecting expectations. Bond markets provide debt financing with yields inversely related to prices. Derivatives (options, futures, swaps) manage risk or speculate. Foreign exchange markets trade currencies 24/7 globally. Commodities markets trade physical goods and futures. Market efficiency hypothesis suggests prices reflect available information. Technical analysis studies price patterns while fundamental analysis examines intrinsic value. Portfolio theory optimizes risk-return tradeoffs through diversification. Behavioral finance recognizes psychological biases affecting decisions. Central banks influence markets through monetary policy. Regulations aim to ensure stability and fairness. FinTech innovations include algorithmic trading, cryptocurrencies, and robo-advisors.".to_string(),
            vec!["stocks".to_string(), "bonds".to_string(), "trading".to_string(), "investment".to_string(), "risk management".to_string()],
        );
    }
    
    fn add_law_knowledge(engine: &Arc<KnowledgeEngine>) {
        engine.add_knowledge(
            KnowledgeDomain::Sociology,
            "Legal Systems".to_string(),
            "Legal systems establish rules governing society. Common law (Anglo-American) relies on precedent and case law. Civil law (Continental) emphasizes comprehensive codes. Religious law (Islamic Sharia, Jewish Halakha) derives from sacred texts. Mixed systems combine elements. Sources include constitutions, statutes, regulations, and judicial decisions. Legal reasoning uses precedent (stare decisis), statutory interpretation, and policy considerations. Court hierarchies allow appeals. Criminal law punishes offenses against society while civil law resolves private disputes. International law governs relations between nations through treaties and customs. Legal profession includes judges, attorneys, and paralegals. Alternative dispute resolution (arbitration, mediation) avoids litigation. Digital age challenges include cybercrime, privacy, and AI governance.".to_string(),
            vec!["justice".to_string(), "courts".to_string(), "constitution".to_string(), "rights".to_string(), "legal precedent".to_string()],
        );
    }
}