//! Mathematical utilities for consciousness visualization
//! 
//! Provides O(1) and O(log n) mathematical operations for 3D graphics

use nalgebra::{Vector3, Vector4, Matrix4, Point3, Quaternion, UnitQuaternion};

/// O(1) 3D transformation utilities
pub struct Transform3D {
    pub position: Vector3<f32>,
    pub rotation: UnitQuaternion<f32>,
    pub scale: Vector3<f32>,
    cached_matrix: Option<Matrix4<f32>>,
    is_dirty: bool,
}

impl Transform3D {
    pub fn new() -> Self {
        Self {
            position: Vector3::zeros(),
            rotation: UnitQuaternion::identity(),
            scale: Vector3::new(1.0, 1.0, 1.0),
            cached_matrix: None,
            is_dirty: true,
        }
    }

    /// O(1) transform matrix with caching
    pub fn get_matrix(&mut self) -> &Matrix4<f32> {
        if self.is_dirty || self.cached_matrix.is_none() {
            self.cached_matrix = Some(self.compute_matrix());
            self.is_dirty = false;
        }
        self.cached_matrix.as_ref().unwrap()
    }

    /// O(1) matrix computation
    fn compute_matrix(&self) -> Matrix4<f32> {
        let translation = Matrix4::new_translation(&self.position);
        let rotation = self.rotation.to_homogeneous();
        let scale = Matrix4::new_nonuniform_scaling(&self.scale);
        
        translation * rotation * scale
    }

    /// O(1) position update
    pub fn set_position(&mut self, pos: Vector3<f32>) {
        self.position = pos;
        self.is_dirty = true;
    }

    /// O(1) rotation update
    pub fn set_rotation(&mut self, rot: UnitQuaternion<f32>) {
        self.rotation = rot;
        self.is_dirty = true;
    }

    /// O(1) scale update
    pub fn set_scale(&mut self, scale: Vector3<f32>) {
        self.scale = scale;
        self.is_dirty = true;
    }
}

/// O(1) camera system with optimized view/projection calculations
pub struct Camera3D {
    pub position: Vector3<f32>,
    pub target: Vector3<f32>,
    pub up: Vector3<f32>,
    pub fov: f32,
    pub aspect_ratio: f32,
    pub near_plane: f32,
    pub far_plane: f32,
    cached_view_matrix: Option<Matrix4<f32>>,
    cached_projection_matrix: Option<Matrix4<f32>>,
    view_dirty: bool,
    projection_dirty: bool,
}

impl Camera3D {
    pub fn new(aspect_ratio: f32) -> Self {
        Self {
            position: Vector3::new(0.0, 0.0, 5.0),
            target: Vector3::zeros(),
            up: Vector3::y(),
            fov: 45.0_f32.to_radians(),
            aspect_ratio,
            near_plane: 0.1,
            far_plane: 1000.0,
            cached_view_matrix: None,
            cached_projection_matrix: None,
            view_dirty: true,
            projection_dirty: true,
        }
    }

    /// O(1) view matrix with caching
    pub fn get_view_matrix(&mut self) -> &Matrix4<f32> {
        if self.view_dirty || self.cached_view_matrix.is_none() {
            self.cached_view_matrix = Some(Matrix4::look_at_rh(
                &Point3::from(self.position),
                &Point3::from(self.target),
                &self.up,
            ));
            self.view_dirty = false;
        }
        self.cached_view_matrix.as_ref().unwrap()
    }

    /// O(1) projection matrix with caching
    pub fn get_projection_matrix(&mut self) -> &Matrix4<f32> {
        if self.projection_dirty || self.cached_projection_matrix.is_none() {
            self.cached_projection_matrix = Some(Matrix4::new_perspective(
                self.aspect_ratio,
                self.fov,
                self.near_plane,
                self.far_plane,
            ));
            self.projection_dirty = false;
        }
        self.cached_projection_matrix.as_ref().unwrap()
    }

    /// O(1) view-projection matrix
    pub fn get_view_projection_matrix(&mut self) -> Matrix4<f32> {
        let projection = *self.get_projection_matrix();
        let view = *self.get_view_matrix();
        projection * view
    }

    /// O(1) camera position update
    pub fn set_position(&mut self, pos: Vector3<f32>) {
        self.position = pos;
        self.view_dirty = true;
    }

    /// O(1) camera target update
    pub fn set_target(&mut self, target: Vector3<f32>) {
        self.target = target;
        self.view_dirty = true;
    }

