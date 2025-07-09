#!/bin/bash
set -e

echo "Fixing missing closing braces in consciousness_engine.rs..."

# Fix if statement at line 153
sed -i '153s/$/\n        }/' think-ai-core/src/consciousness_engine.rs

# Fix state update block around line 177
sed -i '179s|// Store in core engine for persistence|}\n        \n        // Store in core engine for persistence|' think-ai-core/src/consciousness_engine.rs

# Fix result creation around line 188
sed -i '189s|"timestamp": thought_id,|"timestamp": thought_id,\n            })\n        };|' think-ai-core/src/consciousness_engine.rs

# Fix process_thought method
sed -i '193s/Ok((thought_id, awareness))/Ok((thought_id, awareness))\n    }/' think-ai-core/src/consciousness_engine.rs

# Fix is_ethical method
sed -i '198s/return \*cached;/return *cached;\n        }/' think-ai-core/src/consciousness_engine.rs
sed -i '203s/is_ethical$/is_ethical\n    }/' think-ai-core/src/consciousness_engine.rs

# Fix recall_memory method
sed -i '214s/})/})\n    }/' think-ai-core/src/consciousness_engine.rs

# Fix associate_thoughts method - find the line that creates result
sed -i '/type.*thought_association/a\            })\n        };' think-ai-core/src/consciousness_engine.rs
sed -i '227s/Ok(())/Ok(())\n    }/' think-ai-core/src/consciousness_engine.rs

# Fix get_metrics method
sed -i '242s/}/}\n    }/' think-ai-core/src/consciousness_engine.rs

# Fix helper methods
sed -i '248s/hasher.finish()/hasher.finish()\n    }/' think-ai-core/src/consciousness_engine.rs
sed -i '254s/as u64$/as u64\n    }/' think-ai-core/src/consciousness_engine.rs
sed -i '259s/0.3 + (normalized \* 0.7)/0.3 + (normalized * 0.7)\n    }/' think-ai-core/src/consciousness_engine.rs
sed -i '264s/min.wrapping_mul(1000000007).wrapping_add(max)/min.wrapping_mul(1000000007).wrapping_add(max)\n    }/' think-ai-core/src/consciousness_engine.rs

# Fix update_metrics method
sed -i '274s/}/}\n        /' think-ai-core/src/consciousness_engine.rs
sed -i '277s/cache_hits += 1;/cache_hits += 1;\n        } else {/' think-ai-core/src/consciousness_engine.rs
sed -i '279s/$/\n        }\n    }\n}/' think-ai-core/src/consciousness_engine.rs

# Fix ConsciousnessMetrics struct
sed -i '287s/#\[cfg(test)\]/}\n\n#[cfg(test)]/' think-ai-core/src/consciousness_engine.rs

echo "Fixed all missing closing braces"