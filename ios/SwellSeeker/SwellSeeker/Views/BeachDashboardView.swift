import SwiftUI

struct BeachDashboardView: View {
    let beach: Beach
    @StateObject private var viewModel = BeachDashboardViewModel()
    
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            if viewModel.isLoading {
                ProgressView("Loading surf data...")
            } else if let surfData = viewModel.surfData {
                Text("Condition: \(surfData.grade?.capitalized ?? "N/A")")
                    .font(.title2)
                // TODO: Add components for surf height, swell, wind, tide, temperature, etc.
                Text("Wind: \(surfData.wind?.dataType ?? "N/A")")
                Text("Waves: \(surfData.waves?.dataType ?? "N/A")")
                Text("Tides: \(surfData.tides?.dataType ?? "N/A")")
                Text("Temperature: \(surfData.temperature?.dataType ?? "N/A")")
            } else if let error = viewModel.errorMessage {
                Text(error).foregroundColor(.red)
            } else {
                Text("No data available.")
            }
        }
        .padding()
        .navigationTitle(beach.beachName)
        .task {
            await viewModel.fetchSurfData(for: beach.beachName)
        }
    }
} 