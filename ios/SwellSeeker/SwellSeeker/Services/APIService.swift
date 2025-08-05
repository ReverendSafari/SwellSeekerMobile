import Foundation

class APIService {
    static let shared = APIService()
    
    private let baseURL = "http://localhost:8001/api/v1"
    private let apiKey = "your-api-key-here" // Replace with your actual API key
    
    private init() {}
    
    func fetchBeaches() async throws -> [Beach] {
        guard let url = URL(string: "\(baseURL)/beaches/") else {
            throw APIError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw APIError.invalidResponse
        }
        
        let beachList = try JSONDecoder().decode(BeachList.self, from: data)
        return beachList.beaches
    }
    
    func fetchSurfData(for beachName: String) async throws -> SurfData {
        let encodedBeachName = beachName.addingPercentEncoding(withAllowedCharacters: .urlPathAllowed) ?? beachName
        guard let url = URL(string: "\(baseURL)/surf-data/\(encodedBeachName)") else {
            throw APIError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw APIError.invalidResponse
        }
        
        return try JSONDecoder().decode(SurfData.self, from: data)
    }
}

enum APIError: Error {
    case invalidURL
    case invalidResponse
    case decodingError
} 