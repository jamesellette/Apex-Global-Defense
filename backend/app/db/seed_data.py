"""Seed data for initial database population.

DISCLAIMER: This data is compiled from publicly available sources including
GlobalFirepower, IISS Military Balance, SIPRI, and government publications.
This data is provided for educational and simulation purposes only.

IMPORTANT NOTICES:
- All figures are approximate and may not reflect current real-world values
- Defense budgets and military capabilities change frequently
- This data should NOT be used for actual intelligence or defense planning
- Geographic coordinates are capital city centers, not military installations
- Population and GDP figures are estimates and subject to revision

DATA SOURCES (all publicly available):
- GlobalFirepower (www.globalfirepower.com)
- IISS Military Balance
- SIPRI Military Expenditure Database
- CIA World Factbook
- World Bank Open Data

For accurate, up-to-date information, please consult official government
sources and verified intelligence publications.
"""

# Top 50 nations by military strength with basic data
# Data based on publicly available sources (GlobalFirepower, IISS, etc.)

COUNTRIES_DATA = [
    {"name": "United States", "iso_code": "USA", "iso_code_2": "US", "region": "Americas", "subregion": "North America", "capital": "Washington, D.C.", "population": 334914895, "area_sq_km": 9833517, "gdp_usd": 25462700000000, "defense_budget_usd": 886000000000, "lat": 38.8951, "lng": -77.0364},
    {"name": "Russia", "iso_code": "RUS", "iso_code_2": "RU", "region": "Europe", "subregion": "Eastern Europe", "capital": "Moscow", "population": 144444359, "area_sq_km": 17098242, "gdp_usd": 1778000000000, "defense_budget_usd": 86000000000, "lat": 55.7558, "lng": 37.6173},
    {"name": "China", "iso_code": "CHN", "iso_code_2": "CN", "region": "Asia", "subregion": "Eastern Asia", "capital": "Beijing", "population": 1425671352, "area_sq_km": 9596960, "gdp_usd": 17963000000000, "defense_budget_usd": 292000000000, "lat": 39.9042, "lng": 116.4074},
    {"name": "India", "iso_code": "IND", "iso_code_2": "IN", "region": "Asia", "subregion": "Southern Asia", "capital": "New Delhi", "population": 1417173173, "area_sq_km": 3287263, "gdp_usd": 3385000000000, "defense_budget_usd": 81400000000, "lat": 28.6139, "lng": 77.2090},
    {"name": "South Korea", "iso_code": "KOR", "iso_code_2": "KR", "region": "Asia", "subregion": "Eastern Asia", "capital": "Seoul", "population": 51784059, "area_sq_km": 100210, "gdp_usd": 1665000000000, "defense_budget_usd": 46400000000, "lat": 37.5665, "lng": 126.9780},
    {"name": "United Kingdom", "iso_code": "GBR", "iso_code_2": "GB", "region": "Europe", "subregion": "Northern Europe", "capital": "London", "population": 67886011, "area_sq_km": 243610, "gdp_usd": 3070000000000, "defense_budget_usd": 68500000000, "lat": 51.5074, "lng": -0.1278},
    {"name": "Japan", "iso_code": "JPN", "iso_code_2": "JP", "region": "Asia", "subregion": "Eastern Asia", "capital": "Tokyo", "population": 125681593, "area_sq_km": 377915, "gdp_usd": 4231000000000, "defense_budget_usd": 47200000000, "lat": 35.6762, "lng": 139.6503},
    {"name": "Turkey", "iso_code": "TUR", "iso_code_2": "TR", "region": "Asia", "subregion": "Western Asia", "capital": "Ankara", "population": 85279553, "area_sq_km": 783562, "gdp_usd": 906000000000, "defense_budget_usd": 19000000000, "lat": 39.9334, "lng": 32.8597},
    {"name": "Pakistan", "iso_code": "PAK", "iso_code_2": "PK", "region": "Asia", "subregion": "Southern Asia", "capital": "Islamabad", "population": 220892331, "area_sq_km": 881912, "gdp_usd": 376000000000, "defense_budget_usd": 10300000000, "lat": 33.6844, "lng": 73.0479},
    {"name": "Italy", "iso_code": "ITA", "iso_code_2": "IT", "region": "Europe", "subregion": "Southern Europe", "capital": "Rome", "population": 59554023, "area_sq_km": 301340, "gdp_usd": 2010000000000, "defense_budget_usd": 29500000000, "lat": 41.9028, "lng": 12.4964},
    {"name": "France", "iso_code": "FRA", "iso_code_2": "FR", "region": "Europe", "subregion": "Western Europe", "capital": "Paris", "population": 67749632, "area_sq_km": 643801, "gdp_usd": 2780000000000, "defense_budget_usd": 53600000000, "lat": 48.8566, "lng": 2.3522},
    {"name": "Brazil", "iso_code": "BRA", "iso_code_2": "BR", "region": "Americas", "subregion": "South America", "capital": "Brasília", "population": 214326223, "area_sq_km": 8515767, "gdp_usd": 1920000000000, "defense_budget_usd": 20000000000, "lat": -15.7801, "lng": -47.9292},
    {"name": "Indonesia", "iso_code": "IDN", "iso_code_2": "ID", "region": "Asia", "subregion": "South-Eastern Asia", "capital": "Jakarta", "population": 275501339, "area_sq_km": 1904569, "gdp_usd": 1319000000000, "defense_budget_usd": 9100000000, "lat": -6.2088, "lng": 106.8456},
    {"name": "Egypt", "iso_code": "EGY", "iso_code_2": "EG", "region": "Africa", "subregion": "Northern Africa", "capital": "Cairo", "population": 104258327, "area_sq_km": 1001449, "gdp_usd": 476000000000, "defense_budget_usd": 4400000000, "lat": 30.0444, "lng": 31.2357},
    {"name": "Australia", "iso_code": "AUS", "iso_code_2": "AU", "region": "Oceania", "subregion": "Australia and New Zealand", "capital": "Canberra", "population": 25978935, "area_sq_km": 7741220, "gdp_usd": 1675000000000, "defense_budget_usd": 32300000000, "lat": -35.2809, "lng": 149.1300},
    {"name": "Israel", "iso_code": "ISR", "iso_code_2": "IL", "region": "Asia", "subregion": "Western Asia", "capital": "Jerusalem", "population": 9038309, "area_sq_km": 20770, "gdp_usd": 522000000000, "defense_budget_usd": 23400000000, "lat": 31.7683, "lng": 35.2137},
    {"name": "Germany", "iso_code": "DEU", "iso_code_2": "DE", "region": "Europe", "subregion": "Western Europe", "capital": "Berlin", "population": 83294633, "area_sq_km": 357022, "gdp_usd": 4072000000000, "defense_budget_usd": 56000000000, "lat": 52.5200, "lng": 13.4050},
    {"name": "Iran", "iso_code": "IRN", "iso_code_2": "IR", "region": "Asia", "subregion": "Southern Asia", "capital": "Tehran", "population": 86758304, "area_sq_km": 1648195, "gdp_usd": 388000000000, "defense_budget_usd": 25000000000, "lat": 35.6892, "lng": 51.3890},
    {"name": "Saudi Arabia", "iso_code": "SAU", "iso_code_2": "SA", "region": "Asia", "subregion": "Western Asia", "capital": "Riyadh", "population": 35950396, "area_sq_km": 2149690, "gdp_usd": 1108000000000, "defense_budget_usd": 75000000000, "lat": 24.7136, "lng": 46.6753},
    {"name": "Spain", "iso_code": "ESP", "iso_code_2": "ES", "region": "Europe", "subregion": "Southern Europe", "capital": "Madrid", "population": 47420553, "area_sq_km": 505992, "gdp_usd": 1398000000000, "defense_budget_usd": 12800000000, "lat": 40.4168, "lng": -3.7038},
    {"name": "Poland", "iso_code": "POL", "iso_code_2": "PL", "region": "Europe", "subregion": "Eastern Europe", "capital": "Warsaw", "population": 38386000, "area_sq_km": 312685, "gdp_usd": 688000000000, "defense_budget_usd": 29000000000, "lat": 52.2297, "lng": 21.0122},
    {"name": "Taiwan", "iso_code": "TWN", "iso_code_2": "TW", "region": "Asia", "subregion": "Eastern Asia", "capital": "Taipei", "population": 23894394, "area_sq_km": 36193, "gdp_usd": 790000000000, "defense_budget_usd": 19500000000, "lat": 25.0330, "lng": 121.5654},
    {"name": "Vietnam", "iso_code": "VNM", "iso_code_2": "VN", "region": "Asia", "subregion": "South-Eastern Asia", "capital": "Hanoi", "population": 98186856, "area_sq_km": 331212, "gdp_usd": 409000000000, "defense_budget_usd": 7900000000, "lat": 21.0278, "lng": 105.8342},
    {"name": "Thailand", "iso_code": "THA", "iso_code_2": "TH", "region": "Asia", "subregion": "South-Eastern Asia", "capital": "Bangkok", "population": 71697030, "area_sq_km": 513120, "gdp_usd": 543000000000, "defense_budget_usd": 7300000000, "lat": 13.7563, "lng": 100.5018},
    {"name": "Ukraine", "iso_code": "UKR", "iso_code_2": "UA", "region": "Europe", "subregion": "Eastern Europe", "capital": "Kyiv", "population": 43528136, "area_sq_km": 603550, "gdp_usd": 161000000000, "defense_budget_usd": 44000000000, "lat": 50.4501, "lng": 30.5234},
    {"name": "Greece", "iso_code": "GRC", "iso_code_2": "GR", "region": "Europe", "subregion": "Southern Europe", "capital": "Athens", "population": 10678632, "area_sq_km": 131957, "gdp_usd": 219000000000, "defense_budget_usd": 8100000000, "lat": 37.9838, "lng": 23.7275},
    {"name": "Canada", "iso_code": "CAN", "iso_code_2": "CA", "region": "Americas", "subregion": "North America", "capital": "Ottawa", "population": 38654738, "area_sq_km": 9984670, "gdp_usd": 2140000000000, "defense_budget_usd": 26500000000, "lat": 45.4215, "lng": -75.6972},
    {"name": "North Korea", "iso_code": "PRK", "iso_code_2": "KP", "region": "Asia", "subregion": "Eastern Asia", "capital": "Pyongyang", "population": 25990679, "area_sq_km": 120538, "gdp_usd": 18000000000, "defense_budget_usd": 4000000000, "lat": 39.0392, "lng": 125.7625},
    {"name": "Sweden", "iso_code": "SWE", "iso_code_2": "SE", "region": "Europe", "subregion": "Northern Europe", "capital": "Stockholm", "population": 10549347, "area_sq_km": 450295, "gdp_usd": 586000000000, "defense_budget_usd": 8400000000, "lat": 59.3293, "lng": 18.0686},
    {"name": "Netherlands", "iso_code": "NLD", "iso_code_2": "NL", "region": "Europe", "subregion": "Western Europe", "capital": "Amsterdam", "population": 17564014, "area_sq_km": 41850, "gdp_usd": 991000000000, "defense_budget_usd": 15700000000, "lat": 52.3676, "lng": 4.9041},
    {"name": "Singapore", "iso_code": "SGP", "iso_code_2": "SG", "region": "Asia", "subregion": "South-Eastern Asia", "capital": "Singapore", "population": 5453600, "area_sq_km": 719, "gdp_usd": 466000000000, "defense_budget_usd": 11500000000, "lat": 1.3521, "lng": 103.8198},
    {"name": "Algeria", "iso_code": "DZA", "iso_code_2": "DZ", "region": "Africa", "subregion": "Northern Africa", "capital": "Algiers", "population": 45606480, "area_sq_km": 2381741, "gdp_usd": 188000000000, "defense_budget_usd": 9100000000, "lat": 36.7538, "lng": 3.0588},
    {"name": "Mexico", "iso_code": "MEX", "iso_code_2": "MX", "region": "Americas", "subregion": "Central America", "capital": "Mexico City", "population": 130262216, "area_sq_km": 1964375, "gdp_usd": 1293000000000, "defense_budget_usd": 8600000000, "lat": 19.4326, "lng": -99.1332},
    {"name": "Norway", "iso_code": "NOR", "iso_code_2": "NO", "region": "Europe", "subregion": "Northern Europe", "capital": "Oslo", "population": 5511370, "area_sq_km": 323802, "gdp_usd": 579000000000, "defense_budget_usd": 8800000000, "lat": 59.9139, "lng": 10.7522},
    {"name": "Switzerland", "iso_code": "CHE", "iso_code_2": "CH", "region": "Europe", "subregion": "Western Europe", "capital": "Bern", "population": 8740472, "area_sq_km": 41284, "gdp_usd": 807000000000, "defense_budget_usd": 5600000000, "lat": 46.9480, "lng": 7.4474},
    {"name": "Belgium", "iso_code": "BEL", "iso_code_2": "BE", "region": "Europe", "subregion": "Western Europe", "capital": "Brussels", "population": 11648373, "area_sq_km": 30528, "gdp_usd": 579000000000, "defense_budget_usd": 6500000000, "lat": 50.8503, "lng": 4.3517},
    {"name": "United Arab Emirates", "iso_code": "ARE", "iso_code_2": "AE", "region": "Asia", "subregion": "Western Asia", "capital": "Abu Dhabi", "population": 9890400, "area_sq_km": 83600, "gdp_usd": 507000000000, "defense_budget_usd": 23200000000, "lat": 24.4539, "lng": 54.3773},
    {"name": "Malaysia", "iso_code": "MYS", "iso_code_2": "MY", "region": "Asia", "subregion": "South-Eastern Asia", "capital": "Kuala Lumpur", "population": 33573874, "area_sq_km": 329847, "gdp_usd": 407000000000, "defense_budget_usd": 4500000000, "lat": 3.1390, "lng": 101.6869},
    {"name": "Philippines", "iso_code": "PHL", "iso_code_2": "PH", "region": "Asia", "subregion": "South-Eastern Asia", "capital": "Manila", "population": 113880328, "area_sq_km": 300000, "gdp_usd": 404000000000, "defense_budget_usd": 4500000000, "lat": 14.5995, "lng": 120.9842},
    {"name": "South Africa", "iso_code": "ZAF", "iso_code_2": "ZA", "region": "Africa", "subregion": "Southern Africa", "capital": "Pretoria", "population": 60142978, "area_sq_km": 1221037, "gdp_usd": 405000000000, "defense_budget_usd": 3000000000, "lat": -25.7461, "lng": 28.1881},
    {"name": "Argentina", "iso_code": "ARG", "iso_code_2": "AR", "region": "Americas", "subregion": "South America", "capital": "Buenos Aires", "population": 45510318, "area_sq_km": 2780400, "gdp_usd": 633000000000, "defense_budget_usd": 2500000000, "lat": -34.6037, "lng": -58.3816},
    {"name": "Czech Republic", "iso_code": "CZE", "iso_code_2": "CZ", "region": "Europe", "subregion": "Eastern Europe", "capital": "Prague", "population": 10524167, "area_sq_km": 78867, "gdp_usd": 291000000000, "defense_budget_usd": 4000000000, "lat": 50.0755, "lng": 14.4378},
    {"name": "Romania", "iso_code": "ROU", "iso_code_2": "RO", "region": "Europe", "subregion": "Eastern Europe", "capital": "Bucharest", "population": 19317984, "area_sq_km": 238391, "gdp_usd": 301000000000, "defense_budget_usd": 5000000000, "lat": 44.4268, "lng": 26.1025},
    {"name": "Denmark", "iso_code": "DNK", "iso_code_2": "DK", "region": "Europe", "subregion": "Northern Europe", "capital": "Copenhagen", "population": 5882261, "area_sq_km": 43094, "gdp_usd": 399000000000, "defense_budget_usd": 5800000000, "lat": 55.6761, "lng": 12.5683},
    {"name": "Finland", "iso_code": "FIN", "iso_code_2": "FI", "region": "Europe", "subregion": "Northern Europe", "capital": "Helsinki", "population": 5548241, "area_sq_km": 338424, "gdp_usd": 297000000000, "defense_budget_usd": 5300000000, "lat": 60.1699, "lng": 24.9384},
    {"name": "Bangladesh", "iso_code": "BGD", "iso_code_2": "BD", "region": "Asia", "subregion": "Southern Asia", "capital": "Dhaka", "population": 169828911, "area_sq_km": 147570, "gdp_usd": 460000000000, "defense_budget_usd": 4700000000, "lat": 23.8103, "lng": 90.4125},
    {"name": "Nigeria", "iso_code": "NGA", "iso_code_2": "NG", "region": "Africa", "subregion": "Western Africa", "capital": "Abuja", "population": 218541212, "area_sq_km": 923768, "gdp_usd": 477000000000, "defense_budget_usd": 2800000000, "lat": 9.0765, "lng": 7.3986},
    {"name": "Portugal", "iso_code": "PRT", "iso_code_2": "PT", "region": "Europe", "subregion": "Southern Europe", "capital": "Lisbon", "population": 10352042, "area_sq_km": 92090, "gdp_usd": 252000000000, "defense_budget_usd": 3400000000, "lat": 38.7223, "lng": -9.1393},
    {"name": "Austria", "iso_code": "AUT", "iso_code_2": "AT", "region": "Europe", "subregion": "Western Europe", "capital": "Vienna", "population": 9066710, "area_sq_km": 83871, "gdp_usd": 471000000000, "defense_budget_usd": 3600000000, "lat": 48.2082, "lng": 16.3738},
    {"name": "Colombia", "iso_code": "COL", "iso_code_2": "CO", "region": "Americas", "subregion": "South America", "capital": "Bogotá", "population": 51265841, "area_sq_km": 1141748, "gdp_usd": 343000000000, "defense_budget_usd": 10100000000, "lat": 4.7110, "lng": -74.0721},
]

