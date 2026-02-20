import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CashflowForecastingEngine:
    def __init__(self):
        self.models = {}
        self.data_sources = []
        self.preprocessors = []
    
    def add_model(self, name: str, model) -> None:
        """Add a forecasting model to the engine."""
        self.models[name] = model
        logger.info(f"Added model '{name}' to the engine.")
    
    def add_data_source(self, source) -> None:
        """Register a data source with the engine."""
        self.data_sources.append(source)
        logger.info(f"Registered data source '{source.name}'")
    
    def add_preprocessor(self, preprocessor) -> None:
        """Add a data preprocessing step."""
        self.preprocessors.append(preprocessor)
        logger.info(f"Added preprocessor '{preprocessor.name}'")
    
    async def fetch_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Fetch historical transaction and market data within date range."""
        try:
            dfs = []
            for source in self.data_sources:
                df = await source.fetch(start_date, end_date)
                dfs.append(df)
            combined_df = pd.concat(dfs)
            return combined_df
        except Exception as e:
            logger.error(f"Failed to fetch data: {str(e)}")
            raise
    
    async def preprocess_data(self, raw_data: pd.DataFrame) -> Dict[str, Any]:
        """Preprocess raw data for model input."""
        processed_data = {}
        for preprocessor in self.preprocessors:
            try:
                result = await preprocessor.run(raw_data)
                processed_data[preprocessor.name] = result
            except Exception as e:
                logger.error(f"Preprocessing failed: {str(e)}")
        return processed_data
    
    async def train_model(self, model_name: str, data: pd.DataFrame) -> None:
        """Train the specified model with provided data."""
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not registered.")
        try:
            await self.models[model_name].train(data)
            logger.info(f"Trained model '{model_name}' successfully.")
        except Exception as e:
            logger.error(f"Training failed for model '{model_name}': {str(e)}")
    
    async def forecast(self, model_name: str, lookback_period: int) -> pd.DataFrame:
        """Generate cashflow forecasts using specified model."""
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not registered.")
        try:
            forecast = await self.models[model_name].forecast(lookback_period)
            return forecast
        except Exception as e:
            logger.error(f"Forecasting failed for model '{model_name}': {str(e)}")
            raise
    
    async def optimize_strategy(self, forecast: pd.DataFrame) -> Dict[str, Any]:
        """Optimize financial strategies based on forecasts."""
        # Placeholder method; implement specific optimization logic
        pass