    /// O(1) aspect ratio update
    pub fn set_aspect_ratio(&mut self, aspect: f32) {
        self.aspect_ratio = aspect;
        self.projection_dirty = true;
    }

    /// Orbit camera around target
    pub fn orbit(&mut self, horizontal_angle: f32, vertical_angle: f32, distance: f32) {
        let x = distance * vertical_angle.cos() * horizontal_angle.sin();
        let y = distance * vertical_angle.sin();
        let z = distance * vertical_angle.cos() * horizontal_angle.cos();
        
        self.set_position(self.target + Vector3::new(x, y, z));
    }
}

/// O(1) interpolation utilities
pub struct Interpolation;

impl Interpolation {
    /// O(1) linear interpolation
    pub fn lerp(a: f32, b: f32, t: f32) -> f32 {
        a + (b - a) * t
    }

    /// O(1) vector linear interpolation
    pub fn lerp_vec3(a: &Vector3<f32>, b: &Vector3<f32>, t: f32) -> Vector3<f32> {
        a + (b - a) * t
    }

    /// O(1) spherical linear interpolation for quaternions
    pub fn slerp_quat(a: &UnitQuaternion<f32>, b: &UnitQuaternion<f32>, t: f32) -> UnitQuaternion<f32> {
        a.slerp(b, t)
    }

    /// O(1) smooth step interpolation
    pub fn smooth_step(t: f32) -> f32 {
        t * t * (3.0 - 2.0 * t)
    }

    /// O(1) smoother step interpolation
    pub fn smoother_step(t: f32) -> f32 {
        t * t * t * (t * (t * 6.0 - 15.0) + 10.0)
    }

    /// O(1) ease-in-out cubic
    pub fn ease_in_out_cubic(t: f32) -> f32 {
        if t < 0.5 {
            4.0 * t * t * t
        } else {
            1.0 - (-2.0 * t + 2.0).powi(3) / 2.0
        }
    }

    /// O(1) elastic ease-out
    pub fn ease_out_elastic(t: f32) -> f32 {
        if t == 0.0 {
            0.0
        } else if t == 1.0 {
            1.0
        } else {
            2.0_f32.powf(-10.0 * t) * ((t * 10.0 - 0.75) * (2.0 * std::f32::consts::PI) / 3.0).sin() + 1.0
        }
    }
}

/// O(1) 3D geometry utilities
pub struct Geometry3D;

impl Geometry3D {
    /// O(1) distance between points
    pub fn distance(a: &Vector3<f32>, b: &Vector3<f32>) -> f32 {
        (b - a).magnitude()
    }

    /// O(1) squared distance (faster when exact distance not needed)
    pub fn distance_squared(a: &Vector3<f32>, b: &Vector3<f32>) -> f32 {
        (b - a).magnitude_squared()
    }

    /// O(1) dot product
    pub fn dot(a: &Vector3<f32>, b: &Vector3<f32>) -> f32 {
        a.dot(b)
    }

    /// O(1) cross product
    pub fn cross(a: &Vector3<f32>, b: &Vector3<f32>) -> Vector3<f32> {
        a.cross(b)
    }

    /// O(1) vector normalization
    pub fn normalize(v: &Vector3<f32>) -> Vector3<f32> {
        v.normalize()
    }

    /// O(1) reflection of vector across plane normal
    pub fn reflect(incident: &Vector3<f32>, normal: &Vector3<f32>) -> Vector3<f32> {
        incident - 2.0 * normal.dot(incident) * normal
    }

    /// O(1) project vector a onto vector b
    pub fn project(a: &Vector3<f32>, b: &Vector3<f32>) -> Vector3<f32> {
        b * (a.dot(b) / b.magnitude_squared())
    }

    /// O(1) angle between vectors
    pub fn angle_between(a: &Vector3<f32>, b: &Vector3<f32>) -> f32 {
        (a.dot(b) / (a.magnitude() * b.magnitude())).acos()
    }

    /// O(1) check if point is inside sphere
    pub fn point_in_sphere(point: &Vector3<f32>, center: &Vector3<f32>, radius: f32) -> bool {
        Self::distance_squared(point, center) <= radius * radius
    }

    /// O(1) check if point is inside axis-aligned bounding box
    pub fn point_in_aabb(point: &Vector3<f32>, min: &Vector3<f32>, max: &Vector3<f32>) -> bool {
        point.x >= min.x && point.x <= max.x &&
        point.y >= min.y && point.y <= max.y &&
        point.z >= min.z && point.z <= max.z
    }
}

