from dataclasses import dataclass
import pandas as pd
import datetime as dt
#
# # Define your data class to represent a scenario
# @dataclass
# class StockScenario:
#     name: str
#     multiplier: float
#     additional_data: dict
#
# # Function to apply a scenario to the stock data
# def apply_scenario(stock_data, scenario):
#     # Modify stock data based on the scenario
#     modified_data = stock_data.copy()
#     modified_data['Close'] = modified_data['Close'] * scenario.multiplier
#
#     # Additional scenario-specific modifications
#     # You can customize this based on your specific needs
#     for key, value in scenario.additional_data.items():
#         modified_data[key] = modified_data[key] + value
#
#     return modified_data
#
# # Example usage
# if __name__ == "__main__":
#     # Load your historical stock data into a DataFrame
#     # Replace this with your actual data loading code
#     stock_data = pd.DataFrame({
#         'Date': pd.date_range(start='2023-01-01', end='2023-01-10'),
#         'Close': [100, 105, 110, 95, 98, 102, 108, 112, 98, 105],
#         'Volume': [554100, 104545, 1168970, 96546455, 435598, 103452, 108345, 112453, 9435458, 104535]
#     })
#
#     # Define different scenarios using the StockScenario data class
#     # This scenario could be my base in which the parameter is top 0 days so nothing changes
#     scenario1 = StockScenario(name='Scenario 1', multiplier=1.1, additional_data={'Volume': 1000})
#     scenario2 = StockScenario(name='Scenario 2', multiplier=0.9, additional_data={'Volume': -500})
#
#     # Apply scenarios and store modified dataframes in a dictionary
#     scenario_results = {}
#     for scenario in [scenario1, scenario2]:
#         modified_data = apply_scenario(stock_data, scenario)
#         scenario_results[scenario.name] = modified_data
#
#     # Access modified dataframes for each scenario
#     for scenario_name, modified_data in scenario_results.items():
#         print(f"\nResults for {scenario_name}:\n{modified_data}")


date = '2023-03-01'


print('stop')