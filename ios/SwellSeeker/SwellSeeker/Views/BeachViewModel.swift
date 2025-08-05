import Foundation

@MainActor
class BeachViewModel: ObservableObject {
    @Published var beaches: [Beach] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    private let apiService = APIService.shared
    
    func fetchBeaches() async {
        isLoading = true
        errorMessage = nil
        
        do {
            beaches = try await apiService.fetchBeaches()
        } catch {
            errorMessage = "Failed to load beaches: \(error.localizedDescription)"
        }
        
        isLoading = false
    }
} 