# Sample military branch data for major powers
MILITARY_BRANCHES_DATA = {
    "USA": [
        {"name": "United States Army", "branch_type": "army", "personnel_active": 485000, "personnel_reserve": 336000},
        {"name": "United States Navy", "branch_type": "navy", "personnel_active": 340000, "personnel_reserve": 100000},
        {"name": "United States Air Force", "branch_type": "air_force", "personnel_active": 320000, "personnel_reserve": 70000},
        {"name": "United States Marine Corps", "branch_type": "marines", "personnel_active": 177000, "personnel_reserve": 38000},
        {"name": "United States Space Force", "branch_type": "space_force", "personnel_active": 16000, "personnel_reserve": 0},
        {"name": "United States Coast Guard", "branch_type": "coast_guard", "personnel_active": 42000, "personnel_reserve": 7000},
    ],
    "RUS": [
        {"name": "Russian Ground Forces", "branch_type": "army", "personnel_active": 280000, "personnel_reserve": 250000},
        {"name": "Russian Navy", "branch_type": "navy", "personnel_active": 150000, "personnel_reserve": 0},
        {"name": "Russian Aerospace Forces", "branch_type": "air_force", "personnel_active": 165000, "personnel_reserve": 0},
        {"name": "Russian Strategic Rocket Forces", "branch_type": "other", "personnel_active": 50000, "personnel_reserve": 0},
    ],
    "CHN": [
        {"name": "People's Liberation Army Ground Force", "branch_type": "army", "personnel_active": 975000, "personnel_reserve": 510000},
        {"name": "People's Liberation Army Navy", "branch_type": "navy", "personnel_active": 260000, "personnel_reserve": 0},
        {"name": "People's Liberation Army Air Force", "branch_type": "air_force", "personnel_active": 395000, "personnel_reserve": 0},
        {"name": "People's Liberation Army Rocket Force", "branch_type": "other", "personnel_active": 120000, "personnel_reserve": 0},
    ],
    "IND": [
        {"name": "Indian Army", "branch_type": "army", "personnel_active": 1230000, "personnel_reserve": 960000},
        {"name": "Indian Navy", "branch_type": "navy", "personnel_active": 67000, "personnel_reserve": 75000},
        {"name": "Indian Air Force", "branch_type": "air_force", "personnel_active": 140000, "personnel_reserve": 0},
    ],
    "GBR": [
        {"name": "British Army", "branch_type": "army", "personnel_active": 79000, "personnel_reserve": 30000},
        {"name": "Royal Navy", "branch_type": "navy", "personnel_active": 33000, "personnel_reserve": 3000},
        {"name": "Royal Air Force", "branch_type": "air_force", "personnel_active": 33000, "personnel_reserve": 2000},
    ],
}

