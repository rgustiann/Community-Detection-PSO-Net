import unittest
import tempfile
import os
import pandas as pd
import numpy as np
from collections import defaultdict
import sys
import coverage

# Import modules yang akan ditest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import load_network
from pso_algorithm import (
    initialize_population, decode_particle, calculate_modularity, 
    crossover, mutate, pso_net
)

class TestPSOWhiteBox(unittest.TestCase):
    
    def setUp(self):
        """Setup test data"""
        self.test_data_valid = "1\t2\n2\t3\n3\t4\n4\t1\n"
        self.test_data_empty = "node1\tnode2\n"
        self.test_data_single = "node1\tnode2\n1\t1\n"
        self.test_data_mixed = "node1\tnode2\n1\t2\n2.0\t3\n3\t4.5\n"
        
    def create_temp_file(self, content):
        """Helper function to create temporary TSV file"""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.tsv', delete=False)
        temp_file.write(content)
        temp_file.close()
        return temp_file.name
    
    def test_1_file_upload_valid(self):
        print("🧪 Test 1: File Upload Valid")
        temp_file = self.create_temp_file(self.test_data_valid)
        
        try:
            network, nodes = load_network(temp_file, verbose=False)
            self.assertIsInstance(network, defaultdict)
            self.assertIsInstance(nodes, list)
            self.assertGreater(len(nodes), 0)
            self.assertEqual(len(network), 4)
            
            print("Berhasil")
            
        except Exception as e:
            print(f" Gagal: {str(e)}")
            self.fail(f"File upload gagal: {str(e)}")
        finally:
            os.unlink(temp_file)
    
    def test_2_empty_network(self):
        """Test Case 2: Branch Coverage - Empty Network"""
        print("🧪 Test 2: Empty Network")
        temp_file = self.create_temp_file(self.test_data_empty)
        
        try:
            network, nodes = load_network(temp_file, verbose=False)
            modularity = calculate_modularity(network, {})
            
            # Assertions
            self.assertEqual(modularity, 0)
            self.assertEqual(len(nodes), 0)
            
            print("✅ PASSED: Empty network handled correctly")
            
        except Exception as e:
            print(f"❌ FAILED: {str(e)}")
            self.fail(f"Empty network test failed: {str(e)}")
        finally:
            os.unlink(temp_file)
    
    def test_3_pso_iterations(self):
        """Test Case 3: Loop Coverage - PSO Iterations"""
        print("🧪 Test 3: PSO Iterations")
        temp_file = self.create_temp_file(self.test_data_valid)
        
        try:
            network, nodes = load_network(temp_file, verbose=False)
            
            # Test with max_gen = 1
            _, _, q_scores_1 = pso_net(network, num_particles=5, max_gen=1)
            self.assertEqual(len(q_scores_1), 1)
            
            # Test with max_gen = 5
            _, _, q_scores_5 = pso_net(network, num_particles=5, max_gen=5)
            self.assertEqual(len(q_scores_5), 5)
            
            print("✅ PASSED: PSO iterations work correctly")
            
        except Exception as e:
            print(f"❌ FAILED: {str(e)}")
            self.fail(f"PSO iterations test failed: {str(e)}")
        finally:
            os.unlink(temp_file)
    
    def test_4_modularity_zero_edges(self):
        """Test Case 4: Condition Coverage - Modularity Calculation"""
        print("🧪 Test 4: Modularity with Zero Edges")
        
        try:
            empty_network = defaultdict(set)
            empty_network[1] = set()
            empty_network[2] = set()
            
            modularity = calculate_modularity(empty_network, {1: 1, 2: 2})
            
            # Assertion
            self.assertEqual(modularity, 0)
            
            print("✅ PASSED: Modularity calculation handles zero edges")
            
        except ZeroDivisionError:
            print("❌ FAILED: Division by zero error")
            self.fail("Division by zero in modularity calculation")
        except Exception as e:
            print(f"❌ FAILED: {str(e)}")
            self.fail(f"Modularity calculation failed: {str(e)}")
    
 
    def test_5_node_type_conversion(self):
        """Test Case 6: Branch Coverage - Node Type Conversion"""
        print("🧪 Test 6: Node Type Conversion")
        temp_file = self.create_temp_file(self.test_data_mixed)
        
        try:
            network, nodes = load_network(temp_file, verbose=False)
            
            # Check that all nodes are converted to int
            for node in nodes:
                self.assertIsInstance(node, int)
            
            print("✅ PASSED: Node type conversion works")
            
        except Exception as e:
            print(f"❌ FAILED: {str(e)}")
            self.fail(f"Node type conversion failed: {str(e)}")
        finally:
            os.unlink(temp_file)
    
    def test_6_crossover_operations(self):
        """Test Case 7: Loop Coverage - Crossover Operations"""
        print("🧪 Test 7: Crossover Operations")
        
        try:
            parent1 = {1: 2, 2: 3, 3: 4, 4: 1}
            parent2 = {1: 3, 2: 4, 3: 1, 4: 2}
            
            child1, child2 = crossover(parent1, parent2)
            
            # Assertions
            self.assertEqual(len(child1), len(parent1))
            self.assertEqual(len(child2), len(parent2))
            self.assertEqual(set(child1.keys()), set(parent1.keys()))
            self.assertEqual(set(child2.keys()), set(parent2.keys()))
            
            print("✅ PASSED: Crossover operations work correctly")
            
        except Exception as e:
            print(f"❌ FAILED: {str(e)}")
            self.fail(f"Crossover operations failed: {str(e)}")
    
    def test_7_mutation_process(self):
        """Test Case 8: Condition Coverage - Mutation Process"""
        print("🧪 Test 8: Mutation Process")
        
        try:
            network = defaultdict(set)
            network[1] = {2}
            network[2] = {1}
            network[3] = set() 
            
            particle = {1: 2, 2: 1, 3: 3}
            
            mutated = mutate(particle, network)
            
            # Assertions
            self.assertIsInstance(mutated, dict)
            self.assertEqual(len(mutated), len(particle))
            
            print("✅ PASSED: Mutation process handles isolated nodes")
            
        except Exception as e:
            print(f"❌ FAILED: {str(e)}")
            self.fail(f"Mutation process failed: {str(e)}")
    
    def test_8_population_initialization(self):
        """Test Case 9: Path Coverage - Population Initialization"""
        print("🧪 Test 9: Population Initialization")
        
        try:
            network = defaultdict(set)
            network[1] = {2, 3}
            network[2] = {1, 3}
            network[3] = {1, 2}
            
            population = initialize_population(network, num_particles=5)
            
            # Assertions
            self.assertEqual(len(population), 5)
            for particle in population:
                self.assertEqual(len(particle), 3)  # 3 nodes
                for node, neighbor in particle.items():
                    self.assertIn(neighbor, network[node])
            
            print("✅ PASSED: Population initialization works correctly")
            
        except Exception as e:
            print(f"❌ FAILED: {str(e)}")
            self.fail(f"Population initialization failed: {str(e)}")
    
    def test_9_file_processing_error(self):
        """Test Case 10: Exception Handling - File Processing"""
        print("🧪 Test 10: File Processing Error Handling")
        
        try:
            # Test with non-existent file
            with self.assertRaises(FileNotFoundError):
                load_network("non_existent_file.tsv")
            
            # Test with corrupted TSV (wrong separator)
            corrupt_content = "1,2\n2,3\n3,4\n"  # Using comma instead of tab
            temp_file = self.create_temp_file(corrupt_content)
            
            try:
                network, nodes = load_network(temp_file, verbose=False)
                # Should handle gracefully, might create single nodes
                self.assertIsInstance(network, defaultdict)
                
            finally:
                os.unlink(temp_file)
            
            print("✅ PASSED: File processing error handling works")
            
        except Exception as e:
            print(f"❌ FAILED: {str(e)}")
            self.fail(f"File processing error handling failed: {str(e)}")

def run_white_box_tests():
    """Run all white box tests with coverage"""
    print("=" * 60)
    print("🚀 STARTING WHITE BOX TESTING")
    print("=" * 60)
    
    # Initialize coverage
    cov = coverage.Coverage()
    cov.start()
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPSOWhiteBox)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Stop coverage and generate report
    cov.stop()
    cov.save()
    
    print("\n" + "=" * 60)
    print("📊 COVERAGE REPORT")
    print("=" * 60)
    
    try:
        cov.report()
        cov.html_report(directory='htmlcov')
        print("\n📁 HTML coverage report generated in 'htmlcov' directory")
    except Exception as e:
        print(f"⚠️  Could not generate coverage report: {e}")
    
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed}")
    print(f"Failed: {failures}")
    print(f"Errors: {errors}")
    
    if failures > 0:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if errors > 0:
        print("\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    success_rate = (passed / total_tests) * 100 if total_tests > 0 else 0
    print(f"\n🎯 Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("✅ TESTING COMPLETED SUCCESSFULLY!")
    else:
        print("⚠️  TESTING COMPLETED WITH ISSUES!")

if __name__ == "__main__":
    run_white_box_tests()