import requests
import pandas

def categorize_size(radius):
    if radius <1:
        return 'small'
    if radius < 2:
        return 'medium'
    else:
        return 'large'
    
def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def main():
    url = "https://gist.githubusercontent.com/joelbirchler/66cf8045fcbb6515557347c05d789b4a/raw/9a196385b44d4288431eef74896c0512bad3defe/exoplanets"
    data = fetch_data(url)
    if data is None:
        return

    #Place the entire dataset into a padas data frame
    fullDF = pandas.DataFrame(data)

    # Find orphan planets (TypeFlag == 3)
    orphanDF = fullDF[fullDF['TypeFlag'] == 3]
    numOfOrphans = orphanDF.shape[0]
    print(f"Number of Orphans: {numOfOrphans}\n")


    # Find the planet with the hottest host star
    hottestHost = fullDF
    hottestHost['HostStarTempK'] = pandas.to_numeric(fullDF['HostStarTempK'], errors='coerce')              # Convert the 'HostStarTempK' column to numeric, forcing non-numeric values to NaN
    hottestHost = hottestHost.dropna(subset=['HostStarTempK'])                                              # Drop rows with NaN values in 'HostStarTempK'
    hottestHost = hottestHost.loc[fullDF['HostStarTempK'].idxmax()]                                         # Find the row with the maximum temperature using idxmax()
    print(f"Planet with the hottest host star: {hottestHost['PlanetIdentifier']}\n")


    # Create a timeline of planet discoveries grouped by size
    fullDF['RadiusJpt'] = pandas.to_numeric(fullDF['RadiusJpt'], errors='coerce')                           # Convert the 'RadiusJpt' column to numeric, forcing non-numeric values to NaN
    timelineDF = fullDF[['DiscoveryYear', 'RadiusJpt']].copy()                                              #Create a copy of DF
    timelineDF = timelineDF.dropna(subset=['RadiusJpt'])                                                    # Drop rows with NaN values in 'RadiusJpt'
    timelineDF['SizeCategory'] = timelineDF['RadiusJpt'].apply(categorize_size)                             #Create a new row 'SizeCategory' which will hold small, medium, or large
    timelineDF['DiscoveryYear'] = timelineDF['DiscoveryYear'].replace("", "Unknown")                        #Replace empty 'DiscoveryYear' values with "Unknown"
    summary = timelineDF.groupby(['DiscoveryYear', 'SizeCategory']).size().unstack(fill_value=0)            #Group by size and discovery year. Fill empty values with 0
    print(summary)

if __name__ == "__main__":
    main()