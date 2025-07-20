use axum::{
    http::{header, HeaderMap, HeaderValue},
    response::Response,
};

pub struct SecurityHeaders;

impl SecurityHeaders {
    pub fn apply(response: &mut Response<axum::body::Body>) {
        let headers = response.headers_mut();
        
        // Strict Transport Security
        headers.insert(
            header::STRICT_TRANSPORT_SECURITY,
            HeaderValue::from_static("max-age=63072000; includeSubDomains; preload"),
        );
        
        // Content Security Policy
        headers.insert(
            header::CONTENT_SECURITY_POLICY,
            HeaderValue::from_static(
                "default-src 'self'; \
                script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; \
                style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; \
                font-src 'self' https://fonts.gstatic.com; \
                img-src 'self' data: https:; \
                connect-src 'self' wss: https:; \
                frame-ancestors 'none'; \
                base-uri 'self'; \
                form-action 'self'"
            ),
        );
        
        // X-Frame-Options
        headers.insert(
            header::X_FRAME_OPTIONS,
            HeaderValue::from_static("DENY"),
        );
        
        // X-Content-Type-Options
        headers.insert(
            header::X_CONTENT_TYPE_OPTIONS,
            HeaderValue::from_static("nosniff"),
        );
        
        // X-XSS-Protection
        headers.insert(
            "X-XSS-Protection",
            HeaderValue::from_static("1; mode=block"),
        );
        
        // Referrer-Policy
        headers.insert(
            header::REFERRER_POLICY,
            HeaderValue::from_static("strict-origin-when-cross-origin"),
        );
        
        // Permissions-Policy
        headers.insert(
            "Permissions-Policy",
            HeaderValue::from_static(
                "accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()"
            ),
        );
    }
}