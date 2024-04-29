import pandas as pd

locations_data = {
    'location_id': [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800],
    'street_address': ['1297 Via Cola di Rie', '93091 Calle della Te', '2017 9450 Shinjuku-ku Kamiya-cho',
                       '6823', '2014 2011 Jabberwocky Rd Interiors Blvd', '99236',
                       '2007 2004 Zagora St Charade Rd', '98199', '147 Spadina Ave'],
    'postal_code': ['989', '10934', '1689', '', '26192', '', '50090', '98199', 'MSV 2L7'],
    'city': ['Roma', 'Venice', 'Tokyo Hiroshima', '', 'Southlake', 'South San California',
             'South Brun New Jersey Seattle Washington', '', 'Toronto'],
    'state_province': ['IT', 'IT', 'Tokyo Prefecture', 'JP', 'Texas', 'California',
                       'Washington', 'US', 'Ontario'],
    'country_id': ['IT', 'IT', 'JP', 'JP', 'US', 'US', 'US', 'US', 'CA']
}

countries_data = {
    'country_id': ['AR', 'AU', 'BE', 'BR', 'CA', 'CH', 'CN', 'DE'],
    'country_name': ['Argentina', 'Australia', 'Belgium', 'Brazil', 'Canada', 'Switzerland', 'China', 'Germany'],
    'region_id': [2, 3, 1, 2, 2, 1, 3, 1]
}

locations_df = pd.DataFrame(locations_data)
countries_df = pd.DataFrame(countries_data)

print("Locations Table:")
print(locations_df)

print("\nCountries Table:")
print(countries_df)

canada_locations = locations_df.merge(countries_df, on='country_id')
canada_addresses = canada_locations[canada_locations['country_name'] == 'Canada']

print("Using JOIN:")
print(canada_addresses[['location_id', 'street_address', 'city', 'state_province', 'country_name']])

country_map = {row['country_id']: row['country_name'] for _, row in countries_df.iterrows()}
locations_df['country_name'] = locations_df['country_id'].map(country_map)
canada_addresses_no_join = locations_df[locations_df['country_name'] == 'Canada']

print("\nWithout JOIN:")
print(canada_addresses_no_join[['location_id', 'street_address', 'city', 'state_province', 'country_name']])
