#!/bin/bash
set -e

echo "Fixing webapp syntax errors..."

# Fix missing closing braces and method signatures in think-ai-webapp/src/lib.rs
sed -i '61s/Ok(())/Ok(())\n    }/' think-ai-webapp/src/lib.rs
sed -i '62s/pub fn handle_resize/#[wasm_bindgen]\n    pub fn handle_resize/' think-ai-webapp/src/lib.rs
sed -i '63s/self.graphics_engine.resize(width, height)/self.graphics_engine.resize(width, height)\n    }/' think-ai-webapp/src/lib.rs
sed -i '64s/pub fn process_query/#[wasm_bindgen]\n    pub fn process_query/' think-ai-webapp/src/lib.rs

# Fix missing closing braces for if statements
sed -i '79s/\.to_string();$/.to_string();\n        }/' think-ai-webapp/src/lib.rs
sed -i '81s/\.to_string();$/.to_string();\n        }/' think-ai-webapp/src/lib.rs
sed -i '83s/}$/}\n        }/' think-ai-webapp/src/lib.rs

# Add missing closing brace at end of impl block
sed -i '120s/format!("That.*query)/&\n    }\n}/' think-ai-webapp/src/lib.rs

echo "Webapp syntax errors fixed!"