import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0, 1))

def prepare_data(df):
    """
    Prepare time series data for LSTM model.
    
    Args:
        df: DataFrame containing 'Close' price column
    
    Returns:
        tuple: (X, y) arrays for training
    """
    try:
        df_scaled = scaler.fit_transform(df[['Close']])
        X, y = [], []
        for i in range(50, len(df_scaled)):
            X.append(df_scaled[i-50:i, 0])
            y.append(df_scaled[i, 0])
        X = np.array(X)
        y = np.array(y)
        # Reshape X to match LSTM input shape (samples, time steps, features)
        X = X.reshape((X.shape[0], X.shape[1], 1))
        return X, y
    except KeyError:
        raise KeyError("DataFrame must contain 'Close' column")
    except Exception as e:
        raise Exception(f"Error preparing data: {str(e)}")

def create_lstm_model():
    """
    Create and compile LSTM model for time series prediction.
    
    Returns:
        Sequential: Compiled Keras LSTM model
    """
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(50, 1)),
        LSTM(50, return_sequences=False),
        Dense(25),
        Dense(1)
    ])
    model.compile(optimizer="adam", loss="mean_squared_error")
    return model