/// O(1) noise generation for procedural effects
pub struct Noise;

impl Noise {
    /// O(1) simple hash-based noise
    pub fn hash_noise(x: i32, y: i32, z: i32) -> f32 {
        let mut n = (x as u32).wrapping_mul(1619) ^ (y as u32).wrapping_mul(31337) ^ (z as u32).wrapping_mul(6971);
        n = n.wrapping_mul(n.wrapping_mul(n).wrapping_mul(60493));
        n = (n >> 13) ^ n;
        1.0 - ((n.wrapping_mul(n.wrapping_mul(n).wrapping_mul(15731).wrapping_add(789221)).wrapping_add(1376312589)) & 0x7fffffff) as f32 / 1073741824.0
    }

    /// O(1) 3D noise
    pub fn noise_3d(x: f32, y: f32, z: f32) -> f32 {
        let xi = x.floor() as i32;
        let yi = y.floor() as i32;
        let zi = z.floor() as i32;
        
        let xf = x - xi as f32;
        let yf = y - yi as f32;
        let zf = z - zi as f32;
        
        // Get noise values at corners of cube
        let n000 = Self::hash_noise(xi, yi, zi);
        let n001 = Self::hash_noise(xi, yi, zi + 1);
        let n010 = Self::hash_noise(xi, yi + 1, zi);
        let n011 = Self::hash_noise(xi, yi + 1, zi + 1);
        let n100 = Self::hash_noise(xi + 1, yi, zi);
        let n101 = Self::hash_noise(xi + 1, yi, zi + 1);
        let n110 = Self::hash_noise(xi + 1, yi + 1, zi);
        let n111 = Self::hash_noise(xi + 1, yi + 1, zi + 1);
        
        // Trilinear interpolation
        let nx00 = Interpolation::lerp(n000, n100, xf);
        let nx01 = Interpolation::lerp(n001, n101, xf);
        let nx10 = Interpolation::lerp(n010, n110, xf);
        let nx11 = Interpolation::lerp(n011, n111, xf);
        
        let nxy0 = Interpolation::lerp(nx00, nx10, yf);
        let nxy1 = Interpolation::lerp(nx01, nx11, yf);
        
        Interpolation::lerp(nxy0, nxy1, zf)
    }

    /// O(1) turbulence (fractal noise)
    pub fn turbulence_3d(x: f32, y: f32, z: f32, octaves: u32) -> f32 {
        let mut value = 0.0;
        let mut amplitude = 1.0;
        let mut frequency = 1.0;
        
        for _ in 0..octaves {
            value += Self::noise_3d(x * frequency, y * frequency, z * frequency) * amplitude;
            amplitude *= 0.5;
            frequency *= 2.0;
        }
        
        value
    }
}

/// O(1) color utilities
pub struct ColorMath;

impl ColorMath {
    /// O(1) HSV to RGB conversion
    pub fn hsv_to_rgb(h: f32, s: f32, v: f32) -> Vector3<f32> {
        let c = v * s;
        let x = c * (1.0 - ((h * 6.0) % 2.0 - 1.0).abs());
        let m = v - c;
        
        let (r, g, b) = match (h * 6.0) as u32 {
            0 => (c, x, 0.0),
            1 => (x, c, 0.0),
            2 => (0.0, c, x),
            3 => (0.0, x, c),
            4 => (x, 0.0, c),
            _ => (c, 0.0, x),
        };
        
        Vector3::new(r + m, g + m, b + m)
    }

    /// O(1) RGB to HSV conversion
    pub fn rgb_to_hsv(r: f32, g: f32, b: f32) -> Vector3<f32> {
        let max = r.max(g.max(b));
        let min = r.min(g.min(b));
        let delta = max - min;
        
        let h = if delta == 0.0 {
            0.0
        } else if max == r {
            60.0 * (((g - b) / delta) % 6.0)
        } else if max == g {
            60.0 * ((b - r) / delta + 2.0)
        } else {
            60.0 * ((r - g) / delta + 4.0)
        };
        
        let s = if max == 0.0 { 0.0 } else { delta / max };
        let v = max;
        
        Vector3::new(h / 360.0, s, v)
    }

