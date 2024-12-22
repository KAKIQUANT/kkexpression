use polars::prelude::*;
use std::collections::HashMap;
use std::error::Error;

pub mod rpn;
pub mod operators;
pub mod factor;

#[derive(Debug)]
pub struct ExprEngine {
    operators: HashMap<String, Box<dyn Operator>>,
}

impl ExprEngine {
    pub fn new() -> Self {
        let mut engine = ExprEngine {
            operators: HashMap::new(),
        };
        engine.register_default_operators();
        engine
    }

    pub fn evaluate(&self, df: &DataFrame, expr: &str) -> Result<Series, Box<dyn Error>> {
        let tokens = rpn::parse_expression(expr)?;
        let result = rpn::evaluate_rpn(df, &tokens, &self.operators)?;
        Ok(result)
    }

    fn register_default_operators(&mut self) {
        // Register basic arithmetic operators
        self.operators.insert("+".to_string(), Box::new(AddOperator));
        self.operators.insert("-".to_string(), Box::new(SubOperator));
        self.operators.insert("*".to_string(), Box::new(MulOperator));
        self.operators.insert("/".to_string(), Box::new(DivOperator));
        
        // Register functions
        self.operators.insert("MA".to_string(), Box::new(MAOperator));
        self.operators.insert("STD".to_string(), Box::new(StdOperator));
        self.operators.insert("RANK".to_string(), Box::new(RankOperator));
    }
} 