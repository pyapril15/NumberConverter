#!/usr/bin/env python3
"""
Unit tests for Professional Number System Converter
Tests all conversion functions and edge cases
"""

import os
import sys
import unittest

# Add the main directory to the path to import main
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the converter class
import tkinter as tk
from main import NumberSystemConverter


class TestNumberConversions(unittest.TestCase):
    """Test cases for number conversion functions"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        # Create a minimal converter instance for testing
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window during testing
        self.converter = NumberSystemConverter()

    def tearDown(self):
        """Clean up after each test method"""
        self.root.destroy()

    def test_to_decimal_binary(self):
        """Test binary to decimal conversion"""
        test_cases = [
            ("0", 2, 0),
            ("1", 2, 1),
            ("10", 2, 2),
            ("11", 2, 3),
            ("100", 2, 4),
            ("101", 2, 5),
            ("110", 2, 6),
            ("111", 2, 7),
            ("1000", 2, 8),
            ("1010", 2, 10),
            ("1111", 2, 15),
            ("10000", 2, 16),
            ("11111111", 2, 255),
            ("100000000", 2, 256),
            ("1111111111111111", 2, 65535)
        ]

        for binary_str, base, expected in test_cases:
            with self.subTest(binary=binary_str):
                result = self.converter.to_decimal(binary_str, base)
                self.assertEqual(result, expected,
                                 f"Failed for {binary_str} (base {base}): expected {expected}, got {result}")

    def test_to_decimal_octal(self):
        """Test octal to decimal conversion"""
        test_cases = [
            ("0", 8, 0),
            ("1", 8, 1),
            ("7", 8, 7),
            ("10", 8, 8),
            ("11", 8, 9),
            ("17", 8, 15),
            ("20", 8, 16),
            ("77", 8, 63),
            ("100", 8, 64),
            ("377", 8, 255),
            ("777", 8, 511),
            ("1000", 8, 512)
        ]

        for octal_str, base, expected in test_cases:
            with self.subTest(octal=octal_str):
                result = self.converter.to_decimal(octal_str, base)
                self.assertEqual(result, expected,
                                 f"Failed for {octal_str} (base {base}): expected {expected}, got {result}")

    def test_to_decimal_hexadecimal(self):
        """Test hexadecimal to decimal conversion"""
        test_cases = [
            ("0", 16, 0),
            ("1", 16, 1),
            ("9", 16, 9),
            ("A", 16, 10),
            ("B", 16, 11),
            ("C", 16, 12),
            ("D", 16, 13),
            ("E", 16, 14),
            ("F", 16, 15),
            ("10", 16, 16),
            ("1A", 16, 26),
            ("FF", 16, 255),
            ("100", 16, 256),
            ("1AB", 16, 427),
            ("DEAD", 16, 57005),
            ("BEEF", 16, 48879)
        ]

        for hex_str, base, expected in test_cases:
            with self.subTest(hex=hex_str):
                result = self.converter.to_decimal(hex_str, base)
                self.assertEqual(result, expected,
                                 f"Failed for {hex_str} (base {base}): expected {expected}, got {result}")

    def test_from_decimal_binary(self):
        """Test decimal to binary conversion"""
        test_cases = [
            (0, 2, "0"),
            (1, 2, "1"),
            (2, 2, "10"),
            (3, 2, "11"),
            (4, 2, "100"),
            (5, 2, "101"),
            (8, 2, "1000"),
            (10, 2, "1010"),
            (15, 2, "1111"),
            (16, 2, "10000"),
            (255, 2, "11111111"),
            (256, 2, "100000000"),
            (1023, 2, "1111111111")
        ]

        for decimal, base, expected in test_cases:
            with self.subTest(decimal=decimal):
                result = self.converter.from_decimal(decimal, base)
                self.assertEqual(result, expected,
                                 f"Failed for {decimal} (to base {base}): expected {expected}, got {result}")

    def test_from_decimal_octal(self):
        """Test decimal to octal conversion"""
        test_cases = [
            (0, 8, "0"),
            (1, 8, "1"),
            (7, 8, "7"),
            (8, 8, "10"),
            (9, 8, "11"),
            (15, 8, "17"),
            (16, 8, "20"),
            (63, 8, "77"),
            (64, 8, "100"),
            (255, 8, "377"),
            (511, 8, "777"),
            (512, 8, "1000")
        ]

        for decimal, base, expected in test_cases:
            with self.subTest(decimal=decimal):
                result = self.converter.from_decimal(decimal, base)
                self.assertEqual(result, expected,
                                 f"Failed for {decimal} (to base {base}): expected {expected}, got {result}")

    def test_from_decimal_hexadecimal(self):
        """Test decimal to hexadecimal conversion"""
        test_cases = [
            (0, 16, "0"),
            (1, 16, "1"),
            (9, 16, "9"),
            (10, 16, "A"),
            (11, 16, "B"),
            (15, 16, "F"),
            (16, 16, "10"),
            (26, 16, "1A"),
            (255, 16, "FF"),
            (256, 16, "100"),
            (427, 16, "1AB"),
            (4095, 16, "FFF"),
            (4096, 16, "1000")
        ]

        for decimal, base, expected in test_cases:
            with self.subTest(decimal=decimal):
                result = self.converter.from_decimal(decimal, base)
                self.assertEqual(result, expected,
                                 f"Failed for {decimal} (to base {base}): expected {expected}, got {result}")

    def test_round_trip_conversions(self):
        """Test round-trip conversions (decimal → base → decimal)"""
        test_values = [0, 1, 2, 7, 8, 15, 16, 31, 32, 63, 64, 127, 128, 255, 256, 511, 512, 1023, 1024]
        test_bases = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 20, 36]

        for decimal_value in test_values:
            for base in test_bases:
                with self.subTest(value=decimal_value, base=base):
                    # Convert to base
                    converted = self.converter.from_decimal(decimal_value, base)
                    # Convert back to decimal
                    back_to_decimal = self.converter.to_decimal(converted, base)

                    self.assertEqual(back_to_decimal, decimal_value,
                                     f"Round-trip failed for {decimal_value} in base {base}: "
                                     f"got {converted} → {back_to_decimal}")

    def test_invalid_inputs(self):
        """Test handling of invalid inputs"""
        # Invalid digits for base
        invalid_cases = [
            ("2", 2),  # '2' is not valid in binary
            ("8", 8),  # '8' is not valid in octal
            ("G", 16),  # 'G' is not valid in hexadecimal
            ("Z", 10),  # 'Z' is not valid in decimal
            ("A", 2),  # 'A' is not valid in binary
        ]

        for invalid_input, base in invalid_cases:
            with self.subTest(input=invalid_input, base=base):
                result = self.converter.to_decimal(invalid_input, base)
                self.assertFalse(result,
                                 f"Should return False for invalid input '{invalid_input}' in base {base}")

    def test_edge_cases(self):
        """Test edge cases"""
        # Empty string
        result = self.converter.to_decimal("", 10)
        self.assertFalse(result)

        # Zero in different bases
        for base in [2, 8, 10, 16]:
            result = self.converter.to_decimal("0", base)
            self.assertEqual(result, 0)

            result = self.converter.from_decimal(0, base)
            self.assertEqual(result, "0")

    def test_large_numbers(self):
        """Test conversion of large numbers"""
        large_decimal = 1234567890

        # Test conversion to different bases and back
        for base in [2, 8, 16]:
            with self.subTest(base=base):
                converted = self.converter.from_decimal(large_decimal, base)
                back_to_decimal = self.converter.to_decimal(converted, base)

                self.assertEqual(back_to_decimal, large_decimal,
                                 f"Large number conversion failed for base {base}")

    def test_case_insensitive_hex(self):
        """Test case insensitive hexadecimal input"""
        test_cases = [
            ("a", 16, 10),
            ("A", 16, 10),
            ("deadbeef", 16, 3735928559),
            ("DEADBEEF", 16, 3735928559),
            ("DeAdBeEf", 16, 3735928559),
        ]

        for hex_str, base, expected in test_cases:
            with self.subTest(hex=hex_str):
                result = self.converter.to_decimal(hex_str, base)
                self.assertEqual(result, expected,
                                 f"Case insensitive test failed for {hex_str}")


class TestCalculatorFunctions(unittest.TestCase):
    """Test cases for calculator functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.root = tk.Tk()
        self.root.withdraw()
        self.converter = NumberSystemConverter()

    def tearDown(self):
        """Clean up"""
        self.root.destroy()

    def test_calculator_arithmetic(self):
        """Test calculator arithmetic operations"""
        # Test addition
        result = self.converter.perform_calculation(5, 3, '+', 10)
        self.assertEqual(result, "8")

        # Test subtraction
        result = self.converter.perform_calculation(10, 3, '-', 10)
        self.assertEqual(result, "7")

        # Test multiplication
        result = self.converter.perform_calculation(4, 3, '*', 10)
        self.assertEqual(result, "12")

        # Test division
        result = self.converter.perform_calculation(15, 3, '/', 10)
        self.assertEqual(result, "5")

        # Test division by zero
        result = self.converter.perform_calculation(10, 0, '/', 10)
        self.assertEqual(result, "Error")

    def test_calculator_different_bases(self):
        """Test calculator operations in different bases"""
        # Binary arithmetic: 101₂ + 11₂ = 1000₂ (5 + 3 = 8)
        result = self.converter.perform_calculation(5, 3, '+', 2)
        self.assertEqual(result, "1000")

        # Hexadecimal arithmetic: A₁₆ + 5₁₆ = F₁₆ (10 + 5 = 15)
        result = self.converter.perform_calculation(10, 5, '+', 16)
        self.assertEqual(result, "F")

        # Octal arithmetic: 7₈ + 1₈ = 10₈ (7 + 1 = 8)
        result = self.converter.perform_calculation(7, 1, '+', 8)
        self.assertEqual(result, "10")


