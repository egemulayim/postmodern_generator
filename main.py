"""
main.py - Main entry point for the enhanced postmodern essay generator.
This script generates a postmodern essay with optional random seed for reproducibility.
It uses the `essay` module to create the essay content and includes
academic citation conventions.
"""

from essay import generate_essay
import sys

def generate_with_seed(seed=None):
    """Generate an essay with an optional random seed for reproducibility."""
    if seed:
        import random
        random.seed(seed)
        print(f"Using random seed: {seed}")
    
    print(generate_essay())

if __name__ == "__main__":
    # Check if a seed was provided as command line argument
    if len(sys.argv) > 1:
        try:
            seed = int(sys.argv[1])
            generate_with_seed(seed)
        except ValueError:
            print(f"Error: Seed must be an integer. Got '{sys.argv[1]}'")
            print("Usage: python main.py [seed]")
            sys.exit(1)
    else:
        # No seed provided, generate with random seed
        generate_with_seed()