import sys
from pathlib import Path
from reviewer import analyze_code_file, generate_report

# Get path to main.py in root directory
root_dir = Path(__file__).resolve().parent.parent.parent
main_path = root_dir / "main.py"

def test_review_main():
    """Test the code reviewer on main.py"""
    try:
        # Analyze main.py
        analysis = analyze_code_file(str(main_path))
        
        # Generate and save report
        report = generate_report(analysis)
        
        # Save to report file
        report_path = Path(__file__).parent / "reports" / "main_review.md"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, "w") as f:
            f.write(report)
            
        print(f"Review completed. Report saved to: {report_path}")
        
    except Exception as e:
        print(f"Error reviewing main.py: {str(e)}")
        raise

if __name__ == "__main__":
    test_review_main() 