pub type Matrix4 = [f32; 16];
pub type Vector3 = Vector3Struct;

#[derive(Clone, Copy, Debug)]
pub struct Vector3Struct {
    pub x: f32,
    pub y: f32,
    pub z: f32,
}

impl Vector3Struct {
    pub fn new(x: f32, y: f32, z: f32) -> Self {
        Self { x, y, z }
    }
}

pub struct Matrix4Utils;

impl Matrix4Utils {
    pub fn identity() -> Matrix4 {
        [
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0,
        ]
    }

    pub fn perspective(fovy: f32, aspect: f32, near: f32, far: f32) -> Matrix4 {
        let f = 1.0 / (fovy / 2.0).tan();
        [
            f / aspect, 0.0, 0.0, 0.0,
            0.0, f, 0.0, 0.0,
            0.0, 0.0, (far + near) / (near - far), -1.0,
            0.0, 0.0, (2.0 * far * near) / (near - far), 0.0,
        ]
    }

    pub fn look_at(eye: &Vector3Struct, center: &Vector3Struct, up: &Vector3Struct) -> Matrix4 {
        let z = Vector3Struct {
            x: eye.x - center.x,
            y: eye.y - center.y,
            z: eye.z - center.z,
        };

        let z_len = (z.x * z.x + z.y * z.y + z.z * z.z).sqrt();
        let z = Vector3Struct {
            x: z.x / z_len,
            y: z.y / z_len,
            z: z.z / z_len,
        };

        let x = Vector3Struct {
            x: up.y * z.z - up.z * z.y,
            y: up.z * z.x - up.x * z.z,
            z: up.x * z.y - up.y * z.x,
        };

        let x_len = (x.x * x.x + x.y * x.y + x.z * x.z).sqrt();
        let x = Vector3Struct {
            x: x.x / x_len,
            y: x.y / x_len,
            z: x.z / x_len,
        };

        let y = Vector3Struct {
            x: z.y * x.z - z.z * x.y,
            y: z.z * x.x - z.x * x.z,
            z: z.x * x.y - z.y * x.x,
        };

        [
            x.x, y.x, z.x, 0.0,
            x.y, y.y, z.y, 0.0,
            x.z, y.z, z.z, 0.0,
            -(x.x * eye.x + x.y * eye.y + x.z * eye.z),
            -(y.x * eye.x + y.y * eye.y + y.z * eye.z),
            -(z.x * eye.x + z.y * eye.y + z.z * eye.z),
            1.0,
        ]
    }
}