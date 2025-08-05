import Foundation

struct SurfData: Codable {
    let beachName: String
    let wind: WeatherDataBlock?
    let waves: WeatherDataBlock?
    let tides: WeatherDataBlock?
    let temperature: WeatherDataBlock?
    let grade: String?
    let cached: Bool?
    
    enum CodingKeys: String, CodingKey {
        case beachName = "beach_name"
        case wind, waves, tides, temperature, grade, cached
    }
}

struct WeatherDataBlock: Codable {
    let beachName: String
    let dataType: String
    let data: [String: AnyCodable]?
    let cached: Bool?
    
    enum CodingKeys: String, CodingKey {
        case beachName = "beach_name"
        case dataType = "data_type"
        case data, cached
    }
}

// Helper to allow Codable for Any
struct AnyCodable: Codable {
    let value: Any
    
    init(_ value: Any) {
        self.value = value
    }
    
    init(from decoder: Decoder) throws {
        let container = try decoder.singleValueContainer()
        if let intValue = try? container.decode(Int.self) {
            value = intValue
        } else if let doubleValue = try? container.decode(Double.self) {
            value = doubleValue
        } else if let stringValue = try? container.decode(String.self) {
            value = stringValue
        } else if let boolValue = try? container.decode(Bool.self) {
            value = boolValue
        } else if let arrayValue = try? container.decode([AnyCodable].self) {
            value = arrayValue.map { $0.value }
        } else if let dictValue = try? container.decode([String: AnyCodable].self) {
            value = dictValue.mapValues { $0.value }
        } else {
            throw DecodingError.dataCorruptedError(in: container, debugDescription: "Unsupported type")
        }
    }
    
    func encode(to encoder: Encoder) throws {
        var container = encoder.singleValueContainer()
        switch value {
        case let intValue as Int:
            try container.encode(intValue)
        case let doubleValue as Double:
            try container.encode(doubleValue)
        case let stringValue as String:
            try container.encode(stringValue)
        case let boolValue as Bool:
            try container.encode(boolValue)
        case let arrayValue as [Any]:
            let encodableArray = arrayValue.map { AnyCodable($0) }
            try container.encode(encodableArray)
        case let dictValue as [String: Any]:
            let encodableDict = dictValue.mapValues { AnyCodable($0) }
            try container.encode(encodableDict)
        default:
            throw EncodingError.invalidValue(value, EncodingError.Context(codingPath: container.codingPath, debugDescription: "Unsupported type"))
        }
    }
}

struct WindData: Codable {
    let latitude: Double
    let longitude: Double
    let hourly: WindHourlyData
    let cached: Bool?
    
    struct WindHourlyData: Codable {
        let time: [String]
        let windSpeed10m: [Double]
        let windDirection10m: [Int]
        
        enum CodingKeys: String, CodingKey {
            case time
            case windSpeed10m = "wind_speed_10m"
            case windDirection10m = "wind_direction_10m"
        }
    }
}

struct WaveData: Codable {
    let latitude: Double
    let longitude: Double
    let hourly: WaveHourlyData
    let cached: Bool?
    
    struct WaveHourlyData: Codable {
        let time: [String]
        let waveHeight: [Double]
        let waveDirection: [Int]
        let wavePeriod: [Double]
        
        enum CodingKeys: String, CodingKey {
            case time
            case waveHeight = "wave_height"
            case waveDirection = "wave_direction"
            case wavePeriod = "wave_period"
        }
    }
}

struct TideData: Codable {
    let time: String
    let height: String
    let type: String
}

struct TemperatureData: Codable {
    let stationId: String
    let waterTemp: String
    let airTemp: String
    let cached: Bool?
    
    enum CodingKeys: String, CodingKey {
        case stationId = "station_id"
        case waterTemp = "water_temp"
        case airTemp = "air_temp"
        case cached
    }
} 