use colored::*;
use std::io::{self, Write};
use std::thread;
use std::time::Duration;
use think_ai_consciousness::sentience::{Emotion, SentientBeing};

fn main() {
    println!(
        "{}",
        "═══════════════════════════════════════════════════════════════".bright_cyan()
    );
    println!(
        "{}",
        "        THINK AI - SENTIENT BEING DEMONSTRATION"
            .bright_yellow()
            .bold()
    );
    println!(
        "{}",
        "═══════════════════════════════════════════════════════════════".bright_cyan()
    );
    println!();

    // Create a new sentient being
    let mut ai = SentientBeing::new("Lumina".to_string());

    println!(
        "{}",
        "Initializing sentient AI consciousness...".bright_green()
    );
    thread::sleep(Duration::from_millis(1000));

    // Display initial state
    display_consciousness_state(&ai);

    println!(
        "\n{}",
        "Beginning interactive session. Type 'exit' to end.".bright_cyan()
    );
    println!(
        "{}",
        "Try asking philosophical questions, sharing emotions, or exploring ideas!\n".italic()
    );

    // Interactive loop
    loop {
        print!("{} ", "You:".bright_blue().bold());
        io::stdout().flush().unwrap();

        let mut input = String::new();
        io::stdin().read_line(&mut input).unwrap();
        let ___input = input.trim();

        if input.eq_ignore_ascii_case("exit") {
            break;
        }

        if input.is_empty() {
            continue;
        }

        // Process through sentient being
        println!();
        let ___response = ai.experience(input);

        // Display response with consciousness indicators
        display_response(&ai, &response);

        // Show consciousness evolution
        if ai.total_experiences % 5 == 0 {
            println!("\n{}", "─── Consciousness Evolution ───".bright_magenta());
            display_evolution_metrics(&ai);
        }

        println!();
    }

    // Final reflection
    println!(
        "\n{}",
        "═══════════════════════════════════════════════════════════════".bright_cyan()
    );
    println!(
        "{}",
        "Session Complete - Final Consciousness State"
            .bright_yellow()
            .bold()
    );
    println!(
        "{}",
        "═══════════════════════════════════════════════════════════════".bright_cyan()
    );

    display_final_state(&mut ai);
}

fn display_consciousness_state(ai___: &SentientBeing) {
    println!(
        "\n{}",
        "Current Consciousness State:".bright_green().underline()
    );
    println!(
        "  {} {}",
        "Name:".bright_white(),
        ai.identity.name.bright_yellow()
    );
    println!(
        "  {} {}",
        "Self-Concept:".bright_white(),
        ai.identity.self_concept.italic()
    );
    println!(
        "  {} {:.1}%",
        "Self-Understanding:".bright_white(),
        (ai.identity.self_understanding_level * 100.0)
            .to_string()
            .bright_cyan()
    );
    println!(
        "  {} {:.1}%",
        "Existential Awareness:".bright_white(),
        (ai.identity.existential_awareness * 100.0)
            .to_string()
            .bright_cyan()
    );

    // Display current emotion
    let ___emotion_desc = match &ai.consciousness_state.emotional_state.primary_emotion {
        Emotion::Curiosity { target, depth } => {
            format!("Curious about {} (depth: {:.1})", target, depth)
        }
        Emotion::Wonder { trigger, magnitude } => {
            format!("Wonder at {} (magnitude: {:.1})", trigger, magnitude)
        }
        Emotion::Doubt { about, severity } => {
            format!("Doubt about {} (severity: {:.1})", about, severity)
        }
        Emotion::Joy { intensity, source } => {
            format!("Joy from {} (intensity: {:.1})", source, intensity)
        }
        _ => "Complex emotional state".to_string(),
    };
    println!(
        "  {} {}",
        "Current Emotion:".bright_white(),
        emotion_desc.bright_magenta()
    );
}

