#!/usr/bin/env python3
"""
Unit tests for the ICM calculator.
"""
import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from icm import ICMCalculator

class TestICMCalculator(unittest.TestCase):
    """Test cases for the ICMCalculator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calculator = ICMCalculator()
    
    def test_calculate_simple_icm(self):
        """Test simple ICM calculations."""
        # Test with equal stacks
        stacks = (1000, 1000, 1000)
        payouts = (100, 50, 25)
        equities = self.calculator.calculate_simple_icm(stacks, payouts)
        
        # With equal stacks, equities should be equal
        self.assertAlmostEqual(equities[0], equities[1], places=2)
        self.assertAlmostEqual(equities[1], equities[2], places=2)
        
        # Sum of equities should equal sum of payouts
        self.assertAlmostEqual(sum(equities), sum(payouts), places=2)
        
        # Test with unequal stacks
        stacks = (2000, 1000, 500)
        equities = self.calculator.calculate_simple_icm(stacks, payouts)
        
        # Larger stacks should have higher equity
        self.assertTrue(equities[0] > equities[1])
        self.assertTrue(equities[1] > equities[2])
        
        # Sum of equities should equal sum of payouts
        self.assertAlmostEqual(sum(equities), sum(payouts), places=2)
    
    def test_calculate_icm(self):
        """Test the main ICM calculation method."""
        # This should call calculate_simple_icm under the hood
        stacks = [1000, 1000, 1000]
        payouts = [100, 50, 25]
        equities = self.calculator.calculate_icm(stacks, payouts)
        
        # With equal stacks, equities should be equal
        self.assertAlmostEqual(equities[0], equities[1], places=2)
        self.assertAlmostEqual(equities[1], equities[2], places=2)
        
        # Sum of equities should equal sum of payouts
        self.assertAlmostEqual(sum(equities), sum(payouts), places=2)
    
    def test_calculate_icm_pressure(self):
        """Test ICM pressure calculations."""
        # Test with equal stacks
        stacks = [1000, 1000, 1000]
        payouts = [100, 50, 25]
        
        # For equal stacks, pressure should be moderate
        pressure = self.calculator.calculate_icm_pressure(stacks, payouts, 0)
        self.assertTrue(0 <= pressure <= 1)
        
        # Test with big stack
        stacks = [3000, 1000, 500]
        
        # Big stack should have low pressure
        pressure = self.calculator.calculate_icm_pressure(stacks, payouts, 0)
        self.assertTrue(pressure < 0.5)
        
        # Small stack should have high pressure
        pressure = self.calculator.calculate_icm_pressure(stacks, payouts, 2)
        self.assertTrue(pressure > 0.5)
        
        # Test with extreme stack differences
        stacks = [9000, 500, 500]
        
        # Big stack should have very low pressure
        pressure = self.calculator.calculate_icm_pressure(stacks, payouts, 0)
        self.assertTrue(pressure < 0.3)
        
        # Small stack should have very high pressure
        pressure = self.calculator.calculate_icm_pressure(stacks, payouts, 1)
        self.assertTrue(pressure > 0.7)
    
    def test_nash_equilibrium_push_fold(self):
        """Test Nash equilibrium push/fold calculations."""
        stacks = [10, 15, 20]
        positions = ['btn', 'sb', 'bb']
        blinds = (1, 2)
        
        # Test without ICM
        nash_ranges = self.calculator.nash_equilibrium_push_fold(stacks, positions, blinds)
        
        # Check that all positions have thresholds
        for pos in positions:
            self.assertIn(pos, nash_ranges)
            push_threshold, call_threshold = nash_ranges[pos]
            self.assertTrue(0 <= push_threshold <= 1)
            self.assertTrue(0 <= call_threshold <= 1)
        
        # Button should be able to push wider than BB
        btn_push, _ = nash_ranges['btn']
        bb_push, _ = nash_ranges['bb']
        self.assertTrue(btn_push <= bb_push)
        
        # Test with ICM
        payouts = [100, 50, 25]
        nash_ranges_icm = self.calculator.nash_equilibrium_push_fold(stacks, positions, blinds, payouts)
        
        # ICM should make ranges tighter
        for pos in positions:
            push_no_icm, _ = nash_ranges[pos]
            push_icm, _ = nash_ranges_icm[pos]
            self.assertTrue(push_icm >= push_no_icm)

if __name__ == '__main__':
    unittest.main()
