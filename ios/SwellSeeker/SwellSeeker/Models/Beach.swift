import Foundation

struct Beach: Identifiable, Codable {
    let id: Int
    let beachName: String
    let town: String
    let state: String
    let lat: Double
    let long: Double
    let beachAngle: Double
    let stationId: String?
    
    enum CodingKeys: String, CodingKey {
        case id
        case beachName = "beach_name"
        case town
        case state
        case lat
        case long
        case beachAngle = "beach_angle"
        case stationId = "station_id"
    }
}

struct BeachList: Codable {
    let beaches: [Beach]
} 