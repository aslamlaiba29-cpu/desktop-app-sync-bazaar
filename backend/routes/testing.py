# backend/routes/testing.py
from flask import Blueprint, jsonify
from backend.models import db, TestResult
import subprocess
import re
import os
import time
import logging

bp = Blueprint('testing', __name__)

WORKSPACE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

@bp.route('/run', methods=['POST'])
def run_tests():
    # Execute pytest in a separate process to avoid in-process interference
    try:
        # Clear old test results
        TestResult.query.delete()
        db.session.commit()

        start_time = time.time()
        # Run pytest command
        res = subprocess.run(
            ["python", "-m", "pytest", "--verbose"],
            capture_output=True,
            text=True,
            cwd=WORKSPACE_DIR
        )
        duration = round(time.time() - start_time, 2)

        stdout = res.stdout or ""
        stderr = res.stderr or ""
        full_output = f"STDOUT:\n{stdout}\n\nSTDERR:\n{stderr}"

        # Parse output for test names and results
        # E.g. tests/test_auth.py::test_register PASSED
        # Or tests/test_auth.py::test_register FAILED
        lines = stdout.split('\n')
        parsed_results = []
        
        test_pattern = re.compile(r"^(tests/test_\w+\.py::\w+)\s+(\w+)")

        for line in lines:
            line = line.strip()
            match = test_pattern.search(line)
            if match:
                test_name = match.group(1)
                status = match.group(2)  # PASSED, FAILED, etc.
                
                # Normalize status
                if "PASSED" in status.upper():
                    norm_status = "PASSED"
                elif "FAILED" in status.upper():
                    norm_status = "FAILED"
                else:
                    norm_status = "SKIPPED"

                test_res = TestResult(
                    test_name=test_name,
                    status=norm_status,
                    duration=0.1,  # Mocked duration per specific test, or parsed
                    output=line
                )
                db.session.add(test_res)
                parsed_results.append({
                    "test_name": test_name,
                    "status": norm_status
                })

        # If no tests were parsed (e.g. pytest failed to run or no tests found)
        if not parsed_results:
            # Add a generic result indicating test suite failure
            test_res = TestResult(
                test_name="TestSuiteExecution",
                status="FAILED" if res.returncode != 0 else "SKIPPED",
                duration=duration,
                output=full_output
            )
            db.session.add(test_res)
            parsed_results.append({
                "test_name": "TestSuiteExecution",
                "status": "FAILED" if res.returncode != 0 else "SKIPPED"
            })

        db.session.commit()

        logging.info(f"PyTest Run complete: return code {res.returncode}. Duration={duration}s")
        return jsonify({
            "status": "success",
            "message": "Tests executed successfully!",
            "summary": {
                "total": len(parsed_results),
                "passed": sum(1 for r in parsed_results if r['status'] == 'PASSED'),
                "failed": sum(1 for r in parsed_results if r['status'] == 'FAILED'),
                "duration": duration
            },
            "output": full_output,
            "results": parsed_results
        })

    except Exception as e:
        logging.error(f"Error executing pytest: {str(e)}")
        return jsonify({"status": "error", "message": f"Could not run tests: {str(e)}"}), 500

@bp.route('/results', methods=['GET'])
def get_test_results():
    results = TestResult.query.order_by(TestResult.run_at.desc()).all()
    out = []
    for r in results:
        out.append({
            "id": r.id,
            "test_name": r.test_name,
            "status": r.status,
            "duration": r.duration,
            "output": r.output,
            "run_at": r.run_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify({"status": "success", "results": out})
