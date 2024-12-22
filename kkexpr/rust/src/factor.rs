use polars::prelude::*;
use std::error::Error;
use crate::ExprEngine;

pub struct Factor {
    engine: ExprEngine,
    expression: String,
}

impl Factor {
    pub fn new(expression: &str) -> Self {
        Factor {
            engine: ExprEngine::new(),
            expression: expression.to_string(),
        }
    }
    
    pub fn compute(&self, df: &DataFrame) -> Result<Series, Box<dyn Error>> {
        self.engine.evaluate(df, &self.expression)
    }
} 