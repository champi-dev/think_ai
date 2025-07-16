#!/bin/bash
set -e

echo "Removing image-gen references..."

# Comment out image routes in router
sed -i 's|\.route("/image-generator"|// .route("/image-generator"|' think-ai-http/src/router/mod.rs
sed -i 's|\.route("/images"|// .route("/images"|' think-ai-http/src/router/mod.rs
sed -i 's|"/static/image_generator.html"|// "/static/image_generator.html"|' think-ai-http/src/router/mod.rs
sed -i 's|ServeFile::new(static_dir.join("image_generator.html"))|// ServeFile::new(static_dir.join("image_generator.html"))|' think-ai-http/src/router/mod.rs

# Comment out the entire serve_image_generator function
sed -i '/^async fn serve_image_generator/,/^}$/{s/^/\/\/ /}' think-ai-http/src/router/mod.rs

# Remove image handler imports and usage
echo "// Image handler removed - no image-gen dependency" > think-ai-http/src/handlers/image.rs

# Comment out image improver in server.rs
sed -i 's/think_ai_image_gen::AIImageImprover/\/\/ think_ai_image_gen::AIImageImprover/' think-ai-http/src/server.rs

echo "Image-gen references removed!"