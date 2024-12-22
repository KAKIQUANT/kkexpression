use polars::prelude::*;
use std::error::Error;

pub trait Operator: Send + Sync {
    fn evaluate(&self, df: &DataFrame, args: &[Series]) -> Result<Series, Box<dyn Error>>;
    fn arity(&self) -> usize;
}

pub struct AddOperator;
impl Operator for AddOperator {
    fn evaluate(&self, _df: &DataFrame, args: &[Series]) -> Result<Series, Box<dyn Error>> {
        Ok(&args[0] + &args[1])
    }
    
    fn arity(&self) -> usize { 2 }
}

pub struct SubOperator;
impl Operator for SubOperator {
    fn evaluate(&self, _df: &DataFrame, args: &[Series]) -> Result<Series, Box<dyn Error>> {
        Ok(&args[0] - &args[1])
    }
    
    fn arity(&self) -> usize { 2 }
}

pub struct MulOperator;
impl Operator for MulOperator {
    fn evaluate(&self, _df: &DataFrame, args: &[Series]) -> Result<Series, Box<dyn Error>> {
        Ok(&args[0] * &args[1])
    }
    
    fn arity(&self) -> usize { 2 }
}

pub struct DivOperator;
impl Operator for DivOperator {
    fn evaluate(&self, _df: &DataFrame, args: &[Series]) -> Result<Series, Box<dyn Error>> {
        Ok(&args[0] / &args[1])
    }
    
    fn arity(&self) -> usize { 2 }
}

pub struct MAOperator;
impl Operator for MAOperator {
    fn evaluate(&self, _df: &DataFrame, args: &[Series]) -> Result<Series, Box<dyn Error>> {
        let window: i64 = args[1].cast(&DataType::Int64)?[0];
        Ok(args[0].rolling_mean(window as usize))
    }
    
    fn arity(&self) -> usize { 2 }
}

pub struct StdOperator;
impl Operator for StdOperator {
    fn evaluate(&self, _df: &DataFrame, args: &[Series]) -> Result<Series, Box<dyn Error>> {
        let window: i64 = args[1].cast(&DataType::Int64)?[0];
        Ok(args[0].rolling_std(window as usize))
    }
    
    fn arity(&self) -> usize { 2 }
}

pub struct RankOperator;
impl Operator for RankOperator {
    fn evaluate(&self, _df: &DataFrame, args: &[Series]) -> Result<Series, Box<dyn Error>> {
        Ok(args[0].rank(RankOptions {
            method: RankMethod::Average,
            descending: false,
        }))
    }
    
    fn arity(&self) -> usize { 1 }
} 