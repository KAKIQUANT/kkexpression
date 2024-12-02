# KKExpr - Financial Expression Engine

KKExpr is a powerful Python library for evaluating financial expressions and calculating factors for quantitative trading. It provides a flexible and extensible framework for defining and computing financial indicators.

## Features

- Expression parsing and evaluation for financial factors
- Support for complex mathematical operations and time series analysis
- Built-in technical indicators and financial functions
- Efficient data loading and processing
- Type-safe operations with comprehensive error handling
- Integration with pandas DataFrames

## Installation

```bash
pip install kkexpr
```

## Quick Start

```python
from kkexpr import Factor

# Create basic factors
open_factor = Factor('open')
close_factor = Factor('close')
high_factor = Factor('high')
low_factor = Factor('low')

# Create a composite momentum factor
momentum = (close_factor - open_factor) / (high_factor - low_factor)

# Calculate factor values
result = momentum.execute(
    order_book_ids=['000001.XSHE', '600000.XSHG'],
    frequency='1d',
    start_date='20220101',
    end_date='20221231'
)
```

## Expression Functions

KKExpr supports various financial and mathematical functions:

### Technical Indicators

```python
# Moving averages
ma20 = Factor('ma(close, 20)')
ema = Factor('ema(close, 12)')

# Momentum indicators
rsi = Factor('rsi(close, 14)')
macd = Factor('macd(close, 12, 26, 9)')

# Volatility indicators
bbands = Factor('bbands(close, 20)')
atr = Factor('atr(high, low, close, 14)')
```

### Mathematical Operations

```python
# Basic arithmetic
factor1 = Factor('(high + low) / 2')

# Statistical functions
factor2 = Factor('correlation(close, volume, 20)')
factor3 = Factor('std(close, 20) / mean(close, 20)')

# Logical operations
factor4 = Factor('greater(close, ma(close, 20))')
```

## Data Loading

```python
from kkexpr import CSVDataloader

# Load data from CSV files
loader = CSVDataloader(
    path="data/",
    symbols=['000001.XSHE', '600000.XSHG'],
    start_date='20220101',
    end_date='20221231'
)

# Load with custom expressions
data = loader.load(
    fields=['roc(close,20)', 'ma(close,60)'],
    names=['momentum', 'ma60']
)
```

## Error Handling

KKExpr provides robust error handling:

```python
try:
    invalid_factor = Factor('invalid_function(close)')
    result = invalid_factor.execute(...)
except ValueError as e:
    print(f"Invalid expression: {e}")
```

## License
GPL-3.0

## Author
KAKIQUANT

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