class TestInputValidation(unittest.TestCase):
    """Test cases for input validation"""

    def setUp(self):
        """Set up test fixtures"""
        self.root = tk.Tk()
        self.root.withdraw()
        self.converter = NumberSystemConverter()

    def tearDown(self):
        """Clean up"""
        self.root.destroy()

    def test_validate_input_binary(self):
        """Test input validation for binary"""
        self.converter.from_base.set("2")

        # Valid binary inputs
        self.assertTrue(self.converter.validate_input(""))
        self.assertTrue(self.converter.validate_input("0"))
        self.assertTrue(self.converter.validate_input("1"))
        self.assertTrue(self.converter.validate_input("101"))
        self.assertTrue(self.converter.validate_input("1010"))

        # Invalid binary inputs
        self.assertFalse(self.converter.validate_input("2"))
        self.assertFalse(self.converter.validate_input("A"))
        self.assertFalse(self.converter.validate_input("102"))

    def test_validate_input_decimal(self):
        """Test input validation for decimal"""
        self.converter.from_base.set("10")

        # Valid decimal inputs
        self.assertTrue(self.converter.validate_input(""))
        self.assertTrue(self.converter.validate_input("0"))
        self.assertTrue(self.converter.validate_input("123"))
        self.assertTrue(self.converter.validate_input("9876543210"))

        # Invalid decimal inputs
        self.assertFalse(self.converter.validate_input("A"))
        self.assertFalse(self.converter.validate_input("12A"))

    def test_validate_input_hexadecimal(self):
        """Test input validation for hexadecimal"""
        self.converter.from_base.set("16")

        # Valid hexadecimal inputs
        self.assertTrue(self.converter.validate_input(""))
        self.assertTrue(self.converter.validate_input("0"))
        self.assertTrue(self.converter.validate_input("9"))
        self.assertTrue(self.converter.validate_input("A"))
        self.assertTrue(self.converter.validate_input("F"))
        self.assertTrue(self.converter.validate_input("DEAD"))
        self.assertTrue(self.converter.validate_input("beef"))
        self.assertTrue(self.converter.validate_input("123ABC"))

        # Invalid hexadecimal inputs
        self.assertFalse(self.converter.validate_input("G"))
        self.assertFalse(self.converter.validate_input("XYZ"))


