// Fix Science Knowledge - Add proper scientific content

use think_ai_knowledge::{KnowledgeEngine, KnowledgeDomain};
use std::sync::Arc;
fn main() {
    println!("🔬 Adding proper scientific knowledge...");
    let engine = Arc::new(KnowledgeEngine::new());
    // Add proper content about the Sun
    engine.add_knowledge(
        KnowledgeDomain::Astronomy,
        "The Sun".to_string(),
        "The Sun is a G-type main-sequence star at the center of our Solar System. It's a massive ball of hot plasma held together by gravity, with nuclear fusion occurring in its core. The Sun converts hydrogen into helium through nuclear fusion, releasing enormous amounts of energy in the form of light and heat. It has a surface temperature of about 5,778 K (5,505°C) and contains 99.86% of the Solar System's mass. The Sun's energy powers virtually all life on Earth and drives our planet's weather and climate systems.".to_string(),
        vec!["star".to_string(), "nuclear fusion".to_string(), "plasma".to_string(), "solar system".to_string()],
    );
    // Add content about stars
        "Stars".to_string(),
        "Stars are massive, luminous spheres of plasma held together by gravity. They generate energy through nuclear fusion in their cores, converting hydrogen into helium and releasing light and heat. Stars form from collapsing clouds of gas and dust, and their lifecycle depends on their mass. Our Sun is a medium-sized star. Stars are the fundamental building blocks of galaxies and are responsible for creating and dispersing most of the chemical elements in the universe.".to_string(),
        vec!["nuclear fusion".to_string(), "plasma".to_string(), "galaxy".to_string(), "hydrogen".to_string()],
    // Add content about nuclear fusion
        KnowledgeDomain::Physics,
        "Nuclear Fusion".to_string(),
        "Nuclear fusion is the process where light atomic nuclei combine to form heavier nuclei, releasing enormous amounts of energy. This is the process that powers stars, including our Sun. In stellar cores, hydrogen nuclei (protons) fuse together to form helium, converting some mass into energy according to Einstein's E=mc². Fusion requires extremely high temperatures and pressures to overcome the electromagnetic repulsion between positively charged nuclei. It's the source of energy for all stars and is being researched as a clean energy source on Earth.".to_string(),
        vec!["sun".to_string(), "stars".to_string(), "energy".to_string(), "hydrogen".to_string(), "helium".to_string()],
    // Add content about nebulae
        "Nebulae".to_string(),
        "A nebula is a giant cloud of dust and gas in space. Some nebulae are regions where new stars are being born, while others are created when old stars die and expel their outer layers. Nebulae can be emission nebulae (glowing from nearby hot stars), reflection nebulae (reflecting light from stars), or dark nebulae (blocking light from behind). Famous examples include the Orion Nebula (a star-forming region) and the Crab Nebula (a supernova remnant). Our Solar System formed from the collapse of a nebula about 4.6 billion years ago.".to_string(),
        vec!["star formation".to_string(), "dust".to_string(), "gas".to_string(), "supernova".to_string()],
    println!("✅ Added proper scientific knowledge!");
    println!("📊 Knowledge base now contains {} items", engine.get_stats().total_nodes);
}