    /// O(1) color interpolation in HSV space
    pub fn lerp_hsv(color1: &Vector3<f32>, color2: &Vector3<f32>, t: f32) -> Vector3<f32> {
        let hsv1 = Self::rgb_to_hsv(color1.x, color1.y, color1.z);
        let hsv2 = Self::rgb_to_hsv(color2.x, color2.y, color2.z);
        
        // Handle hue wraparound
        let mut h1 = hsv1.x;
        let mut h2 = hsv2.x;
        
        if (h2 - h1).abs() > 0.5 {
            if h2 > h1 {
                h1 += 1.0;
            } else {
                h2 += 1.0;
            }
        }
        
        let h = (Interpolation::lerp(h1, h2, t) % 1.0 + 1.0) % 1.0;
        let s = Interpolation::lerp(hsv1.y, hsv2.y, t);
        let v = Interpolation::lerp(hsv1.z, hsv2.z, t);
        
        Self::hsv_to_rgb(h, s, v)
    }

    /// O(1) gamma correction
    pub fn gamma_correct(color: &Vector3<f32>, gamma: f32) -> Vector3<f32> {
        Vector3::new(
            color.x.powf(1.0 / gamma),
            color.y.powf(1.0 / gamma),
            color.z.powf(1.0 / gamma),
        )
    }
}

/// O(log n) spatial partitioning for efficient collision detection
pub struct OctreeNode {
    pub bounds: (Vector3<f32>, Vector3<f32>), // min, max
    pub objects: Vec<usize>,
    pub children: Option<Box<[OctreeNode; 8]>>,
    pub depth: u32,
}

impl OctreeNode {
    pub fn new(min: Vector3<f32>, max: Vector3<f32>, max_depth: u32) -> Self {
        Self {
            bounds: (min, max),
            objects: Vec::new(),
            children: None,
            depth: max_depth,
        }
    }

    /// O(log n) point insertion
    pub fn insert_point(&mut self, point: Vector3<f32>, object_id: usize) {
        if self.depth == 0 || self.objects.len() < 8 {
            self.objects.push(object_id);
            return;
        }

        if self.children.is_none() {
            self.subdivide();
        }

        let center = (self.bounds.0 + self.bounds.1) * 0.5;
        let child_index = self.get_child_index(&point, &center);
        
        if let Some(ref mut children) = self.children {
            children[child_index].insert_point(point, object_id);
        }
    }

    /// O(log n) range query
    pub fn query_range(&self, min: &Vector3<f32>, max: &Vector3<f32>) -> Vec<usize> {
        let mut result = Vec::new();
        
        if !self.intersects_bounds(min, max) {
            return result;
        }
        
        for &object_id in &self.objects {
            result.push(object_id);
        }
        
        if let Some(ref children) = self.children {
            for child in children.iter() {
                result.extend(child.query_range(min, max));
            }
        }
        
        result
    }

    fn subdivide(&mut self) {
        let center = (self.bounds.0 + self.bounds.1) * 0.5;
        let min = self.bounds.0;
        let max = self.bounds.1;

        self.children = Some(Box::new([
            OctreeNode::new(Vector3::new(min.x, min.y, min.z), Vector3::new(center.x, center.y, center.z), self.depth - 1),
            OctreeNode::new(Vector3::new(center.x, min.y, min.z), Vector3::new(max.x, center.y, center.z), self.depth - 1),
            OctreeNode::new(Vector3::new(min.x, center.y, min.z), Vector3::new(center.x, max.y, center.z), self.depth - 1),
            OctreeNode::new(Vector3::new(center.x, center.y, min.z), Vector3::new(max.x, max.y, center.z), self.depth - 1),
            OctreeNode::new(Vector3::new(min.x, min.y, center.z), Vector3::new(center.x, center.y, max.z), self.depth - 1),
            OctreeNode::new(Vector3::new(center.x, min.y, center.z), Vector3::new(max.x, center.y, max.z), self.depth - 1),
            OctreeNode::new(Vector3::new(min.x, center.y, center.z), Vector3::new(center.x, max.y, max.z), self.depth - 1),
            OctreeNode::new(Vector3::new(center.x, center.y, center.z), Vector3::new(max.x, max.y, max.z), self.depth - 1),
        ]));
    }

    fn get_child_index(&self, point: &Vector3<f32>, center: &Vector3<f32>) -> usize {
        let mut index = 0;
        if point.x > center.x { index |= 1; }
        if point.y > center.y { index |= 2; }
        if point.z > center.z { index |= 4; }
        index
    }

    fn intersects_bounds(&self, min: &Vector3<f32>, max: &Vector3<f32>) -> bool {
        self.bounds.0.x <= max.x && self.bounds.1.x >= min.x &&
        self.bounds.0.y <= max.y && self.bounds.1.y >= min.y &&
        self.bounds.0.z <= max.z && self.bounds.1.z >= min.z
    }
}