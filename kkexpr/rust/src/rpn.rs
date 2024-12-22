use polars::prelude::*;
use std::collections::VecDeque;
use std::error::Error;

pub fn parse_expression(expr: &str) -> Result<Vec<String>, Box<dyn Error>> {
    let mut output = Vec::new();
    let mut operator_stack = Vec::new();
    
    let tokens = tokenize(expr);
    
    for token in tokens {
        match token.as_str() {
            "(" => operator_stack.push(token),
            ")" => {
                while let Some(op) = operator_stack.pop() {
                    if op == "(" {
                        break;
                    }
                    output.push(op);
                }
            }
            op if is_operator(&token) => {
                while let Some(top) = operator_stack.last() {
                    if !is_operator(top) || precedence(&token) > precedence(top) {
                        break;
                    }
                    output.push(operator_stack.pop().unwrap());
                }
                operator_stack.push(token);
            }
            _ => output.push(token),
        }
    }
    
    while let Some(op) = operator_stack.pop() {
        output.push(op);
    }
    
    Ok(output)
}

pub fn evaluate_rpn(
    df: &DataFrame,
    tokens: &[String],
    operators: &HashMap<String, Box<dyn Operator>>
) -> Result<Series, Box<dyn Error>> {
    let mut stack: VecDeque<Series> = VecDeque::new();
    
    for token in tokens {
        if let Some(operator) = operators.get(token) {
            let args = (0..operator.arity())
                .map(|_| stack.pop_front().unwrap())
                .collect::<Vec<_>>();
            let result = operator.evaluate(df, &args)?;
            stack.push_front(result);
        } else if let Ok(value) = token.parse::<f64>() {
            stack.push_front(Series::new("", &[value]));
        } else {
            // Assume it's a column name
            let series = df.column(token)?.clone();
            stack.push_front(series);
        }
    }
    
    Ok(stack.pop_front().unwrap())
}

fn tokenize(expr: &str) -> Vec<String> {
    // Basic tokenization - can be improved
    expr.replace("(", " ( ")
        .replace(")", " ) ")
        .split_whitespace()
        .map(String::from)
        .collect()
}

fn is_operator(token: &str) -> bool {
    matches!(token, "+" | "-" | "*" | "/" | "MA" | "STD" | "RANK")
}

fn precedence(op: &str) -> i32 {
    match op {
        "+" | "-" => 1,
        "*" | "/" => 2,
        "MA" | "STD" | "RANK" => 3,
        _ => 0,
    }
} 