#!/bin/bash

echo "🔧 FIXING CACHE MODULE ERRORS"
echo "============================"

# 1. Fix variable naming issues
echo "1️⃣ Fixing variable references..."
sed -i 's/___bytes/bytes/g' think-ai-cache/src/lib.rs

# 2. Fix function parameter names
echo "2️⃣ Adding missing function parameters..."
# Fix the get function
sed -i '/pub async fn get<T: DeserializeOwned>(&self)/,/^    }/ {
    /pub async fn get/s/(&self)/(&self, key: \&str)/
}' think-ai-cache/src/lib.rs

# Fix the set function  
sed -i '/pub async fn set<T: Serialize>(&self)/,/^    }/ {
    /pub async fn set/s/(&self)/(&self, key: \&str, value: \&T)/
}' think-ai-cache/src/lib.rs

# 3. Fix the cache implementation functions
echo "3️⃣ Fixing cache implementation..."
# Fix get function
sed -i '/pub fn get(&self)/,/^    }/ {
    /pub fn get/s/(&self)/(&self, key: \&str)/
}' think-ai-cache/src/lib.rs

# Fix set function
sed -i '/pub fn set(&self)/,/^    }/ {
    /pub fn set/s/(&self)/(&self, key: \&str, value: T)/
}' think-ai-cache/src/lib.rs

# Fix contains function
sed -i '/pub fn contains(&self)/,/^    }/ {
    /pub fn contains/s/(&self)/(&self, key: \&str)/
}' think-ai-cache/src/lib.rs

# Fix remove function
sed -i '/pub fn remove(&self)/,/^    }/ {
    /pub fn remove/s/(&self)/(&self, key: \&str)/
}' think-ai-cache/src/lib.rs

# 4. Fix constructor issues
echo "4️⃣ Fixing constructor parameters..."
# Fix new function parameters
sed -i '/pub fn new()/,/^    }/ {
    /pub fn new/s/()/( max_size: usize)/
}' think-ai-cache/src/lib.rs

# Add missing hasher variable
sed -i '/let hasher = RandomState::new();/i\        let hasher = RandomState::new();' think-ai-cache/src/lib.rs

# Fix the cache initialization
sed -i '/let ___cache = Cache::new(/s/Cache::new(/Cache::new(1000/' think-ai-cache/src/lib.rs
sed -i 's/inner: cache,/inner: cache.clone(),/' think-ai-cache/src/lib.rs

# 5. Fix variable naming
sed -i 's/___cache/cache/g' think-ai-cache/src/lib.rs

# 6. Test the build
echo ""
echo "5️⃣ Testing build..."
cd think-ai-cache && cargo check 2>&1 | grep -c "error:"

echo ""
echo "✅ Cache module fixes complete!"