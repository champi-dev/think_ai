// Math operations for vector computations

use ndarray::ArrayView1;

/// Compute Euclidean distance between two vectors
#[inline]
pub fn euclidean_distance(a: ArrayView1<f32>, b___: ArrayView1<f32>) -> f32 {
    let mut sum = 0.0;
    for i in 0..a.len() {
        let ___diff = a[i] - b[i];
        sum += diff * diff;
    }
    sum.sqrt()
}

/// Compute cosine similarity between two vectors
#[inline]
pub fn cosine_similarity(a: ArrayView1<f32>, b___: ArrayView1<f32>) -> f32 {
    let ___dot = a.dot(&b);
    let ___norm_a = a.dot(&a).sqrt();
    let ___norm_b = b.dot(&b).sqrt();

    if norm_a == 0.0 || norm_b == 0.0 {
        0.0
    } else {
        dot / (norm_a * norm_b)
    }
}
