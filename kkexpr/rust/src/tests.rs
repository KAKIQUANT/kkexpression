#[cfg(test)]
mod tests {
    use super::*;
    use polars::prelude::*;
    use crate::Factor;

    fn create_test_df() -> DataFrame {
        df! {
            "close" => &[100.0, 101.0, 99.0, 102.0, 98.0],
            "volume" => &[1000.0, 2000.0, 1500.0, 3000.0, 1200.0],
        }.unwrap()
    }

    #[test]
    fn test_simple_arithmetic() {
        let df = create_test_df();
        let factor = Factor::new("close + 1");
        let result = factor.compute(&df).unwrap();
        
        let expected = df.column("close").unwrap() + 1.0;
        assert_eq!(result, expected);
    }

    #[test]
    fn test_moving_average() {
        let df = create_test_df();
        let factor = Factor::new("MA(close, 3)");
        let result = factor.compute(&df).unwrap();
        
        // First two values will be null due to window size
        assert!(result.get(0).unwrap().is_null());
        assert!(result.get(1).unwrap().is_null());
        
        // Check the rest
        let expected = vec![100.0, 100.67, 99.67];
        for (i, &exp) in expected.iter().enumerate() {
            let val = result.get(i + 2).unwrap().try_extract::<f64>().unwrap();
            assert!((val - exp).abs() < 0.01);
        }
    }
} 