import Foundation

@MainActor
class BeachDashboardViewModel: ObservableObject {
    @Published var surfData: SurfData?
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    private let apiService = APIService.shared
    
    func fetchSurfData(for beachName: String) async {
        isLoading = true
        errorMessage = nil
        do {
            surfData = try await apiService.fetchSurfData(for: beachName)
        } catch {
            errorMessage = "Failed to load surf data: \(error.localizedDescription)"
        }
        isLoading = false
    }
} 