use pyo3::prelude::*;
use polars::prelude::*;
use crate::Factor;

#[pymodule]
fn kkexpr_rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyFactor>()?;
    Ok(())
}

#[pyclass]
struct PyFactor {
    inner: Factor,
}

#[pymethods]
impl PyFactor {
    #[new]
    fn new(expression: &str) -> Self {
        PyFactor {
            inner: Factor::new(expression)
        }
    }
    
    fn compute(&self, df: &PyDataFrame) -> PyResult<PyDataFrame> {
        let result = self.inner.compute(&df.0)?;
        Ok(PyDataFrame(result))
    }
} 