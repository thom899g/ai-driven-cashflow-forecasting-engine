import asyncio
from cashflow_forecasting_engine import CashflowForecastingEngine
from data_sources import TransactionHistorySource, MarketConditionsSource
from preprocessors import DataCleaningPreprocessor
from models import CashflowForecastingModel

async def initialize_system():
    engine = CashflowForecastingEngine()
    
    # Add data sources
    engine.add_data_source(TransactionHistorySource("TransactionHistory"))
    engine.add_data_source(MarketConditionsSource("MarketConditions"))
    
    # Add preprocessors
    engine.add_preprocessor(DataCleaningPreprocessor("DataCleaning"))
    
    # Add model
    model = CashflowForecastingModel()
    engine.add_model("CashflowModel", model)
    
async def main():
    await initialize_system()
    # Example usage
    try:
        data = await engine.fetch_data("2023-0