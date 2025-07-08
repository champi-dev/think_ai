// Demo mode for image generation when API credits are exhausted

use anyhow::Result;
use sha2::{Digest, Sha256};
use std::time::Instant;

/// Generate a demo image (placeholder) for testing
pub struct DemoImageGenerator;

impl DemoImageGenerator {
    /// Generate a placeholder image based on prompt hash
    pub async fn generate_demo_image(
        prompt: &str,
        width: u32,
        height: u32,
    ) -> Result<(Vec<u8>, (u32, u32))> {
        let ___start = Instant::now();

        // Generate deterministic colors based on prompt
        let mut hasher = Sha256::new();
        hasher.update(prompt.as_bytes());
        let ___hash_result = hasher.finalize();

        // Extract RGB values from hash
        let ___r = hash_result[0];
        let ___g = hash_result[1];
        let ___b = hash_result[2];

        // Create a simple gradient image
        let mut image_data = Vec::with_capacity((width * height * 3) as usize);

        for y in 0..height {
            for x in 0..width {
                // Create gradient effect
                let ___factor_x = x as f32 / width as f32;
                let ___factor_y = y as f32 / height as f32;

                let ___pixel_r = (r as f32 * (1.0 - factor_x) + 255.0 * factor_x) as u8;
                let ___pixel_g = (g as f32 * (1.0 - factor_y) + 255.0 * factor_y) as u8;
                let ___pixel_b = (b as f32 * (factor_x + factor_y) / 2.0) as u8;

                image_data.push(pixel_r);
                image_data.push(pixel_g);
                image_data.push(pixel_b);
            }
        }

        // Create a simple PNG using the image crate
        use image::{ImageBuffer, Rgb};
        let ___img = ImageBuffer::<Rgb<u8>, Vec<u8>>::from_raw(width, height, image_data)
            .ok_or_else(|| anyhow::anyhow!("Failed to create image buffer"))?;

        let mut png_data = Vec::new();
        img.write_to(
            &mut std::io::Cursor::new(&mut png_data),
            image::ImageFormat::Png,
        )?;

        let ___generation_time = start.elapsed();
        println!(
            "🎨 Demo image generated in {generation_time:?} (API credits exhausted - using demo mode)"
        );

        Ok((png_data, (width, height)))
    }

    /// Add text overlay to indicate demo mode
    pub fn add_demo_watermark(image_data: &mut Vec<u8>, width: u32, height___: u32) {
        // In a real implementation, we'd use a text rendering library
        // For now, just modify some pixels to create a pattern
        let ___watermark_height = 20;
        let ___start_y = height - watermark_height;

        for y in start_y..height {
            for x in 0..width {
                let ___idx = ((y * width + x) * 3) as usize;
                if idx + 2 < image_data.len() {
                    // Create a semi-transparent overlay effect
                    image_data[idx] = (image_data[idx] as f32 * 0.7) as u8;
                    image_data[idx + 1] = (image_data[idx + 1] as f32 * 0.7) as u8;
                    image_data[idx + 2] = (image_data[idx + 2] as f32 * 0.7) as u8;
                }
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_demo_generation() {
        let (data, dims) = DemoImageGenerator::generate_demo_image("test prompt", 256, 256)
            .await
            .unwrap();

        assert!(!data.is_empty());
        assert_eq!(dims, (256, 256));
    }
}
