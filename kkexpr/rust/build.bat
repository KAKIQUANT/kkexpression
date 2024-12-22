@echo off
:: Build the extension
maturin develop

:: Run Rust tests
cargo test

:: Run Python tests
pytest ../tests/test_rust_extension.py -v 