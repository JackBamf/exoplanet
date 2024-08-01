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
        data = response.json()
        return pandas.DataFrame(data)
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def find_hottest_host(df):
    hottestHost = df
    hottestHost['HostStarTempK'] = pandas.to_numeric(df['HostStarTempK'], errors='coerce')                      # Convert the 'HostStarTempK' column to numeric, forcing non-numeric values to NaN
    hottestHost = hottestHost.dropna(subset=['HostStarTempK'])                                                  # Drop rows with NaN values in 'HostStarTempK'
    return hottestHost.loc[df['HostStarTempK'].idxmax()]['PlanetIdentifier']                                    # Find the row with the maximum temperature using idxmax()

def count_orphan_planets(df):
    orphanDF = df[df['TypeFlag'] == 3]
    return orphanDF.shape[0]

def create_timeline_summary(df):
    df['RadiusJpt'] = pandas.to_numeric(df['RadiusJpt'], errors='coerce')                                       # Convert the 'RadiusJpt' column to numeric, forcing non-numeric values to NaN
    timelineDF = df[['DiscoveryYear', 'RadiusJpt']].copy()                                                      #Create a copy of DF
    timelineDF = timelineDF.dropna(subset=['RadiusJpt'])                                                        # Drop rows with NaN values in 'RadiusJpt'
    timelineDF['SizeCategory'] = timelineDF['RadiusJpt'].apply(categorize_size)                                 #Create a new row 'SizeCategory' which will hold small, medium, or large
    timelineDF['DiscoveryYear'] = timelineDF['DiscoveryYear'].replace("", "Unknown")                            #Replace empty 'DiscoveryYear' values with "Unknown"
    return timelineDF.groupby(['DiscoveryYear', 'SizeCategory']).size().unstack(fill_value=0)                   #Group by size and discovery year. Fill empty values with 0

def main():
    url = "https://gist.githubusercontent.com/joelbirchler/66cf8045fcbb6515557347c05d789b4a/raw/9a196385b44d4288431eef74896c0512bad3defe/exoplanets"
    

    #Place the entire dataset into a padas data frame
    fullDF = fetch_data(url)

    # Find orphan planets (TypeFlag == 3)
    numOfOrphans = count_orphan_planets(fullDF)
    print(f"Number of Orphans: {numOfOrphans}\n")


    # Find the planet with the hottest host star
    hottestHost = find_hottest_host(fullDF)
    print(f"Planet with the hottest host star: {hottestHost}\n")


    # Create a timeline of planet discoveries grouped by size
    summary = create_timeline_summary(fullDF)
    print(summary)

if __name__ == "__main__":
    main()