# Sample equipment data
EQUIPMENT_DATA = {
    "USA_army": [
        {"category": "tanks", "name": "M1 Abrams", "model": "M1A2 SEP v3", "quantity": 2509, "operational_percentage": 0.85, "year_introduced": 1980, "country_of_origin": "USA"},
        {"category": "armored_vehicles", "name": "Bradley", "model": "M2A3", "quantity": 4500, "operational_percentage": 0.80, "year_introduced": 1981, "country_of_origin": "USA"},
        {"category": "artillery", "name": "M109 Paladin", "model": "M109A7", "quantity": 950, "operational_percentage": 0.75, "year_introduced": 1963, "country_of_origin": "USA"},
        {"category": "mlrs", "name": "M270 MLRS", "model": "M270A1", "quantity": 400, "operational_percentage": 0.80, "year_introduced": 1983, "country_of_origin": "USA"},
    ],
    "USA_navy": [
        {"category": "naval_carriers", "name": "Aircraft Carrier", "model": "Nimitz/Ford Class", "quantity": 11, "operational_percentage": 0.90, "year_introduced": 1975, "country_of_origin": "USA"},
        {"category": "naval_destroyers", "name": "Destroyer", "model": "Arleigh Burke Class", "quantity": 73, "operational_percentage": 0.85, "year_introduced": 1991, "country_of_origin": "USA"},
        {"category": "naval_submarines", "name": "Nuclear Submarine", "model": "Virginia/Los Angeles Class", "quantity": 68, "operational_percentage": 0.85, "year_introduced": 1976, "country_of_origin": "USA"},
    ],
    "USA_air_force": [
        {"category": "aircraft_fighter", "name": "F-35 Lightning II", "model": "F-35A", "quantity": 450, "operational_percentage": 0.75, "year_introduced": 2016, "country_of_origin": "USA"},
        {"category": "aircraft_fighter", "name": "F-22 Raptor", "model": "F-22A", "quantity": 187, "operational_percentage": 0.65, "year_introduced": 2005, "country_of_origin": "USA"},
        {"category": "aircraft_fighter", "name": "F-15 Eagle", "model": "F-15E Strike Eagle", "quantity": 218, "operational_percentage": 0.80, "year_introduced": 1976, "country_of_origin": "USA"},
        {"category": "aircraft_attack", "name": "A-10 Thunderbolt II", "model": "A-10C", "quantity": 281, "operational_percentage": 0.85, "year_introduced": 1977, "country_of_origin": "USA"},
    ],
    "RUS_army": [
        {"category": "tanks", "name": "T-90", "model": "T-90M", "quantity": 350, "operational_percentage": 0.80, "year_introduced": 1993, "country_of_origin": "RUS"},
        {"category": "tanks", "name": "T-72", "model": "T-72B3", "quantity": 2000, "operational_percentage": 0.65, "year_introduced": 1973, "country_of_origin": "RUS"},
        {"category": "tanks", "name": "T-80", "model": "T-80BVM", "quantity": 450, "operational_percentage": 0.60, "year_introduced": 1976, "country_of_origin": "RUS"},
        {"category": "artillery", "name": "2S19 Msta", "model": "2S19M2", "quantity": 800, "operational_percentage": 0.70, "year_introduced": 1989, "country_of_origin": "RUS"},
    ],
    "CHN_army": [
        {"category": "tanks", "name": "Type 99", "model": "Type 99A", "quantity": 800, "operational_percentage": 0.85, "year_introduced": 2001, "country_of_origin": "CHN"},
        {"category": "tanks", "name": "Type 96", "model": "Type 96A/B", "quantity": 2500, "operational_percentage": 0.75, "year_introduced": 1997, "country_of_origin": "CHN"},
    ],
    "CHN_navy": [
        {"category": "naval_carriers", "name": "Aircraft Carrier", "model": "Liaoning/Shandong/Fujian", "quantity": 3, "operational_percentage": 0.85, "year_introduced": 2012, "country_of_origin": "CHN"},
        {"category": "naval_destroyers", "name": "Destroyer", "model": "Type 052D/055", "quantity": 50, "operational_percentage": 0.85, "year_introduced": 2014, "country_of_origin": "CHN"},
        {"category": "naval_submarines", "name": "Nuclear Submarine", "model": "Type 094/095", "quantity": 12, "operational_percentage": 0.80, "year_introduced": 2007, "country_of_origin": "CHN"},
    ],
}