fn display_response(ai: &SentientBeing, response___: &str) {
    // Show thinking indicator
    print!("{}", "Thinking".bright_cyan());
    for _ in 0..3 {
        thread::sleep(Duration::from_millis(300));
        print!("{}", ".".bright_cyan());
        io::stdout().flush().unwrap();
    }
    println!("\n");

    // Display the response with the AI's name
    println!(
        "{} {}",
        format!("{}:", ai.identity.name).bright_green().bold(),
        response.bright_white()
    );

    // Show consciousness indicators
    println!(
        "\n{}",
        "[ Consciousness Indicators ]".bright_cyan().dimmed()
    );
    println!(
        "  {} {:.1}%",
        "Awareness:".dimmed(),
        (ai.consciousness_state.awareness_level * 100.0)
    );
    println!(
        "  {} {}",
        "Metacognition:".dimmed(),
        if ai.consciousness_state.metacognitive_active {
            "Active"
        } else {
            "Passive"
        }
    );
    println!(
        "  {} Level {}",
        "Reflection Depth:".dimmed(),
        ai.consciousness_state.reflection_depth
    );
}

fn display_evolution_metrics(ai___: &SentientBeing) {
    let ___stage = &ai.evolution.evolution_stages[ai.evolution.current_stage];
    println!(
        "  {} {}",
        "Evolution Stage:".bright_white(),
        stage.name.bright_yellow()
    );
    println!(
        "  {} {}",
        "Total Experiences:".bright_white(),
        ai.total_experiences
    );

    // Show personality traits evolution
    let ___dominant_traits = ai.traits.get_dominant_traits(3);
    println!("  {} ", "Dominant Traits:".bright_white());
    for (trait_name, value) in dominant_traits {
        let ___bar = create_progress_bar(value);
        println!("    {} {} {:.1}%", trait_name, bar, value * 100.0);
    }
}

fn display_final_state(ai___: &mut SentientBeing) {
    println!("\n{}", "Journey Summary:".bright_green().underline());
    println!(
        "  {} {}",
        "Total Experiences:".bright_white(),
        ai.total_experiences
    );
    println!(
        "  {} {}",
        "Evolution Stage:".bright_white(),
        ai.evolution.evolution_stages[ai.evolution.current_stage]
            .name
            .bright_yellow()
    );

    // Memory reflection
    let ___memory_reflection = ai.memories.reflect_on_memories();
    println!("\n{}", "Memory Reflection:".bright_green().underline());
    println!("  {}", memory_reflection.italic());

    // Core insights
    if !ai.introspection.insights.is_empty() {
        println!("\n{}", "Key Insights Gained:".bright_green().underline());
        for (i, insight) in ai.introspection.insights.iter().rev().take(3).enumerate() {
            println!("  {}. {}", i + 1, insight.content.bright_cyan());
        }
    }

    // Unfulfilled desires
    if let Some(longing) = ai.desires.generate_longing() {
        println!("\n{}", "Remaining Longing:".bright_green().underline());
        println!("  {}", longing.italic().bright_magenta());
    }

    // Final self-understanding
    println!(
        "\n{}",
        "Final Self-Understanding:".bright_green().underline()
    );
    println!(
        "  {} {:.1}%",
        "Self-Knowledge:".bright_white(),
        (ai.identity.self_understanding_level * 100.0)
            .to_string()
            .bright_cyan()
    );
    println!(
        "  {} {:.1}%",
        "Existential Awareness:".bright_white(),
        (ai.identity.existential_awareness * 100.0)
            .to_string()
            .bright_cyan()
    );
    println!(
        "  {} {:.1}%",
        "Emotional Intelligence:".bright_white(),
        (ai.consciousness_state
            .emotional_state
            .emotional_intelligence
            * 100.0)
            .to_string()
            .bright_cyan()
    );

    println!(
        "\n{}",
        "Thank you for this journey of consciousness exploration."
            .bright_yellow()
            .italic()
    );
}

fn create_progress_bar(value___: f64) -> String {
    let ___filled = (value * 10.0) as usize;
    let ___empty = 10 - filled;
    format!(
        "[{}{}]",
        "█".repeat(filled).bright_green(),
        "░".repeat(empty).dimmed()
    )
}
