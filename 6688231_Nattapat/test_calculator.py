"""
Unit tests for the calculator module.
"""

import pytest
from calculator import add, subtract, multiply, divide, calculate


class TestAddition:
    """Test cases for the add function."""
    
    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        assert add(2, 3) == 5
    
    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        assert add(-2, -3) == -5
    
    def test_add_mixed_numbers(self):
        """Test adding positive and negative numbers."""
        assert add(5, -3) == 2
        assert add(-5, 3) == -2
    
    def test_add_floats(self):
        """Test adding floating point numbers."""
        assert add(1.5, 2.5) == 4.0
    
    def test_add_zero(self):
        """Test adding zero."""
        assert add(5, 0) == 5
        assert add(0, 0) == 0


class TestSubtraction:
    """Test cases for the subtract function."""
    
    def test_subtract_positive_numbers(self):
        """Test subtracting two positive numbers."""
        assert subtract(5, 3) == 2
    
    def test_subtract_negative_numbers(self):
        """Test subtracting two negative numbers."""
        assert subtract(-2, -3) == 1
    
    def test_subtract_mixed_numbers(self):
        """Test subtracting positive and negative numbers."""
        assert subtract(5, -3) == 8
        assert subtract(-5, 3) == -8
    
    def test_subtract_floats(self):
        """Test subtracting floating point numbers."""
        assert subtract(5.5, 2.5) == 3.0
    
    def test_subtract_zero(self):
        """Test subtracting zero."""
        assert subtract(5, 0) == 5
        assert subtract(0, 5) == -5


class TestMultiplication:
    """Test cases for the multiply function."""
    
    def test_multiply_positive_numbers(self):
        """Test multiplying two positive numbers."""
        assert multiply(3, 4) == 12
    
    def test_multiply_negative_numbers(self):
        """Test multiplying two negative numbers."""
        assert multiply(-3, -4) == 12
    
    def test_multiply_mixed_numbers(self):
        """Test multiplying positive and negative numbers."""
        assert multiply(3, -4) == -12
        assert multiply(-3, 4) == -12
    
    def test_multiply_floats(self):
        """Test multiplying floating point numbers."""
        assert multiply(2.5, 4.0) == 10.0
    
    def test_multiply_by_zero(self):
        """Test multiplying by zero."""
        assert multiply(5, 0) == 0
        assert multiply(0, 0) == 0
    
    def test_multiply_by_one(self):
        """Test multiplying by one."""
        assert multiply(5, 1) == 5


class TestDivision:
    """Test cases for the divide function."""
    
    def test_divide_positive_numbers(self):
        """Test dividing two positive numbers."""
        assert divide(10, 2) == 5
    
    def test_divide_negative_numbers(self):
        """Test dividing two negative numbers."""
        assert divide(-10, -2) == 5
    
    def test_divide_mixed_numbers(self):
        """Test dividing positive and negative numbers."""
        assert divide(10, -2) == -5
        assert divide(-10, 2) == -5
    
    def test_divide_floats(self):
        """Test dividing floating point numbers."""
        assert divide(10.0, 2.5) == 4.0
    
    def test_divide_by_one(self):
        """Test dividing by one."""
        assert divide(5, 1) == 5
    
    def test_divide_by_zero(self):
        """Test that dividing by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(5, 0)
    
    def test_divide_zero_by_number(self):
        """Test dividing zero by a number."""
        assert divide(0, 5) == 0


class TestCalculateFunction:
    """Test cases for the calculate function."""
    
    def test_calculate_with_symbol_operators(self):
        """Test calculate with symbol operators."""
        assert calculate('+', 5, 3) == 8
        assert calculate('-', 5, 3) == 2
        assert calculate('*', 5, 3) == 15
        assert calculate('/', 10, 2) == 5
    
    def test_calculate_with_word_operators(self):
        """Test calculate with word operators."""
        assert calculate('add', 5, 3) == 8
        assert calculate('subtract', 5, 3) == 2
        assert calculate('multiply', 5, 3) == 15
        assert calculate('divide', 10, 2) == 5
    
    def test_calculate_invalid_operation(self):
        """Test calculate with invalid operation."""
        with pytest.raises(ValueError, match="Invalid operation"):
            calculate('%', 5, 3)
        with pytest.raises(ValueError, match="Invalid operation"):
            calculate('power', 5, 3)
    
    def test_calculate_divide_by_zero(self):
        """Test calculate with division by zero."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calculate('/', 5, 0)
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calculate('divide', 5, 0)
