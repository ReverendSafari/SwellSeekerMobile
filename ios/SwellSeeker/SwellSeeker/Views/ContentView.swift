import SwiftUI

struct ContentView: View {
    @StateObject private var beachViewModel = BeachViewModel()
    
    var body: some View {
        NavigationView {
            List(beachViewModel.beaches) { beach in
                NavigationLink(destination: BeachDashboardView(beach: beach)) {
                    BeachRowView(beach: beach)
                }
            }
            .navigationTitle("SwellSeeker")
            .refreshable {
                await beachViewModel.fetchBeaches()
            }
        }
        .task {
            await beachViewModel.fetchBeaches()
        }
    }
}

struct BeachRowView: View {
    let beach: Beach
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(beach.beachName)
                .font(.headline)
            
            Text("\(beach.town), \(beach.state)")
                .font(.subheadline)
                .foregroundColor(.secondary)
        }
        .padding(.vertical, 4)
    }
}

#Preview {
    ContentView()
} 