class TestProgrammingTools(unittest.TestCase):
    """Test cases for programming tools functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.root = tk.Tk()
        self.root.withdraw()
        self.converter = NumberSystemConverter()

    def tearDown(self):
        """Clean up"""
        self.root.destroy()

    def test_base_system_definitions(self):
        """Test that all base systems are properly defined"""
        expected_bases = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
                          "11", "12", "13", "14", "15", "16", "20", "36"]

        for base in expected_bases:
            self.assertIn(base, self.converter.base_systems,
                          f"Base {base} not found in base_systems")

            base_info = self.converter.base_systems[base]
            self.assertIn("name", base_info)
            self.assertIn("digits", base_info)
            self.assertIn("max_digit", base_info)

            # Verify digits string length matches base
            expected_digit_count = int(base)
            actual_digit_count = len(base_info["digits"])
            self.assertEqual(actual_digit_count, expected_digit_count,
                             f"Base {base} should have {expected_digit_count} digits, "
                             f"but has {actual_digit_count}")


class TestSpecialCases(unittest.TestCase):
    """Test cases for special scenarios and edge cases"""

    def setUp(self):
        """Set up test fixtures"""
        self.root = tk.Tk()
        self.root.withdraw()
        self.converter = NumberSystemConverter()

    def tearDown(self):
        """Clean up"""
        self.root.destroy()

    def test_conversion_consistency(self):
        """Test that conversions are consistent across different paths"""
        # Test value
        test_value = 1000

        # Direct conversion: decimal → binary
        binary_direct = self.converter.from_decimal(test_value, 2)

        # Indirect conversion: decimal → hex → decimal → binary
        hex_intermediate = self.converter.from_decimal(test_value, 16)
        decimal_intermediate = self.converter.to_decimal(hex_intermediate, 16)
        binary_indirect = self.converter.from_decimal(decimal_intermediate, 2)

        self.assertEqual(binary_direct, binary_indirect,
                         "Direct and indirect conversion paths should yield same result")

    def test_extreme_values(self):
        """Test conversion of extreme values"""
        # Test very large number
        large_number = 2 ** 32 - 1  # Maximum 32-bit unsigned integer

        for base in [2, 8, 16]:
            with self.subTest(base=base):
                converted = self.converter.from_decimal(large_number, base)
                back_to_decimal = self.converter.to_decimal(converted, base)

                self.assertEqual(back_to_decimal, large_number,
                                 f"Extreme value conversion failed for base {base}")

    def test_all_supported_bases(self):
        """Test conversion for all supported bases"""
        test_value = 100

        for base_str in self.converter.base_systems.keys():
            base = int(base_str)
            with self.subTest(base=base):
                # Convert to base
                converted = self.converter.from_decimal(test_value, base)
                # Convert back
                back_to_decimal = self.converter.to_decimal(converted, base)

                self.assertEqual(back_to_decimal, test_value,
                                 f"Conversion failed for base {base}")


def run_tests():
    """Run all tests and display results"""
    print("=" * 60)
    print("Professional Number System Converter - Test Suite")
    print("=" * 60)

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTest(loader.loadTestsFromTestCase(TestNumberConversions))
    suite.addTest(loader.loadTestsFromTestCase(TestCalculatorFunctions))
    suite.addTest(loader.loadTestsFromTestCase(TestInputValidation))
    suite.addTest(loader.loadTestsFromTestCase(TestProgrammingTools))
    suite.addTest(loader.loadTestsFromTestCase(TestSpecialCases))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\nFAILURES:")
        for test, failure in result.failures:
            print(f"- {test}: {failure}")

    if result.errors:
        print("\nERRORS:")
        for test, error in result.errors:
            print(f"- {test}: {error}")

    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED!")
        print("\nConversion algorithms are working correctly!")
        print("The application is ready for use.")
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("\nPlease review the failures and fix the issues.")

    print("\nTest Coverage:")
    print("✓ Number base conversions (2-36 bases)")
    print("✓ Calculator arithmetic operations")
    print("✓ Input validation for all bases")
    print("✓ Programming tools functionality")
    print("✓ Edge cases and extreme values")
    print("✓ Round-trip conversion accuracy")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
