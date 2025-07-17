use anyhow::Result;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Serialize, Deserialize)]
pub struct GeolocationInfo {
    pub country_code: String,
    pub country_name: String,
    pub region: Option<String>,
    pub city: Option<String>,
    pub timezone: Option<String>,
    pub language: String,
}

// Country code to primary language mapping
lazy_static::lazy_static! {
    static ref COUNTRY_LANGUAGE_MAP: HashMap<&'static str, &'static str> = {
        let mut m = HashMap::new();
        // Major countries and their primary languages
        m.insert("US", "en"); // United States
        m.insert("GB", "en"); // United Kingdom
        m.insert("CA", "en"); // Canada (English dominant)
        m.insert("AU", "en"); // Australia
        m.insert("NZ", "en"); // New Zealand
        m.insert("IE", "en"); // Ireland

        m.insert("ES", "es"); // Spain
        m.insert("MX", "es"); // Mexico
        m.insert("AR", "es"); // Argentina
        m.insert("CO", "es"); // Colombia
        m.insert("CL", "es"); // Chile
        m.insert("PE", "es"); // Peru
        m.insert("VE", "es"); // Venezuela
        m.insert("EC", "es"); // Ecuador
        m.insert("GT", "es"); // Guatemala
        m.insert("CU", "es"); // Cuba
        m.insert("BO", "es"); // Bolivia
        m.insert("DO", "es"); // Dominican Republic
        m.insert("HN", "es"); // Honduras
        m.insert("PY", "es"); // Paraguay
        m.insert("SV", "es"); // El Salvador
        m.insert("NI", "es"); // Nicaragua
        m.insert("CR", "es"); // Costa Rica
        m.insert("PA", "es"); // Panama
        m.insert("UY", "es"); // Uruguay

        m.insert("FR", "fr"); // France
        m.insert("BE", "fr"); // Belgium (French part)
        m.insert("CH", "fr"); // Switzerland (French part)
        m.insert("LU", "fr"); // Luxembourg
        m.insert("MC", "fr"); // Monaco

        m.insert("DE", "de"); // Germany
        m.insert("AT", "de"); // Austria
        m.insert("LI", "de"); // Liechtenstein

        m.insert("PT", "pt"); // Portugal
        m.insert("BR", "pt"); // Brazil
        m.insert("AO", "pt"); // Angola
        m.insert("MZ", "pt"); // Mozambique

        m.insert("IT", "it"); // Italy
        m.insert("SM", "it"); // San Marino
        m.insert("VA", "it"); // Vatican City

        m.insert("CN", "zh"); // China
        m.insert("TW", "zh"); // Taiwan
        m.insert("HK", "zh"); // Hong Kong
        m.insert("SG", "zh"); // Singapore (Chinese is one of the official languages)

        m.insert("JP", "ja"); // Japan

        m.insert("KR", "ko"); // South Korea
        m.insert("KP", "ko"); // North Korea

        m.insert("RU", "ru"); // Russia
        m.insert("BY", "ru"); // Belarus
        m.insert("KZ", "ru"); // Kazakhstan
        m.insert("KG", "ru"); // Kyrgyzstan

        m.insert("SA", "ar"); // Saudi Arabia
        m.insert("AE", "ar"); // UAE
        m.insert("EG", "ar"); // Egypt
        m.insert("IQ", "ar"); // Iraq
        m.insert("JO", "ar"); // Jordan
        m.insert("KW", "ar"); // Kuwait
        m.insert("LB", "ar"); // Lebanon
        m.insert("LY", "ar"); // Libya
        m.insert("MA", "ar"); // Morocco
        m.insert("OM", "ar"); // Oman
        m.insert("QA", "ar"); // Qatar
        m.insert("SY", "ar"); // Syria
        m.insert("TN", "ar"); // Tunisia
        m.insert("YE", "ar"); // Yemen
        m.insert("DZ", "ar"); // Algeria
        m.insert("BH", "ar"); // Bahrain

        m.insert("IN", "hi"); // India (Hindi is most common)

        // Default to English for unlisted countries
        m
    };
}

pub async fn get_language_from_ip(ip: &str) -> Result<String> {
    // For localhost/private IPs, detect system locale
    if ip == "127.0.0.1"
        || ip.starts_with("192.168.")
        || ip.starts_with("10.")
        || ip.starts_with("172.")
    {
        return Ok(get_system_language());
    }

    // Use ip-api.com free service (no API key required, 45 requests per minute limit)
    let url = format!(
        "http://ip-api.com/json/{}?fields=status,countryCode,country,regionName,city,timezone",
        ip
    );

    let client = reqwest::Client::new();
    let response = client
        .get(&url)
        .timeout(std::time::Duration::from_secs(3))
        .send()
        .await?;

    if response.status().is_success() {
        let data: serde_json::Value = response.json().await?;

        if data["status"] == "success" {
            let country_code = data["countryCode"].as_str().unwrap_or("US");
            let language = COUNTRY_LANGUAGE_MAP
                .get(country_code)
                .copied()
                .unwrap_or("en");

            return Ok(language.to_string());
        }
    }

    // Default to English if geolocation fails
    Ok("en".to_string())
}

fn get_system_language() -> String {
    // Try to get system locale
    if let Ok(lang) = std::env::var("LANG") {
        // Extract language code from locale (e.g., "en_US.UTF-8" -> "en")
        if let Some(code) = lang.split('_').next() {
            if let Some(code) = code.split('.').next() {
                return match code {
                    "es" | "fr" | "de" | "pt" | "it" | "zh" | "ja" | "ko" | "ru" | "ar" | "hi" => {
                        code.to_string()
                    }
                    _ => "en".to_string(),
                };
            }
        }
    }

    "en".to_string()
}

pub async fn get_geolocation_info(ip: &str) -> Result<GeolocationInfo> {
    // For localhost/private IPs
    if ip == "127.0.0.1"
        || ip.starts_with("192.168.")
        || ip.starts_with("10.")
        || ip.starts_with("172.")
    {
        let language = get_system_language();
        return Ok(GeolocationInfo {
            country_code: "LOCAL".to_string(),
            country_name: "Local Network".to_string(),
            region: None,
            city: None,
            timezone: None,
            language,
        });
    }

    // Use ip-api.com free service
    let url = format!(
        "http://ip-api.com/json/{}?fields=status,countryCode,country,regionName,city,timezone",
        ip
    );

    let client = reqwest::Client::new();
    let response = client
        .get(&url)
        .timeout(std::time::Duration::from_secs(3))
        .send()
        .await?;

    if response.status().is_success() {
        let data: serde_json::Value = response.json().await?;

        if data["status"] == "success" {
            let country_code = data["countryCode"].as_str().unwrap_or("US").to_string();
            let language = COUNTRY_LANGUAGE_MAP
                .get(country_code.as_str())
                .copied()
                .unwrap_or("en")
                .to_string();

            return Ok(GeolocationInfo {
                country_code,
                country_name: data["country"].as_str().unwrap_or("Unknown").to_string(),
                region: data["regionName"].as_str().map(|s| s.to_string()),
                city: data["city"].as_str().map(|s| s.to_string()),
                timezone: data["timezone"].as_str().map(|s| s.to_string()),
                language,
            });
        }
    }

    // Default response if geolocation fails
    Ok(GeolocationInfo {
        country_code: "US".to_string(),
        country_name: "United States".to_string(),
        region: None,
        city: None,
        timezone: None,
        language: "en".to_string(),
    })
}
